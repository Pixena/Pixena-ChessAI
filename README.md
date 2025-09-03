
PixenaChess AI / PixenaChess AI

English
Author: Рустем Эмир-Велиев

PixenaChess AI is a modular chess engine written in Python. It is meant to be practical and readable: iterative deepening, alpha-beta with move ordering, transposition table, quiescence search, piece-square evaluation, opponent modeling and a small opening book. This engine is standalone and does not call external engines. It is tuned to play at a strong club level and can reach 2000+ Elo on modern hardware with proper tuning.

Quick start
1. pip install -r requirements.txt
2. python app.py --mode web
3. open http://localhost:5001

Production deployment
1. Build docker image: docker build -t pixena-chess .
2. Run container: docker run -p 5001:5001 -v /path/to/data:/app/data pixena-chess
3. Put Nginx in front, enable SSL, monitor resources. Use systemd or container orchestrator.

Embedding PixenaChess in your project
Copy files from archive into your project folder and import ai_worker.AIClient or call HTTP API.

Example: call via HTTP
import requests
def ask_pixena(fen, url='http://localhost:5001/move'):
    r = requests.post(url, json={'fen': fen})
    return r.json()

Example: integrate directly as a library
from ai_worker import AIWorker
ai = AIWorker()
move = ai.best_move(fen)
ai.observe_opponent(prev_fen, uci_move)

How to pass data to the engine
Use FEN strings. Provide the position before asking. If you want Pixena to learn opponent tendencies, call observe_opponent with the position before opponent move and the move they played.

Русский
Автор: Рустем Эмир-Велиев

PixenaChess AI модульный шахматный движок на Python. Писал руками, чтобы было удобно читать и модифицировать. Движок не вызывает внешние бинарные движки, всё внутри Python. В нём есть итеративное углубление, альфа-бета с сортировкой ходов, транспозиционная таблица, квиеcценция, таблицы позиций, модель оппонента и простая дебютная книжка. С правильной настройкой может показывать уровень 2000+ Эло в локальных тестах.

Быстрый старт
1. pip install -r requirements.txt
2. python app.py --mode web
3. открыть http://localhost:5001

Продакшен
1. docker build -t pixena-chess .
2. docker run -p 5001:5001 -v /path/to/data:/app/data pixena-chess
3. ставьте Nginx впереди, SSL, systemd/контейнерный оркестратор, мониторьте CPU/RAM.

Интеграция в сайт или сервис
Если сайт на Python, просто импортируйте ai_worker.AIWorker и вызывайте метод best_move(fen). Для внешних сервисов удобен HTTP endpoint /move, который принимает json {fen: "..."} и возвращает {move: "e2e4"}.

Пример запроса (Python)
import requests
resp = requests.post('http://localhost:5001/move', json={'fen': fen})
data = resp.json()
move = data.get('move')

Пример встраивания в любой проект
Распакуйте архив в папку проекта, импортируйте ai_worker как обычный модуль или используйте HTTP API. Передавайте FEN, принимайте UCI ход.

License
This project is MIT licensed. Author: Рустем Эмир-Велиев