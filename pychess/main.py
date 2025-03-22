
from chess_logic import ChessLogic

def main():
    game = ChessLogic()
    print("Initial Board:")
    for row in game.board:
        print(' '.join(row))

if __name__ == "__main__":
    main()
