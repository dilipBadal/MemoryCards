# 🧠 Memory Matching Game

A Memory Matching Game built in **Python** with both a **Pygame GUI** and a **Terminal (CLI)** version.

The objective is simple: match all 8 pairs of cards in the fewest number of moves.

---

# Features

- 🎮 Two playable versions
  - **Pygame GUI** (`game.py`)
  - **Terminal CLI** (`cli_game.py`)

- 4×4 board containing 16 hidden cards
- 8 randomized matching pairs (A-H)
- Move counter
- Reset game at any time
- Auto Solver
- Input validation
- Sound effects (GUI)
- Win screen with replay options

---

# Game Description

The game begins with **16 face-down cards** arranged in a **4×4 grid**.

Each card contains a hidden letter from **A** to **H**, with every letter appearing exactly **twice**.

The player reveals two cards each turn.

- If the cards match, they remain visible.
- If they do not match, they flip back over.
- The objective is to match every pair using the fewest possible moves.

---

# Players

This is a **Human vs Computer** game.

### Human Player

- Selects cards.
- Tries to remember previously revealed cards.
- Matches every pair.

### Computer

- Randomly shuffles the cards.
- Validates every move.
- Tracks matched cards and move count.
- Provides an Auto Solver when requested.

---

# Rules

1. The board starts with 16 hidden cards.
2. Every letter appears exactly twice.
3. The player selects two different unmatched cards.
4. Matching cards remain face up.
5. Non-matching cards are hidden again.
6. One move is counted after selecting the second card.
7. The game ends once all 8 pairs have been matched.
8. The game may be reset at any time.

---

# Controls

## Pygame Version

Run:

```bash
python3 game.py
```

### Menu

- Classic Mode
- Input Mode
- Quit

### Keyboard Shortcuts

| Key     | Action         |
| ------- | -------------- |
| **S**   | Auto Solver    |
| **R**   | Reset Game     |
| **ESC** | Return to Menu |

---

## Terminal Version

Run:

```bash
python3 cli_game.py
```

### Commands

| Command  | Action      |
| -------- | ----------- |
| `1`-`16` | Select card |
| `s`      | Auto Solver |
| `r`      | Reset       |
| `q`      | Quit        |

---

# Game Flow

1. Start the game.
2. Shuffle 8 pairs into 16 positions.
3. Display the main menu.
4. Select a game mode.
5. Display the board.
6. Select the first card.
7. Select the second card.
8. Check if the cards match.
9. If they match, keep them revealed.
10. Otherwise, hide both cards again.
11. Check whether all cards are matched.
12. If every pair has been found, display the win screen.
13. Otherwise, continue playing.

---

# Project Structure

```
MemoryCards/
│
├── game.py                 # Main Pygame application
├── cli_game.py             # Terminal version
├── memory_logic.py         # Game logic and solver
├── memory_constants.py     # Colors, sizes, fonts and constants
├── memory_sound.py         # Sound effects and playback
├── memory_ui.py            # UI drawing functions
├── test_memory_logic.py    # Unit tests
├── requirements.txt
├── README.md
```

---

# Manual Test Cases

## Test 1: Normal Gameplay

**Steps**

- Start `game.py`
- Choose Classic Mode
- Match every pair

**Expected Result**

- Moves are counted correctly.
- Win screen appears after matching all pairs.

---

## Test 2: Reset Game

**Steps**

- Start a game.
- Reveal several cards.
- Press **R**.

**Expected Result**

- Board reshuffles.
- Move counter resets to 0.

---

## Test 3: Menu Navigation

**Steps**

- Start any game mode.
- Press **ESC**.

**Expected Result**

- Returns to the main menu.

---

## Test 4: Invalid Input

**Steps**

In Input Mode enter:

- `0`
- `17`
- Non-numeric input

**Expected Result**

- Invalid input is rejected.
- User is prompted to enter a valid card number.

---

## Test 5: Same Card Selection

**Steps**

Select the same card twice.

**Expected Result**

- Move is rejected.
- User is asked to choose a different card.

---

## Test 6: Already Matched Card

**Steps**

- Match a pair.
- Attempt to select one of those cards again.

**Expected Result**

- Selection is rejected.

---

## Test 7: Auto Solver

**Steps**

Press **S** during gameplay.

**Expected Result**

- The computer selects valid cards automatically.
- Game continues normally.

---

## Test 8: End Game

**Steps**

Match all 8 pairs.

**Expected Result**

- Win screen appears.
- Player can restart or return to the menu.

---

# Automated Tests

## Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

## Run Tests

```bash
python3 -m unittest
```

The automated tests verify:

- Board always contains 16 cards.
- Board always contains exactly 8 matching pairs.
- Reset produces a fresh game state.
- Auto Solver correctly finds known pairs.
- Auto Solver stops when fewer than two unmatched cards remain.
- Terminal log maintains only the most recent visible entries.

---

# GitHub Repository

https://github.com/dilipBadal/MemoryCards

---

# Technologies Used

- Python 3
- Pygame
- unittest

---

# Author

**Dilip Badal**
**Sudheer**
