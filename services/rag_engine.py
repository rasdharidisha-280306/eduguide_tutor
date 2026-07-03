import os
import google.generativeai as genai
from config.settings import Settings

class RAGEngine:
    """Engine for performing retrieval-augmented generation (RAG) using the Gemini API."""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = Settings.GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured. Please check your .env file.")
        
        genai.configure(api_key=self.api_key)

    def query(self, user_query: str, retrieved_context: str) -> str:
        """
        Answers a user query based on the retrieved context document segments.
        
        Args:
            user_query (str): The query or question from the user.
            retrieved_context (str): The context extracted from relevant document parts.
            
        Returns:
            str: The AI generated answer text.
        """
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
            
        prompt = f"Answer the user query based ONLY on the context. Query: {user_query}\nContext: {retrieved_context}"
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error executing RAG query: {e}"
