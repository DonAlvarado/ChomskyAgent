from typing import Protocol, Any


class IVisualizer(Protocol):
    def visualize(self, obj: Any) -> str:
        ...
