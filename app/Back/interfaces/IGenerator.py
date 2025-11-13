from typing import Protocol, Dict, Any


class IGenerator(Protocol):
    def generate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        ...
