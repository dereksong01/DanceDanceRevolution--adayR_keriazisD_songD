from typing import Dict, Tuple

class Point:
    def __init__(self: 'Point', x: int, y: int, color: str) -> None:
        self.x = x
        self.y = y
        self.color = color

class Canvas:
    def __init__(self: 'Canvas') -> None:
        self.points: Dict[Tuple[int, int], Point] = {}

    def add(self: 'Canvas', p: Point) -> None:
        self.points[(p.x, p.y)] = p

