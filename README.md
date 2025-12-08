# GuessRoyale – Hybrid Number & Word Guessing Game

**Team: Runtime_Terror!**

GuessRoyale is a Python-based interactive game featuring both Number Guessing and a Wordle-style Word Guessing mode, all inside a unified GUI built with wxPython. Players earn points, manage lives, and even get a second chance through a unique Revival Arena containing four fast-paced mini-games. A persistent leaderboard stores high scores across sessions.

This project was developed as part of our academic coursework, combining concepts of Python programming, modular architecture, GUI development, and game design.

---

## Features

### Dual Game Modes

**Number Guessing Mode**  
Classic high/low number guessing with dynamic difficulty.

**Word Guessing Mode (Wordle-inspired)**  
Letter tiles update with color feedback:  
- Green → correct letter in correct position  
- Yellow → correct letter in wrong position  
- Red → letter not in the word

---

## Lives & Scoring System

- Points awarded based on attempts remaining.  
- Limited lives to increase challenge and replay value.

---

## Revival Arena (Second Chance System)

When the player loses all lives, a random mini-game is chosen:

- Memory Flash  
- Direction Reflex  
- Fast Typing  
- Quick Math  

Winning restores one life and continues gameplay.

---

## Leaderboard

The game stores player results (name, score, mode, difficulty) in a persistent leaderboard file.

---

## GUI Built With wxPython

- Unified interface for both game modes  
- Dynamic resizing for Wordle grid  
- Clean input flow and status updates  
- Message dialogs for feedback and round completion

---

## Tech Stack

- Python 3.10+  
- wxPython for GUI  
- Standard libraries: random, json, time

---

## How to Run

**Run GUI Version:**  
```bash
python gui_wx.py
```

**Run CLI Version:**  
```bash
python main.py
```

---

## Team: Runtime_Terror!

1. [Chinmay J Rao](https://github.com/chinmay1505-droid)  
2. [Darshan R Chavan](https://github.com/darshan0548-glitch)  
3. [Digantha G D](https://github.com/notthegd-lab)  
4. [Jayasheel K S](https://github.com/ksjayasheel)

---

## License

This project is intended for academic use under the institution’s guidelines.

---

## Acknowledgments

We’d like to thank our instructors and peers for continuous support and feedback during development.
