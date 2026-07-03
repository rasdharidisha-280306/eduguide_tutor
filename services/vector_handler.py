import os
import json
import numpy as np
import google.generativeai as genai
from config.settings import Settings

class VectorService:
    """Manages text embedding generation and local vector index storage."""
    
    def __init__(self):
        self.api_key = Settings.GEMINI_API_KEY
        self.index_path = Settings.CHROMA_PATH / "vectors.json"
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured. Please check your .env file.")
        genai.configure(api_key=self.api_key)
        self.index = self._load_index()

    def _load_index(self) -> list:
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_index(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=4)

    def generate_embedding(self, text: str) -> list:
        if not self.api_key:
            return [0.0] * 768
        try:
            response = genai.embed_content(model="models/text-embedding-004", content=text, task_type="retrieval_document")
            return response['embedding']
        except:
            return [0.0] * 768

    def add_documents(self, chunks: list):
        for chunk in chunks:
            embedding = self.generate_embedding(chunk["text"])
            self.index.append({"text": chunk["text"], "metadata": chunk["metadata"], "vector": embedding})
        self._save_index()

    def query_top_k(self, query_text: str, k: int = 3) -> list:
        if not self.index:
            return []
        query_vector = np.array(self.generate_embedding(query_text))
        scored_results = []
        for item in self.index:
            item_vector = np.array(item["vector"])
            dot = np.dot(query_vector, item_vector)
            norm = np.linalg.norm(query_vector) * np.linalg.norm(item_vector)
            similarity = dot / norm if norm > 0 else 0.0
            scored_results.append((similarity, item))
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [res[1] for res in scored_results[:k]]