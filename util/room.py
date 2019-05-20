from typing import Dict, List, Counter
from enum import Enum, auto, unique
from random import shuffle, choice
from json import dumps
from collections import Counter

from util.ids import Id, gen_id
from util.canvas import Canvas, DrawId, Point, PointTuple
from util.player import Player, PlayerId


@unique
class RoomStatus(Enum):
    WAITING = auto()
    IN_GAME = auto()
    CASTING = auto()
    RESULTS = auto()


RoomId = Id

MAX_ROUND = 3


class Room:
    def __init__(self: "Room") -> None:
        self.id = gen_id(8)
        self.players: Dict[PlayerId, Player] = {}
        self.canvas = Canvas()
        self.status = RoomStatus.WAITING
        self.order: List[PlayerId] = []
        self.turn = 0
        self.round = 0
        self.fake = ""
        self.votes: Counter[PlayerId] = Counter()
        self.has_voted: Dict[PlayerId, bool] = {}

    def wait_json(self: "Room", player_id: PlayerId) -> str:
        players = [
            {"name": p.name, "color": p.color} for p in self.players.values()
        ]
        result = {"status": self.status.name, "players": players}
        return dumps(result)

    def canvas_json(self: "Room", draw_id: DrawId) -> str:
        data = self.canvas.get(draw_id)
        if data is None:
            return ""  # TODO: Better error handling
        p, new_draw_id = data
        result = {
            "new_draw_id": new_draw_id,
            "points": [{"x": p.x, "y": p.y, "color": p.color}],
        }
        return dumps(result)

    def info_json(self: "Room") -> str:
        pass

    def start_game(self: "Room") -> bool:
        if self.status is not RoomStatus.WAITING:
            return False
        self.order = list(self.players.keys())
        shuffle(self.order)
        self.round += 1
        self.fake = choice(self.order)
        self.has_voted[self.fake] = True
        self.status = RoomStatus.IN_GAME
        return True

    def end_turn(self: "Room", player_id: PlayerId) -> bool:
        if self.status is not RoomStatus.IN_GAME:
            return False
        if self.order[self.turn] != player_id:
            return False
        self.turn += 1
        if self.turn == len(self.order):
            self.turn = 0
            self.round += 1
            if self.round > MAX_ROUND:
                self.end_game()
        return True

    def end_game(self: "Room") -> bool:
        self.status = RoomStatus.CASTING
        return True  # Anticipate the possibility of future success checking

    def update(
        self: "Room", player_id: PlayerId, points: List[PointTuple]
    ) -> bool:
        if player_id not in self.players:
            return False
        # TODO: Uncomment this before production please
        #  if len(self.order) <= self.turn:
        #  return False
        #  if self.order[self.turn] != player_id:
        #  return False
        player = self.players[player_id]
        for point in points:
            p = Point(point.x, point.y, player.color)
            self.canvas.add(p)
        return True

    def vote(self: "Room", player_id: PlayerId, fake_arist_pos: int) -> bool:
        if self.status is not RoomStatus.CASTING:
            return False
        self.has_voted[player_id] = True
        if fake_arist_pos < 0 or fake_arist_pos >= len(self.order):
            return True  # Abstained from voting
        self.votes[self.order[fake_arist_pos]] += 1
        if all(self.has_voted.values()):
            self.status = RoomStatus.RESULTS
        return True

    def results(self: "Room") -> str:
        if self.status is not RoomStatus.RESULTS:
            return ""  # TODO: Better error handling
        return ""  # TODO: Implement this
