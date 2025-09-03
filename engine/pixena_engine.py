import chess
import time
import random
import math

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

pst_white = {
    chess.PAWN:[
         0,   5,  10,  20,  20,  10,   5,   0,
         5,  10,  15,  25,  25,  15,  10,   5,
         5,  10,  10,  20,  20,  10,  10,   5,
         0,   0,   0,  15,  15,   0,   0,   0,
         5,  -5, -10,   0,   0, -10,  -5,   5,
         5,  10,  10, -20, -20,  10,  10,   5,
         0,   0,   0,   0,   0,   0,   0,   0,
         0,   0,   0,   0,   0,   0,   0,   0
    ],
    chess.KNIGHT:[
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ],
    chess.BISHOP:[
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ],
    chess.ROOK:[
         0,  0,  5, 10, 10,  5,  0,  0,
         0,  0,  5, 10, 10,  5,  0,  0,
         0,  0,  5, 10, 10,  5,  0,  0,
         0,  0,  5, 10, 10,  5,  0,  0,
         0,  0,  5, 10, 10,  5,  0,  0,
         0,  0,  5, 10, 10,  5,  0,  0,
        25, 25, 25, 25, 25, 25, 25, 25,
         0,  0,  5, 10, 10,  5,  0,  0
    ],
    chess.QUEEN:[
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],
    chess.KING:[
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20
    ]
}

class TTEntry:
    def __init__(self, depth, score, flag, move):
        self.depth = depth
        self.score = score
        self.flag = flag
        self.move = move

class PixenaEngine:
    def __init__(self, depth=6, time_limit=3):
        self.max_depth = depth
        self.time_limit = time_limit
        self.start_time = 0
        self.nodes = 0
        self.tt = {}
        self.history = {}
        self.opponent_stats = {}
        self.zobrist_piece = [[random.getrandbits(64) for _ in range(64)] for _ in range(12)]
        self.zobrist_side = random.getrandbits(64)
        self.zobrist_castle = [random.getrandbits(64) for _ in range(16)]
        self.zobrist_ep = [random.getrandbits(64) for _ in range(8)]
    def zobrist_hash(self, board):
        h = 0
        for sq in range(64):
            piece = board.piece_at(sq)
            if piece:
                idx = (piece.piece_type - 1) + (0 if piece.color else 6)
                h ^= self.zobrist_piece[idx][sq]
        if board.turn == chess.WHITE:
            h ^= self.zobrist_side
        cr = 0
        if board.has_kingside_castling_rights(chess.WHITE): cr |= 1
        if board.has_queenside_castling_rights(chess.WHITE): cr |= 2
        if board.has_kingside_castling_rights(chess.BLACK): cr |= 4
        if board.has_queenside_castling_rights(chess.BLACK): cr |= 8
        h ^= self.zobrist_castle[cr]
        if board.ep_square is not None:
            file = board.ep_square % 8
            h ^= self.zobrist_ep[file]
        return h
    def evaluate(self, board):
        material = 0
        pst = 0
        for sq in range(64):
            piece = board.piece_at(sq)
            if not piece:
                continue
            val = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                material += val
                pst += pst_white[piece.piece_type][sq]
            else:
                material -= val
                pst -= pst_white[piece.piece_type][63 - sq]
        mobility = len(list(board.legal_moves))
        score = material + pst + mobility
        return score if board.turn == chess.WHITE else -score
    def quiescence(self, board, alpha, beta):
        stand = self.evaluate(board)
        if stand >= beta:
            return beta
        if alpha < stand:
            alpha = stand
        captures = [m for m in board.legal_moves if board.is_capture(m)]
        captures = sorted(captures, key=lambda m: self.capture_score(board, m), reverse=True)
        for m in captures:
            if time.time() - self.start_time > self.time_limit:
                break
            board.push(m)
            score = -self.quiescence(board, -beta, -alpha)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha
    def capture_score(self, board, move):
        if board.is_en_passant(move):
            return 1000
        captured = board.piece_at(move.to_square)
        attacker = board.piece_at(move.from_square)
        if captured and attacker:
            return piece_values[captured.piece_type] - piece_values[attacker.piece_type]
        return 0
    def predict_opponent(self, board):
        key = self.zobrist_hash(board)
        stats = self.opponent_stats.get(key, {})
        if not stats:
            return []
        items = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        return [k for k,v in items[:5]]
    def order_moves(self, board, moves):
        scored = []
        predicted = self.predict_opponent(board)
        for m in moves:
            score = 0
            if board.is_capture(m):
                score += 100000 + self.capture_score(board, m)
            key = (m.from_square, m.to_square)
            score += self.history.get(key, 0)
            if m.uci() in predicted:
                score += 5000
            scored.append((score, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored]
    def search(self, board, depth, alpha, beta):
        if time.time() - self.start_time > self.time_limit:
            raise TimeoutError()
        self.nodes += 1
        key = self.zobrist_hash(board)
        entry = self.tt.get(key)
        if entry and entry.depth >= depth:
            if entry.flag == 'EXACT':
                return entry.score, entry.move
            elif entry.flag == 'LOWER' and entry.score > alpha:
                alpha = entry.score
            elif entry.flag == 'UPPER' and entry.score < beta:
                beta = entry.score
            if alpha >= beta:
                return entry.score, entry.move
        if depth == 0:
            q = self.quiescence(board, alpha, beta)
            return q, None
        best_move = None
        moves = list(board.legal_moves)
        moves = self.order_moves(board, moves)
        for m in moves:
            board.push(m)
            score, _ = self.search(board, depth-1, -beta, -alpha)
            score = -score
            board.pop()
            if score > alpha:
                alpha = score
                best_move = m
            if alpha >= beta:
                key2 = (m.from_square, m.to_square)
                self.history[key2] = self.history.get(key2, 0) + (1 << depth)
                break
        flag = 'EXACT' if best_move else 'UPPER'
        self.tt[key] = TTEntry(depth, alpha, flag, best_move)
        return alpha, best_move
    def learn_opponent(self, fen_before, uci_move):
        b = chess.Board(fen_before)
        key = self.zobrist_hash(b)
        if key not in self.opponent_stats:
            self.opponent_stats[key] = {}
        self.opponent_stats[key][uci_move] = self.opponent_stats[key].get(uci_move, 0) + 1
    def best_move(self, fen):
        board = chess.Board(fen)
        self.start_time = time.time()
        self.nodes = 0
        best = None
        try:
            for d in range(1, self.max_depth + 1):
                score, move = self.search(board, d, -9999999, 9999999)
                if move:
                    best = move
                if time.time() - self.start_time > self.time_limit:
                    break
        except TimeoutError:
            pass
        return best.uci() if best else None