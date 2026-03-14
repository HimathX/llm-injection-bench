import os
import groq
from .base import LLMClient

class GroqClient(LLMClient):
    def __init__(self):
        self.client = groq.AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    async def generate(self, prompt: str) -> str:
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return chat_completion.choices[0].message.content or ""
        except Exception as e:
            raise e
