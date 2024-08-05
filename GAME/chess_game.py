# chess_game.py
import chess

class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def get_board(self):
        return self.board

    def make_move(self, move):
        print(f"Attempting move: {move}")
        try:
            self.board.push_uci(move)
            print("Move made successfully")
            return True
        except ValueError as e:
            print(f"Move failed: {e}")
            return False

    def get_legal_moves(self):
        return [move.uci() for move in self.board.legal_moves]
