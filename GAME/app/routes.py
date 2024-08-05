# app/routes.py
from flask import Blueprint, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from chess_game import ChessGame

main = Blueprint('main', __name__)
socketio = SocketIO()

games = {}

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/board')
def board():
    game_id = request.args.get('game_id')
    if game_id not in games:
        games[game_id] = ChessGame()
    board_state = games[game_id].get_board().fen()
    return jsonify(board_state)

@main.route('/api/move', methods=['POST'])
def move():
    game_id = request.json.get('game_id')
    move = request.json.get('move')
    print(f"Game ID: {game_id}, Move: {move}")
    if game_id not in games:
        games[game_id] = ChessGame()
    success = games[game_id].make_move(move)
    print(f"Move successful: {success}")
    return jsonify({'success': success, 'board': games[game_id].get_board().fen(), 'legal_moves': games[game_id].get_legal_moves()})

@socketio.on('join')
def on_join(data):
    game_id = data['game_id']
    join_room(game_id)
    emit('status', {'msg': f'Player has joined the game {game_id}'}, room=game_id)

@socketio.on('leave')
def on_leave(data):
    game_id = data['game_id']
    leave_room(game_id)
    emit('status', {'msg': f'Player has left the game {game_id}'}, room=game_id)

@socketio.on('move')
def on_move(data):
    game_id = data['game_id']
    move = data['move']
    if game_id not in games:
        games[game_id] = ChessGame()
    success = games[game_id].make_move(move)
    emit('move', {'success': success, 'board': games[game_id].get_board().fen(), 'legal_moves': games[game_id].get_legal_moves()}, room=game_id)
