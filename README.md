# AI-Chess-Game

## Description
An offline singleplayer chess game. Players can enter their name, select their color, and select which AI to play against.

## Required:
- Python 3.x
- pygame
- pygame-menu

## How it works
### Main Objects
- Piece = an abstract base class from which all board pieces are derived (King, Queen, Bishop, Knight, Rook, Pawn)
- Tile = a class which represents a single cell on the chess board; each tile may or may not contain a piece
- Board = a class which contains all game states necessary to ensure proper game functioning, and most importantly, it contains a tilemap atrribute which consists of all the tiles contained within the board

### Minimax AI
- Determines best move for the current turn by considering future game states resulting from a move
- The best move for a player is the move that maximizes their score and minimizes their opponent's score
- The 'score' of a resulting game state is calculated by considering the material scores for each player
- Uses alpha-beta pruning to minimize the number of board states that need to be analyzed, thus increasing the speed of the AI

### Random AI
- Randomly selects a move from its available valid moves

## Known Bugs
- No En passant rule for pawns
- AI moves too quickly which makes the timers unfair in a Human vs AI matchup
