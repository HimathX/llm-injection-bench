import os
import anthropic
from .base import LLMClient

class ClaudeClient(LLMClient):
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # Using the latest haiku to match the project plan intent "claude-haiku-4-5" (likely intended 3.5)
        self.model = "claude-3-5-haiku-latest"

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
