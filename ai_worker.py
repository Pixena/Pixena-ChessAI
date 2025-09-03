from utils.config import CONFIG
from engine.pixena_engine import PixenaEngine
from utils.logger import logger
class AIWorker:
    def __init__(self):
        self.engine = PixenaEngine(depth=CONFIG.get('ai_depth', 6), time_limit=CONFIG.get('time_limit', 3))
    def best_move(self, fen):
        move = self.engine.best_move(fen)
        logger.info('PixenaChess AI выбрал ход %s для fen %s', move, fen)
        return move
    def observe_opponent(self, fen_before, uci_move):
        self.engine.learn_opponent(fen_before, uci_move)
        logger.info('PixenaChess наблюдал за ходом противника %s в %s', uci_move, fen_before)