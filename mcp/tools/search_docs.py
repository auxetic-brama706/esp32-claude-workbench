"""
Tool for semantic search over ESP32 documentation using a local RAG pipeline.
"""

import os
import pickle

faiss_index = None
meta_data = None
encoder = None

def _load_resources():
    global faiss_index, meta_data, encoder
    
    if faiss_index is not None and meta_data is not None and encoder is not None:
        return True
        
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".cache")
    index_path = os.path.join(cache_dir, "esp32_docs.faiss")
    meta_path = os.path.join(cache_dir, "esp32_docs_meta.pkl")
    
    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        return False
        
    try:
        import faiss
        from sentence_transformers import SentenceTransformer
        
        faiss_index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            meta_data = pickle.load(f)
            
        encoder = SentenceTransformer("all-MiniLM-L6-v2")
        return True
    except ImportError as e:
        raise ImportError(f"Missing required ML libraries. Run 'pip install -r mcp/requirements.txt' ({e})")

def search_esp_docs(query: str, top_k: int = 5) -> str:
    """Search ESP32 Technical Reference Manuals and datasheets semantically."""
    try:
        if not _load_resources():
            return "Error: ESP32 documentation index not found. Please run `python scripts/index_esp_docs.py` first."
            
        # Encode the query
        q_emb = encoder.encode([query])
        
        # Search the index
        distances, indices = faiss_index.search(q_emb, top_k)
        
        results = [f"=== ESP32 Docs Search: \"{query}\" ===\n"]
        
        for i, idx in enumerate(indices[0]):
            if idx == -1: 
                continue
            meta = meta_data[idx]
            
            source_name = meta.get("source_name", "Unknown Source")
            page = meta.get("page", "?")
            url = meta.get("url", "N/A")
            tags = ", ".join(meta.get("tags", []))
            text = meta.get("text", "")
            
            res_str = f"[{i+1}] {source_name} — Page {page}\n"
            res_str += f"Source: {url}\n"
            res_str += f"Tags: {tags}\n"
            res_str += f"---\n{text}\n---\n"
            
            results.append(res_str)
            
        return "\n".join(results)
    except Exception as e:
        return f"Search Error: {str(e)}"
