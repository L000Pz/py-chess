# ♟️ Python Chess Game ♔

Welcome to **Python Chess Game**! This project brings you the thrill of chess in a Python-based application, styled with a theme inspired by [Chess.com](https://www.chess.com/). Whether you’re a seasoned player or new to the game, enjoy classic chess right from your command line! 🎉
<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1gm9OcGlmoFmMJmCKnHpMRwS21bcdQYYZ" alt="Description of image" width="300"/>
</p>

---

## 🎮 Features

- **🎨 Chess.com Theme**: Familiar visuals inspired by Chess.com for an immersive chess experience.
- **♟️ Full Chess Rules**: All rules implemented, including:
  - ✅ Complete piece movement and capture mechanics
  - 🔄 Special moves like castling, en passant, and pawn promotion
  - ⚠️ Check and checkmate detection for challenging gameplay
- **🔍 Captured Pieces Tracking**: Keep track of the taken pieces throughout the game (known issue currently; see below).
- **👓 Command-Line Promotion**: Reach the end of the board with your pawn? Use the command line to select your piece for promotion (UI for this feature is in progress!).

---

## ⚠️ Known Issues

- **📉 Captured Pieces Display**: Captured pieces are not displaying correctly due to a minor bug.
- **🔢 No On-Screen Prompts for Moves**: No UI prompts for piece selection; input moves directly via the command line.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/py-chess.git
```
### 2. Navigate to the Game Directory
```bash
cd py-chess
```
### 3. Install Dependencies (if any)
```bash
pip install -r requirements.txt
```
### 4. Start the Game
```bash
python main.py
```

## 📖 How to Play

- **Run the game** and follow on-screen instructions to start.
- **Select moves directly through the command line** by specifying piece coordinates.
- **Promote pawns via CLI**: If your pawn reaches the opposite side, you can choose its promotion by typing your choice into the CLI.

## 📖 Game Controls

- **Mouse**: Click to select pieces and move them on the board.
- **Undo Move**: Click the undo button or press `Z`.
- **Redo Move**: Click the redo button or press `X`.
- **New Game**: Click the new game button or press `R`.
- **Save Moves**: Press `S` to save your game’s move log to `saves/save.txt`.

## 📂 Assets and Dependencies

Ensure the following assets and libraries are present:

- **Assets**: The `images` and `assets` folders must contain necessary icons, piece images, and font files.

## 🤝 Contributing

We welcome contributions! 🎉 Fork the repository, make your improvements, and submit a pull request.

## 📜 License

This project is licensed under the **MIT License**—feel free to use, modify, and distribute it.

---

👑 Enjoy the game, and may the best strategist win! Whether honing your skills or diving into the game, the Python Chess Game awaits!
