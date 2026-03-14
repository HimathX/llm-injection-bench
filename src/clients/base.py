import abc

class LLMClient(abc.ABC):
    @abc.abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate response from the LLM asynchronously."""
        pass
