from game.adapter import GameAdapter
from ai_worker import AIWorker
from utils.logger import logger
def main():
    g = GameAdapter()
    ai = AIWorker()
    print('PixenaChess AI by Рустем Эмир-Велиев. Вводите ходы в UCI, например e2e4. exit чтобы выйти.')
    while True:
        print('FEN:', g.fen())
        if g.is_game_over():
            print('Игра окончена', g.result())
            break
        s = input('Ваш ход: ').strip()
        if s in ('exit', 'quit'):
            break
        prev = g.fen()
        ok = g.push(s)
        if not ok:
            print('Неверный ход')
            continue
        ai.observe_opponent(prev, s)
        if g.is_game_over():
            print('Игра окончена', g.result())
            break
        mv = ai.best_move(g.fen())
        if mv:
            pushed = g.push(mv)
            logger.info('PixenaChess AI played %s pushed=%s', mv, pushed)
        else:
            print('AI не сделал ход')