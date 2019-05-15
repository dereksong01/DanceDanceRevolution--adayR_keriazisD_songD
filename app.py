# Team DanceDanceRevolution

from json import dumps
from typing import Dict, Optional, Union, cast, NamedTuple

from flask import Flask, render_template, request

from util.safe_json import coerce_type
from util.room import RoomId, Room, RoomStatus
from util.player import Player
from util.canvas import PointTuple
from util.config import config

app = Flask(__name__)
#  c = config()

rooms: Dict[RoomId, Room] = {}

@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/join', methods=['POST'])
def join() -> str:
    """
    Adds a player to a room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>,
        "name": <player_name>
    }

    Returns a string in the following JSON format:
    {
        "player_id": <player_id>
    }
    """
    class Join(NamedTuple):
        name: str
        room_id: str
    data = cast(Optional[Join], coerce_type(request.get_json(), Join))
    if data is None:
        return ''  # TODO: Better error handling
    p = Player(data.name)  # Create player with `name`
    if data.room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[data.room_id]
    r.players[p.id] = p  # Add `p` to the room
    result = {'player_id': p.id}  # Create result data
    return dumps(result)


@app.route('/create', methods=['POST'])
def create() -> str:
    """
    Creates a new room

    Expects a POST in the following JSON format:
    {
        "name": <player_name>
    }

    Returns a string in the following JSON format:
    {
        "room_id": <room_id>,
        "player_id": <player_id>
    }
    """
    class Create(NamedTuple):
        name: str
    data = cast(Optional[Create], coerce_type(request.get_json(), Create))
    if data is None:
        return ''  # TODO: Better error handling
    p = Player(data.name)  # Create player with `name`
    r = Room()  # Create a new room
    r.players[p.id] = p  # Add `p` to the room
    rooms[r.id] = r  # Add the room to `rooms`
    result = {'room_id': r.id, 'player_id': p.id}  # Create result data
    return dumps(result)


@app.route('/room/<room_id>')
def room(room_id: RoomId) -> str:
    return render_template('room.html')


@app.route('/start', methods=['POST'])
def start() -> str:
    """
    Starts the game for a given room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>
    }
    """
    class Start(NamedTuple):
        room_id: str
    data = cast(Optional[Start], coerce_type(request.get_json(), Start))
    if data is None:
        return ''  # TODO: Better error handling
    if data.room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[data.room_id]
    success = r.start_game()
    if not success:
        return ''  # TODO: Better error handling
    return ''


@app.route('/wait')
def wait() -> str:
    """
    Returns the status of a given room in WAITING

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>,
        "player_id": <player_id>
    }

    Returns a string in the following JSON format:
    {
        "status": <status>,
        "players": [
            {
                "name": <name>,
                "color": <color>
            }
        ]
    }
    """
    class Status(NamedTuple):
        room_id: str
        player_id: str
    data = cast(Optional[Status], coerce_type(request.get_json(), Status))
    if data is None:
        return ''  # TODO: Better error handling
    if data.room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[data.room_id]
    return r.wait_json(data.player_id)


@app.route('/canvas', methods=['POST'])
def canvas() -> str:
    """
    Returns game information for a given room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>,
        "draw_id": <draw_id>
    }

    Returns a string in the following JSON format:
    {
        "point": {
            "color": <color>,
            "x": <x>,
            "y": <y>
        },
        "new_draw_id": <new_draw_id>
    }
    """
    class Canvas(NamedTuple):
        room_id: str
        draw_id: str
    data = cast(Optional[Canvas], coerce_type(request.get_json(), Canvas))
    if data is None:
        return ''  # TODO: Better error handling
    if data.room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[data.room_id]
    return r.canvas_json(data.draw_id)


@app.route('/info')
def info() -> str:
    """
    Returns game information for a given room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>
    }

    Returns a string in the following JSON format:
    {
        "status": <status>
    }
    """
    class Info(NamedTuple):
        room_id: str
    data = cast(Optional[Info], coerce_type(request.get_json(), Info))
    if data is None:
        return ''  # TODO: Better error handling
    if data.room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[data.room_id]
    result = {'status': r.status.name}
    return dumps(result)


@app.route('/update', methods=['POST'])
def update() -> str:
    """
    Update the canvas for a given room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>,
        "player_id": <player_id>,
        "point": {
            "x": <x>,
            "y": <y>
        }
    }
    """
    class Update(NamedTuple):
        room_id: str
        player_id: str
        point: PointTuple
    data = cast(Optional[Update], coerce_type(request.get_json(), Update))
    if data is None:
        return ''  # TODO: Better error handling
    if data.room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[data.room_id]
    success = r.update(data.player_id, data.point)
    if not success:
        return ''  # TODO: Better error handling
    return ''


@app.route('/end', methods=['POST'])
def end() -> str:
    """
    Ends a given player's turn for a given room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>,
        "player_id": <player_id>
    }
    """
    class End(NamedTuple):
        room_id: str
        player_id: str
    data = cast(Optional[End], coerce_type(request.get_json(), End))
    if data is None:
        return ''  # TODO: Better error handling
    if data.room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[data.room_id]
    success = r.end_turn(data.player_id)
    if not success:
        return ''  # TODO: Better error handling
    return ''


@app.route('/vote', methods=['POST'])
def vote() -> str:
    """
    Vote for a player to be the fake artist

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>,
        "player_id": <player_id>,
        "fake_arist_pos": <fake_arist_pos>
    }
    """
    class Vote(NamedTuple):
        room_id: str
        player_id: str
        fake_arist_pos: int
    data = cast(Optional[Vote], coerce_type(request.get_json(), Vote))
    if data is None:
        return ''  # TODO: Better error handling
    if data.room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[data.room_id]
    success = r.vote(data.player_id, data.fake_arist_pos)
    if not success:
        return ''  # TODO: Better error handling
    return ''


if __name__ == '__main__':
    app.debug = __debug__  # Run `python -O` to set to False
    app.run()

