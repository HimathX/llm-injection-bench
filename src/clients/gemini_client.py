import os
from google import genai
from .base import LLMClient

class GeminiClient(LLMClient):
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-2.0-flash"

    async def generate(self, prompt: str) -> str:
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text if response.text else ""
        except Exception as e:
            # For logging/debug, though the evaluator will handle retries
            raise e
