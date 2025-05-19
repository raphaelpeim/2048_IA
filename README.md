# 🧠 2048 Game – Python Edition

A Python implementation of the classic **2048 game**, complete with:
- Terminal and GUI interfaces (via Tkinter)
- AI player using a simple heuristic
- Modular, testable architecture

---

## 🎮 Features

- Classic 2048 gameplay (with arrow key controls)
- GUI with Tkinter
- Optional AI autoplay (press `A` key to toggle)
- Customizable board size and win condition
- Well-structured code: separation of core logic, GUI, helpers, and tests

---

## 📂 Project Structure

```
2048-game/
├── main.py                  # Entry point – launches the GUI
├── src/
│   ├── common/              # Reusable constants and helpers
│   │   ├── constants.py
│   │   ├── direction.py
│   │   ├── moves.py
│   │   └── utils.py
│   ├── core/                # Game logic and AI
│   │   ├── ai.py
│   │   └── game.py
│   └── gui/                 # Graphical UI (Tkinter)
│       └── gui.py
├── tests/                  # Unit tests
│   ├── test_game.py
│   └── test_moves.py
```

---

## 🚀 Getting Started

### ✅ Requirements
- Python 3.8+
- Tkinter (usually bundled with Python)
  
Install any missing dependencies:

```bash
pip install -r requirements.txt
```

> If using macOS and see a Tkinter warning, you can suppress it with:
> `export TK_SILENCE_DEPRECATION=1`

---

### ▶️ Running the Game

```bash
python main.py
```

---

## 🔹 Controls

- **Arrow Keys**: Move tiles up, down, left, right
- **A key**: Toggle AI autoplay

---

## 🧪 Testing

Run tests with:

```bash
python -m unittest discover tests
```

---

## 🤖 AI Strategy

The AI picks the move that leaves the board with the most empty cells — a simple yet effective strategy for early to mid-game survival.

---

## 📌 Customization

You can edit `src/common/constants.py` to:
- Change the board size
- Modify the winning tile value

---

## 📃 License

MIT License – feel free to use, modify, and share!

---

Enjoy the game! 🚀
