from __future__ import annotations


class ModelProvider:
    def summarize(self, prompt: str) -> str:
        raise NotImplementedError


class StaticModelProvider(ModelProvider):
    def __init__(self, response: str) -> None:
        self._response = response

    def summarize(self, prompt: str) -> str:
        return self._response
