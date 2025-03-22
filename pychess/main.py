
from chess_logic import ChessLogic

def main():
    chess_game = ChessLogic()
    print("Initial Board:")
    for row in chess_game.chess_board:
        print(' '.join(row))

if __name__ == "__main__":
    main()
