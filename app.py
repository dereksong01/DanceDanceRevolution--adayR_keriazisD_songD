# Team DanceDanceRevolution

from json import dumps
from typing import Dict, Optional, Union, cast

from flask import Flask, render_template, request

from util.safe_json import safe_loads
from util.room import RoomId, Room, RoomStatus
from util.player import Player
from util.canvas import Point

app = Flask(__name__)

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
    join_type = {
        'name': str,
        'room_id': str,
    }
    data = cast(
        Optional[Dict[str, str]], safe_loads(request.get_json(), join_type),
    )
    if data is None:
        return ''  # TODO: Better error handling
    room_id = data['room_id']
    name = data['name']
    p = Player(name)  # Create player with `name`
    if room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[room_id]
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
        "player_id": <player_id>
    }
    """
    create_type = {
        'name': str,
    }
    data = cast(
        Optional[Dict[str, str]], safe_loads(request.get_json(), create_type),
    )
    if data is None:
        return ''  # TODO: Better error handling
    name = data['name']
    p = Player(name)  # Create player with `name`
    r = Room()  # Create a new room
    r.players[p.id] = p  # Add `p` to the room
    rooms[r.id] = r  # Add the room to `rooms`
    result = {'player_id': p.id}  # Create result data
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
    start_type = {
        'room_id': str,
    }
    data = cast(
        Optional[Dict[str, str]], safe_loads(request.get_json(), start_type),
    )
    if data is None:
        return ''  # TODO: Better error handling
    room_id = data['room_id']
    if room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[room_id]
    success = r.start_game()
    if not success:
        return ''  # TODO: Better error handling
    return ''


@app.route('/status')
def status() -> str:
    """
    Returns the status of a given room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>
    }

    Returns a string in the following JSON format:
    {
        "status": <status>
    }
    """
    status_type = {
        'room_id': str,
    }
    data = cast(
        Optional[Dict[str, str]], safe_loads(request.get_json(), status_type),
    )
    if data is None:
        return ''  # TODO: Better error handling
    room_id = data['room_id']
    if room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[room_id]
    return r.status_json()


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
    info_type = {
        'room_id': str,
    }
    data = cast(
        Optional[Dict[str, str]], safe_loads(request.get_json(), info_type),
    )
    if data is None:
        return ''  # TODO: Better error handling
    room_id = data['room_id']
    if room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[room_id]
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
    update_type = {
        'room_id': str,
        'player_id': str,
        'point': {
            'x': int,
            'y': int
        }
    }
    data = cast(
        Optional[Dict[str, Union[str, Dict[str, int]]]],
        safe_loads(request.get_json(), update_type),
    )
    if data is None:
        return ''  # TODO: Better error handling
    room_id = cast(str, data['room_id'])
    player_id = cast(str, data['player_id'])
    point = cast(Dict[str, int], data['point'])
    if room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[room_id]
    if player_id not in r.players:
        return ''  # TODO: Better error handling
    player = r.players[player_id]
    color = player.color
    p = Point(point['x'], point['y'], color)
    r.canvas.add(p)
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
    end_type = {
        'room_id': str,
        'player_id': str
    }
    data = cast(
        Optional[Dict[str, str]], safe_loads(request.get_json(), end_type),
    )
    if data is None:
        return ''  # TODO: Better error handling
    room_id = data['room_id']
    player_id = data['player_id']
    if room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[room_id]
    success = r.end_turn(player_id)
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
    end_type = {
        'room_id': str,
        'player_id': str,
        "fake_arist_pos": int
    }
    data = cast(
        Optional[Dict[str, Union[str, int]]],
        safe_loads(request.get_json(), end_type),
    )
    if data is None:
        return ''  # TODO: Better error handling
    room_id = cast(str, data['room_id'])
    player_id = cast(str, data['player_id'])
    fake_arist_pos = cast(int, data['fake_arist_pos'])
    if room_id not in rooms:
        return ''  # TODO: Better error handling
    r = rooms[room_id]
    success = r.vote(player_id, fake_arist_pos)
    if not success:
        return ''  # TODO: Better error handling
    return ''


if __name__ == '__main__':
    app.debug = __debug__  # Run `python -O` to set to False
    app.run()

