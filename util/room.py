from typing import Dict, List, Counter
from enum import Enum, auto, unique
from random import shuffle, choice
from json import dumps
from collections import Counter

from util.ids import Id, gen_id
from util.canvas import Canvas
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
    def __init__(self: 'Room') -> None:
        self.id = gen_id(8)
        self.players: Dict[PlayerId, Player] = {}
        self.canvas = Canvas()
        self.status = RoomStatus.WAITING
        self.order: List[PlayerId] = []
        self.turn = 0
        self.round = 0
        self.fake = ''
        self.votes: Counter[PlayerId] = Counter()

    def status_json(self: 'Room') -> str:
        result = {'status': self.status.name}
        return dumps(result)

    def info_json(self: 'Room') -> str:
        pass

    def start_game(self: 'Room') -> bool:
        if self.status is not RoomStatus.WAITING:
            return False
        self.order = list(self.players.keys())
        shuffle(self.order)
        self.round += 1
        self.fake = choice(self.order)
        self.status = RoomStatus.IN_GAME
        return True

    def end_turn(self: 'Room', player_id: PlayerId) -> bool:
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

    def end_game(self: 'Room') -> None:
        self.status = RoomStatus.CASTING

    def vote(self: 'Room', player_id: PlayerId, fake_arist_pos: int) -> bool:
        if self.status is not RoomStatus.CASTING:
            return False
        if fake_arist_pos >= len(self.order):
            return False
        self.votes[self.order[fake_arist_pos]] += 1
        return True

