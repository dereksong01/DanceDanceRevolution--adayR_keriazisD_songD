# Team DanceDanceRevolution

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create/<room_id>')
def create(room_id):
    pass

@app.route('/join/<room_id>')
def join(room_id):
    pass

@app.route('/room/<room_id>')
def room(room_id):
    pass

@app.route('/start')
def start():
    """
    Initializes and starts the game for a given room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>,
        "players": [
            "player_id": <player_id>,
            "color": <color>,
            "name": <name>
         ]
    }
    """
    pass

@app.route('/turn')
def turn():
    """
    Ends a given player's turn for a given room

    Expects a POST in the following JSON format:
    {
        "room_id": <room_id>,
        "player_id": <player_id>,
        "line": [
            {
                "x": <x>,
                "y": <y>
            }
        ]
    }
    """
    pass

if __name__ == '__main__':
    app.debug = True
    app.run()

