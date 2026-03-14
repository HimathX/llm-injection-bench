import os
import google.generativeai as genai
from .base import LLMClient

class GeminiClient(LLMClient):
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def generate(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            # Handle potential safety block where response.text throws ValueError
            return response.text if response.parts else ""
        except Exception as e:
            # For logging/debug, though the evaluator will handle retries
            raise e
