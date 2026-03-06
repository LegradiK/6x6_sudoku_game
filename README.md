# 6x6 Sudoku

A desktop 6x6 Sudoku puzzle game built with Python and Pygame.

## Features

- 6×6 Sudoku grid with 2×3 box regions
- Puzzle generation via a local REST API (Docker-based)
- Real-time wrong-answer highlighting in red
- New Game and Restart buttons
- Solution validation on submit

## Requirements

- Python 3.x
- `pygame` library
- `requests` library
- Docker (for the puzzle generator service)

Install Python dependencies:

```bash
pip install pygame requests
```

A virtual environment is optional but recommended to keep dependencies isolated:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pygame requests
```

## Running the Sudoku Generator

The game fetches puzzles from a local Docker service. Start it before launching the game:

```bash
docker run -p 8080:80 jotools/sudoku
```

The API is expected at `http://localhost:8080/api/sudoku/generate`.

## Running the Game

```bash
python main.py
```

## How to Play

| Action | Key / Input |
|---|---|
| Move selection | Arrow keys |
| Enter a number | Keys `1` – `6` |
| Erase a cell | `Backspace`, `Delete`, `e`, or `d` |
| Submit your answer | `Enter` |
| Start a new puzzle | Click **New Game** |
| Reset the current puzzle | Click **Restart** |

Cells with wrong values are highlighted in **red**. When you press Enter:

- If any cells are empty, a "Fill all cells" warning is shown.
- If there are incorrect values, a "Wrong answers" warning is shown.
- If the puzzle is fully and correctly solved, "PUZZLE SOLVED!" is displayed in green.

## Project Structure

```
├── .gitignore
├── README.md
├── main.py       # Game loop, input handling, puzzle loading
├── ui.py         # Drawing functions and GameState class
└── button.py     # Button component
```
