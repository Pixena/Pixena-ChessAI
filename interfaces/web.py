from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from game.adapter import GameAdapter
from ai_worker import AIWorker
from utils.config import CONFIG
from utils.logger import logger
app = Flask('pixena', template_folder='templates', static_folder='static')
CORS(app)
GAME = GameAdapter()
AI = AIWorker()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/state')
def state():
    return jsonify({'fen': GAME.fen(), 'legal': GAME.legal_moves(), 'over': GAME.is_game_over()})
@app.route('/move', methods=['POST'])
def move():
    data = request.json or {}
    fen = data.get('fen')
    uci = data.get('move')
    if fen:
        try:
            GAME.board = __import__('chess').Board(fen)
        except Exception:
            pass
    if uci:
        prev = GAME.fen()
        ok = GAME.push(uci)
        if ok:
            AI.observe_opponent(prev, uci)
        else:
            return jsonify({'ok': False, 'error': 'illegal move'}), 400
    if GAME.is_game_over():
        return jsonify({'ok': True, 'fen': GAME.fen(), 'result': GAME.result()})
    ai_move = AI.best_move(GAME.fen())
    if ai_move:
        GAME.push(ai_move)
    return jsonify({'ok': True, 'fen': GAME.fen(), 'ai_move': ai_move})
def run_app():
    app.run(host=CONFIG['host'], port=CONFIG['port'])