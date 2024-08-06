import logging

# Add this at the top to configure logging
logging.basicConfig(level=logging.DEBUG)

# Existing imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from chess_logic import is_valid_move, update_board_state
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.String, nullable=False)
    active_spells = db.Column(db.String, nullable=True)  # Adjust based on how you want to store spells

db.create_all()

@app.route('/api/new_game', methods=['POST'])
def new_game():
    initial_board_state = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    game = Game(board_state=initial_board_state, active_spells=None)
    db.session.add(game)
    db.session.commit()
    logging.debug(f"New game created with ID: {game.id} and initial board state: {game.board_state}")
    return jsonify({"game_id": game.id, "board_state": game.board_state})

@app.route('/api/move', methods=['POST'])
def move():
    data = request.json
    game_id = data.get('game_id')
    move = data.get('move')

    game = Game.query.get(game_id)
    if not game:
        logging.error(f"Invalid game ID: {game_id}")
        return jsonify({"error": "Invalid game ID"}), 400

    board_state = game.board_state
    logging.debug(f"Board state before move: {board_state}")
    logging.debug(f"Move: {move}")

    if is_valid_move(board_state, move):
        new_board_state = update_board_state(board_state, move)
        game.board_state = new_board_state
        db.session.commit()
        logging.debug(f"Board state after move: {new_board_state}")
        return jsonify({"board_state": game.board_state})
    else:
        logging.error("Invalid move attempted")
        return jsonify({"error": "Invalid move"}), 400

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Chess game data", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
