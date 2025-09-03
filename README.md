# PixenaChess AI / PixenaChess AI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Python Version](https://img.shields.io/badge/python-3.8%2B-green.svg)](#)

**English author:** Rustem Emir-Veliev (Рустем Эмир-Велиев)

---

## Overview — What is PixenaChess AI

PixenaChess AI is a compact, modular chess engine implemented in **pure Python**. It was written for clarity and extensibility — easy to read, modify and integrate. The engine includes classical ingredients for a practical engine: iterative deepening, alpha–beta pruning with move ordering, a transposition table, quiescence search, piece-square evaluation, a tiny opening book and a simple opponent-modeling component.

> *A simple engine by design — not a research monster — but it is easy to tune and extend. With proper parameter tuning and hardware it can reach strong club level play.*

This repository contains a self-contained engine and a small web UI (`app.py --mode web`) exposing an HTTP endpoint for programmatic use.

---

## Highlights / Features

* Pure Python implementation — no external engine binaries required
* Iterative deepening & alpha–beta search with move ordering
* Quiescence search and transposition table
* Piece-square tables and configurable evaluation weights
* Lightweight opponent modeling (observe opponent moves to bias selection)
* Small opening book (package data)
* HTTP API for easy integration (`/move` endpoint)
* Example web UI for local testing (runs on `http://localhost:5001` by default)

---

## Quick start

```bash
# create venv (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
python app.py --mode web
# open http://localhost:5001
```

Or run as HTTP service only:

```bash
python app.py --mode api
# default: POST /move -> {"fen": "..."} returns {"move": "e2e4"}
```

---

## Docker (production-ish)

```bash
docker build -t pixena-chess .
docker run -p 5001:5001 -v /path/to/data:/app/data pixena-chess
```

Recommended: place Nginx in front, enable SSL, supervise the container with systemd / k8s, monitor CPU/RAM.

---

## API — HTTP usage

`POST /move`

**Request** (JSON):

```json
{ "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 2 3" }
```

**Response** (JSON):

```json
{ "move": "e4e5", "info": { "depth": 12, "score": 45 } }
```

**Python example (client)**

```python
import requests

def ask_pixena(fen, url='http://localhost:5001/move'):
    r = requests.post(url, json={'fen': fen})
    r.raise_for_status()
    return r.json()

resp = ask_pixena('startpos')
print(resp['move'])
```

**Library usage (importable)**

```python
from ai_worker import AIWorker

ai = AIWorker()
move = ai.best_move(fen)
# Optional: inform the engine about opponents moves
ai.observe_opponent(prev_fen, uci_move)
```

---

## Configuration and tuning

The engine exposes several tunable parameters (see `config.py` or top of `ai_worker.py`):

* `search_depth` / `time_per_move` — control search limits
* `use_tt` — enable/disable transposition table
* `eval_weights` — numeric weights for material, mobility, pawn structure
* `quiescence_depth` — limits for quiescence search
* Move ordering heuristics (history, MVV-LVA)

**Tuning tips**

* Start with time-based iterative deepening (e.g. 100–500 ms per move) to avoid pathological fixed-depth traps.
* Use a transposition table with reasonable RAM limits; monitor memory usage on long searches.
* Increase quiescence limits carefully — it increases tactical accuracy but can slow search.
* Use opponent modeling only for repetitive opponents; it slightly biases the engine toward preparing counters.

---

## Opening book

A small built-in opening book is included in `/data/book/`. It is intentionally tiny — meant as a convenience for realistic play rather than exhaustive covering. You can replace or extend the book with your own polyglot or simple JSON/UCI table.

---

## Testing & Evaluation

* To run self-play or evaluation scripts, check `tools/benchmarks.py` (if present).
* A simple ELO estimate can be obtained by running many matches against a reference engine and fitting a logistic curve.

**Note:** CPU, clock speed and single-thread performance strongly affect wall-time strength. Python's GIL and interpreter overhead make absolute strength depend on implementation details and tuning.

---

## Project structure

```
├── ai_worker.py  
├── app.py
├── requirements.txt
├── LICENSE
├── README.md
├── data/
├── docs/
├── engine/
├── game/
├── interfaces/
├── templates/
└── utils/
```

---

## Contributing

Contributions are welcome — bug fixes, performance improvements, additional heuristics and small datasets for openings are all useful. Please follow these steps:

1. Fork the repository
2. Create a branch for your feature/fix
3. Add tests where appropriate
4. Open a pull request with a clear description

If you make changes that affect API or config formats, document them in `CHANGES.md`.

---

## Limitations & honesty

This engine was written to be readable and educational. It is intentionally simple and **may be weaker** than highly-engineered C/C++ engines out of the box. With careful tuning and additional modules (e.g. better evaluation, tablebases, NN features) it can be improved significantly.

---

## License

This project is released under the **MIT License**. See `LICENSE` for full text.

---

# Русская версия — PixenaChess AI

**Автор:** Рустем Эмир-Велиев

## Описание

PixenaChess AI — компактный модульный шахматный движок на чистом Python. Писался, чтобы было удобно читать и модифицировать: итеративное углубление, альфа-бета с сортировкой ходов, транспозиционная таблица, квиеcценция, таблицы оценки и простая дебютная книжка.

Движок автономный и не использует внешние движки. Он достаточно гибкий — с правильной настройкой и ресурсами может показывать уровень клубного игрока (в тестах 2000+ Elo возможен с оптимизацией), но по умолчанию сделан простым и обучаемым.

## Быстрый старт

```bash
pip install -r requirements.txt
python app.py --mode web
# открыть http://localhost:5001
```

## Продакшен (Docker)

```bash
docker build -t pixena-chess .
docker run -p 5001:5001 -v /path/to/data:/app/data pixena-chess
```

## API (пример)

POST `/move` принимает JSON `{ "fen": "..." }`, возвращает `{ "move": "e2e4" }`.

## Настройка и улучшение

В конфигурации доступны параметры глубины поиска, времени на ход, веса для оценки и т.п. Для улучшения силы:

* Настройте время на ход вместо фиксированной глубины
* Используйте транспозиционную таблицу и ограничьте её по памяти
* Улучшайте оценочную функцию: структура пешек, матрицы фигур, мобильность
* Добавляйте более полную дебютную книжку

## Структура репозитория

(см. раздел на английском)

## Вклад

Форк, ветка, PR — добавляйте тесты и документацию к изменениям.

## Лицензия

MIT. Автор: Рустем Эмир-Велиев
