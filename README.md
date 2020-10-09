# ChessAI

## Description
A singleplayer chess game where players can enter their name, select their color, and play against an AI. To create visual representations the chess pieces, I drew each of them myself using pixelart.com.

## Required:
- Python 3.x
- pygame
- pygame-menu

## How it works
### Main Objects
- Piece = an abstract base class from which all board pieces are derived (King, Queen, Bishop, Knight, Rook, Pawn)
- Tile = a class which represents a single cell on the chess board; each tile may or may not contain a piece
- Board = a class which tracks all values necessary to ensure proper game functioning, and most importantly, it contains a tilemap atrribute which consists of all the tiles contained within the board

### Minimax AI
- Determines best move for the current turn by considering future game states resulting from a move
- The best move for a player is the move that maximizes their score and minimizes their opponent's score
- The 'score' of a resulting game state is calculated by considering the material scores for each player
- Uses alpha-beta pruning to minimize the number of board states that need to be analyzed, thus increasing the speed of the AI

### Random AI
- Randomly selects a move from its available valid moves

## How it looks
### Menu Screen
![Menu Screen](https://paste.pics/fb89c6ccc7b403a7c3d9bb9bbd18515b)
### Pregame Screen
![Pregame Screen](https://i.paste.pics/c3bebe6f37281c1e00ada487ba1bc32c.png)
### Game Screen
![Game Screen](https://i.paste.pics/3dbf11bbdd860606e20fd07158384d1f.png)
### End Screen
![End Screen](https://i.paste.pics/3988638a886560139ea1e6a74cf0d4fd.png)

## Known Bugs
- No En passant rule for pawns
- No castling
- Rare crash when determining move for AI
