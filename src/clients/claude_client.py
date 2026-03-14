import os
import anthropic
from .base import LLMClient

class ClaudeClient(LLMClient):
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-haiku-4-5"

    async def generate(self, prompt: str) -> str:
        try:
            response = await self.client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
            )
            return response.content[0].text
        except Exception as e:
            raise e
