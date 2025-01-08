import os
import google.generativeai as genai

class GeminiInvoke:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash-8b')
            GeminiInvoke._initialized = True

    async def generate_content(self, prompt):
        """Generate content using Gemini model
        
        Args:
            prompt (str): The prompt to send to Gemini
            
        Returns:
            str: The generated response text
        """
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None
