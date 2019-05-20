from typing import Dict, Tuple, NamedTuple, Optional
from util.ids import gen_id


class Point(NamedTuple):
    x: int
    y: int
    color: str


class PointTuple(NamedTuple):
    x: int
    y: int


DrawId = str


class Canvas:
    def __init__(self: "Canvas") -> None:
        self.points: Dict[DrawId, Tuple[Point, DrawId]] = {}
        self.init_id = ""
        self.last_id = self.init_id

    def add(self: "Canvas", p: Point) -> None:
        new_id = gen_id(64)
        self.points[self.last_id] = (p, new_id)
        self.last_id = new_id

    def get(self: "Canvas", p: DrawId) -> Optional[Tuple[Point, DrawId]]:
        return self.points.get(p)
