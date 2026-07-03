import os
import json
import google.generativeai as genai
from config.settings import Settings

class LLMService:
    """Core AI Service handling structured quiz generation, smart text summarization, and RAG contextual answers using Gemini."""
    
    def __init__(self):
        self.api_key = Settings.GEMINI_API_KEY
        self.model_name = "gemini-2.5-flash"
        
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY is not configured inside environment properties.")
            
        genai.configure(api_key=self.api_key)
            
    def generate_quiz(self, text_content: str, num_questions: int = 5, difficulty: str = "Medium") -> list:
        """Generates multiple-choice quiz questions returning a clean structured list."""
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY is not configured inside environment properties.")
            Error executing summary abstraction routine: 404 models/gemini-pro is not found for API version v1beta, or is not supported for generateContent. Call ModelService.ListModels to see the list of available models and their supported methods.
        if not text_content or len(text_content.strip()) == 0:
            return []

        # JSON response constraints enforce karne ke liye strict instructions prompt
        prompt = f"""
        You are an expert tutor. Based on the following context, generate exactly {num_questions} multiple-choice questions (MCQs) at a '{difficulty}' difficulty level.
        
        Context material:
        \"\"\"{text_content[:6000]}\"\"\"
        
        Return ONLY a raw JSON array matching this exact schema specification without any markdown formatting wrappers or backticks:
        [
          {{
            "question": "The question string goes here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A"
          }}
        ]
        Make sure the 'answer' matches exactly one of the strings inside the 'options' array.
        """
        
        try:
            model = genai.GenerativeModel(self.model_name)
            # JSON format control configuration instruction mapping
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            clean_text = response.text.strip()
            # Markdown text wrappers safeguards cleaning
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
                
            return json.loads(clean_text.strip())
            
        except Exception as e:
            print(f"❌ Exception triggered in LLMService quiz engine generation: {e}")
            return []

    def summarize_text(self, text_content: str) -> str:
        """Generates comprehensive structured bullet notes summaries from text blobs."""
        if not self.api_key or not text_content:
            return "No text context provided for summary generation pipelines."
            
        prompt = f"Provide an insightful, well-structured executive summary with bullet points highlighting key educational concepts from this text:\n\n{text_content[:8000]}"
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error executing summary abstraction routine: {e}"