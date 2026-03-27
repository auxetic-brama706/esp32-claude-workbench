"""
Script to download, parse, and index ESP32 documentation for local RAG search.
"""

import os
import re
import yaml
import pickle
import requests
import typing
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

try:
    import faiss
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Error: Missing ML libraries. Please run 'pip install -r mcp/requirements.txt'")
    exit(1)

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".cache")
PDF_DIR = os.path.join(CACHE_DIR, "pdfs")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def download_file(url: str, target_path: str, progress: Progress, task_id: int) -> None:
    """Download a file with rich progress."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    progress.update(task_id, total=total_size)
    
    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                progress.advance(task_id, len(chunk))

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """Simple word-based chunker."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))
        i += chunk_size - overlap
    return chunks

def crawl_html(start_url: str, max_pages: int = 200) -> typing.Generator[tuple[str, str, str], None, None]:
    """Crawl domain and yield title, text, and url."""
    visited = set()
    to_visit = [start_url]
    domain = urlparse(start_url).netloc
    
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited: continue
        visited.add(url)
        
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code != 200: continue
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # Find new internal links
            for a in soup.find_all("a", href=True):
                next_url = urljoin(url, a["href"])
                if urlparse(next_url).netloc == domain and next_url not in visited:
                    to_visit.append(next_url)
                    
            text = soup.get_text(separator="\n")
            title = soup.title.string if soup.title else "HTML Doc"
            yield title, url, text
        except Exception:
            continue

def main() -> None:
    yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs_sources.yaml")
    if not os.path.exists(yaml_path):
        print(f"Error: Could not find {yaml_path}")
        return

    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    sources = config.get("sources", [])
    
    chunks_data = [] # List of dict metadata
    chunks_text = [] # List of raw chunk strings to encode
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
    ) as progress:
        
        for source in sources:
            source_name = source["name"]
            url = source["url"]
            doc_type = source.get("type", "pdf")
            tags = source.get("tags", [])
            
            if doc_type == "pdf":
                filename = url.split("/")[-1]
                pdf_path = os.path.join(PDF_DIR, filename)
                
                # Download
                if not os.path.exists(pdf_path):
                    task_id = progress.add_task(f"Downloading {filename}...", total=None)
                    download_file(url, pdf_path, progress, task_id)
                    progress.update(task_id, completed=True)
                
                # Parse
                parse_task = progress.add_task(f"Parsing {filename}...", total=None)
                try:
                    doc = fitz.open(pdf_path)
                    progress.update(parse_task, total=len(doc))
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        text = page.get_text()
                        
                        docs_chunks = chunk_text(text)
                        for c in docs_chunks:
                            if len(c.strip()) > 30: # Skip very small or empty chunks
                                chunks_text.append(c)
                                chunks_data.append({
                                    "source_name": source_name,
                                    "page": page_num + 1,
                                    "url": url,
                                    "tags": tags,
                                    "text": c
                                })
                        progress.advance(parse_task, 1)
                except Exception as e:
                    print(f"Failed to parse {filename}: {e}")
            
            elif doc_type == "html_crawl":
                crawl_task = progress.add_task(f"Crawling {source_name}...", total=None)
                page_count = 0
                for title, p_url, text in crawl_html(url, max_pages=100):
                    paras = text.split("\n\n")
                    for p in paras:
                        c_text = p.strip()
                        if len(c_text) > 50:
                            chunks_text.append(c_text)
                            chunks_data.append({
                                "source_name": f"{source_name} ({title})",
                                "page": "HTML",
                                "url": p_url,
                                "tags": tags,
                                "text": c_text
                            })
                    page_count += 1
                    progress.update(crawl_task, description=f"Crawling {source_name} ({page_count} pages)")
                progress.update(crawl_task, completed=True)

        if not chunks_text:
            print("No textual data extracted from sources.")
            return

        # Encode chunks
        enc_task = progress.add_task("Loading Sentence Transformer & encoding data...", total=100)
        model = SentenceTransformer("all-MiniLM-L6-v2")
        progress.update(enc_task, completed=10, description="Encoding chunks...")
        
        # We can just let model.encode manage its own batching but we fake progress
        # For simplicity we simply run it.
        embeddings = model.encode(chunks_text, show_progress_bar=False)
        progress.update(enc_task, completed=80, description="Building FAISS index...")
        
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        
        faiss.write_index(index, os.path.join(CACHE_DIR, "esp32_docs.faiss"))
        
        with open(os.path.join(CACHE_DIR, "esp32_docs_meta.pkl"), "wb") as f:
            pickle.dump(chunks_data, f)
            
        progress.update(enc_task, completed=100, description="Done!")

    print("\n✅ Indexing complete.")
    print(f"Total Sources: {len(sources)}")
    print(f"Total Chunks: {len(chunks_text)}")
    print(f"Index Dimensions: {dim}")

if __name__ == "__main__":
    main()
