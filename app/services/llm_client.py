from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    async def generate_answer(self, prompt: str) -> str:
        ...


class MockLLMClient(LLMClient):
    async def generate_answer(self, prompt: str) -> str:
        return (
            "This is a mocked answer based on the provided context. "
            "In a real deployment this would call an LLM API."
        )


def get_llm_client(provider: str) -> LLMClient:
    return MockLLMClient()