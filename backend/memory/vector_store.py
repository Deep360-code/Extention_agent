import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class VectorStore:
    def __init__(self, index_path="memory/faiss_index.bin"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_path = index_path
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            
        # For simplicity, we'll store metadata in a separate dict or file in a real app
        # deeper implementation would use a proper vector DB or manage IDs
        self.metadata = {} 

    def store(self, text: str, meta: Dict = None):
        if not text:
            return
        
        vector = self.model.encode([text])
        self.index.add(vector.astype('float32'))
        
        # Simple ID tracking for demo
        idx = self.index.ntotal - 1
        self.metadata[idx] = {"text": text, "meta": meta or {}}
        
        # Save index locally (optional for this demo but good for persistence)
        # faiss.write_index(self.index, self.index_path)

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        vector = self.model.encode([query])
        distances, indices = self.index.search(vector.astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx in self.metadata:
                results.append(self.metadata[idx])
        return results

vector_memory = VectorStore()
