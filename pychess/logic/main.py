
from chess_logic import ChessLogic
from .utils import array2grid, grid2array
from .pieces import *

def main():
    chess_game = ChessLogic()
    print("Initial Board:")
    for row in chess_game.chess_board:
        print(' '.join(row))

if __name__ == "__main__":
    main()
