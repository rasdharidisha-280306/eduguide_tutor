import os
import google.generativeai as genai

class QuizEngine:
    """Engine for generating interactive quizzes from text content using the Gemini API."""
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            
    def generate_quiz(self, text_content: str, num_questions: int = 5, difficulty: str = "Medium") -> list:
        """
        Generates multiple-choice quiz questions based on the provided text content.
        
        Args:
            text_content (str): The source text to generate questions from.
            num_questions (int): Number of questions to generate.
            difficulty (str): Difficulty level (Easy, Medium, Hard).
            
        Returns:
            list: A list of dictionaries representing quiz questions, e.g.:
                [
                    {
                        "question": "What is...?",
                        "options": ["A", "B", "C", "D"],
                        "answer": "A"
                    }
                ]
        """
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        
        # TODO: Implement Gemini prompt construction and API call
        # prompt = f"Generate {num_questions} {difficulty} level MCQs from: {text_content}..."
        # model = genai.GenerativeModel(self.model_name)
        # response = model.generate_content(prompt)
        
        return []
