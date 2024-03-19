# Connect-4
Connect-4 is a classic two-player connection board game implemented in Python with PyGame.

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)  
- [Rules](#rules)
- [AI Player](#ai-player)
- [Code Structure](#code-structure)
- [Future Improvements](#future-improvements)

## About

Players take turns dropping colored discs into a 7x6 vertically suspended grid, attempting to connect 4 of their discs in a row horizontally, vertically, or diagonally.

### Features:

- Player vs Player mode
- Player vs AI mode with Minimax algorithm
- Colorful grid graphics using PyGame
- Play with any grid size

## Getting Started

### Prerequisites

- Python 3
- PyGame 


## Usage

Run `python main.py` to launch the game.

Select game mode 0 for Player vs Player or 1 for Player vs AI. 

Use the mouse to select a column to drop your disc. Take alternating turns with the opponent trying to connect 4 in a row to win.

## Rules

- Players take turns dropping their colored discs into the columns.
- The discs fall to the lowest available space in the column. 
- The first player to connect 4 discs horizontally, vertically or diagonally wins.
- If the board fills up before either player connects 4, the game is a draw.

## AI Player 

The AI player uses the Minimax algorithm to calculate the optimal move. It evaluates future game states up to a fixed depth and chooses the move that maximizes its chances of winning.

The evaluation function calculates a score for the board based on:

- Number of 4, 3, and 2 in a rows
- Blocking the opponent from getting 3 in a row
- Controlling the center column

## Code Structure

- `Board` handles the game state
- `View` renders the graphics 
- `GameManager` contains game logic
- `Minimax` implements the AI algorithm
- `Heuristic` evaluates board scores

The code is structured into classes with distinct responsibilities. PyGame is used for graphics, mouse input, and sound effects.

## Future Improvements

- Network multiplayer
- Animated transitions between turns 
- Selectable AI difficulty levels
- Improved heuristic evaluation function
