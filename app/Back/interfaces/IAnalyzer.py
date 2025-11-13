from typing import Protocol, Dict, Any


class IAnalyzer(Protocol):
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        ...
