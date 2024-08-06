from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from chess_logic import is_valid_move, update_board_state, is_valid_spell_target
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
    active_spells = db.Column(db.String, nullable=True)

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String, nullable=False)

db.create_all()

@app.route('/api/new_game', methods=['POST'])
def new_game():
    initial_board_state = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    game = Game(board_state=initial_board_state, active_spells=None)
    db.session.add(game)
    db.session.commit()
    return jsonify({"game_id": game.id, "board_state": game.board_state})

@app.route('/api/move', methods=['POST'])
def move():
    data = request.json
    game_id = data.get('game_id')
    move = data.get('move')

    game = Game.query.get(game_id)
    if not game:
        return jsonify({"error": "Invalid game ID"}), 400

    board_state = game.board_state

    if is_valid_move(board_state, move):
        new_board_state = update_board_state(board_state, move)
        game.board_state = new_board_state
        db.session.commit()
        return jsonify({"board_state": game.board_state})
    else:
        return jsonify({"error": "Invalid move"}), 400

@app.route('/api/cast_spell', methods=['POST'])
def cast_spell():
    data = request.json
    game_id = data.get('game_id')
    spell_id = data.get('spell_id')
    target_piece = data.get('target_piece')

    game = Game.query.get(game_id)
    spell = Spell.query.get(spell_id)

    if not game:
        return jsonify({"error": "Invalid game ID"}), 400
    if not spell:
        return jsonify({"error": "Invalid spell ID"}), 400

    if not is_valid_spell_target(spell, target_piece):
        return jsonify({"error": "Invalid spell target"}), 400

    # Add the spell to active_spells and update the game state
    active_spells = game.active_spells if game.active_spells else ''
    active_spells += f'{spell.id}:{target_piece},'
    game.active_spells = active_spells
    db.session.commit()

    return jsonify({"board_state": game.board_state, "active_spells": game.active_spells})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Chess game data", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
