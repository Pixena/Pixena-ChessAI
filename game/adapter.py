import chess
class GameAdapter:
    def __init__(self, fen=None):
        self.board = chess.Board(fen) if fen else chess.Board()
    def fen(self):
        return self.board.fen()
    def legal_moves(self):
        return [m.uci() for m in self.board.legal_moves]
    def push(self, uci):
        try:
            move = chess.Move.from_uci(uci)
        except Exception:
            return False
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False
    def push_san(self, san):
        try:
            move = self.board.parse_san(san)
            self.board.push(move)
            return True
        except Exception:
            return False
    def is_game_over(self):
        return self.board.is_game_over()
    def result(self):
        return self.board.result()