from typing import Protocol


class IAgent(Protocol):
    def reply(self, message: str) -> str:
        ...
