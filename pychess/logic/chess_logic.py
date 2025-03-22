class ChessLogic:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        self.result = ""
        self.en_passant_target = None
        self.current_turn = "w"

    def parse_move(self, move: str):
        try:
            start, end = move[:2], move[2:]
            return self.to_index(start), self.to_index(end)
        except Exception as e:
            print(f"Error parsing move {move}: {e}")
            return None, None
    
    def to_index(self, pos: str):
        try:
            col = ord(pos[0]) - ord('a')
            row = 8 - int(pos[1])
            return row, col
        except Exception as e:
            print(f"Invalid position {pos}: {e}")
            return -1, -1

    def play_move(self, move: str) -> str:
        try:
            (start_row, start_col), (end_row, end_col) = self.parse_move(move)
            if start_row == -1 or end_row == -1:
                return "Invalid move"

            piece = self.board[start_row][start_col]
            target = self.board[end_row][end_col]

            if not piece or (piece.isupper() and target.isupper()) or (piece.islower() and target.islower()):
                return "Invalid move"

            if (self.current_turn == "w" and not piece.isupper()) or (self.current_turn == "b" and not piece.islower()):
                return "Not your turn"

            if not self.is_valid_move(piece, start_row, start_col, end_row, end_col):
                return "Illegal move"

            # Handle en passant
            if piece.lower() == 'p' and end_col != start_col and target == "" and self.en_passant_target == (end_row, end_col):
                self.board[start_row][end_col] = ""

            # Perform move
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = ""

            # Handle pawn promotion
            if piece.lower() == 'p' and (end_row == 0 or end_row == 7):
                self.board[end_row][end_col] = 'Q' if piece.isupper() else 'q'

            # Update en passant target
            self.en_passant_target = None
            if piece.lower() == 'p' and abs(start_row - end_row) == 2:
                self.en_passant_target = ((start_row + end_row) // 2, start_col)

            # Update turns
            self.current_turn = "b" if self.current_turn == "w" else "w"

            # Check for checkmate
            opponent = "b" if piece.isupper() else "w"
            if self.is_checkmate(opponent):
                self.result = opponent

            return f"{chr(start_col + 97)}{8 - start_row}{chr(end_col + 97)}{8 - end_row}"
        
        except Exception as e:
            print(f"Error during move {move}: {e}")
            return "Error encountered"

    def is_valid_move(self, piece, start_row, start_col, end_row, end_col):
        if piece.lower() == "p":
            direction = -1 if piece.isupper() else 1
            start_rank = 6 if piece.isupper() else 1
            if start_col == end_col and self.board[end_row][end_col] == "":
                if end_row == start_row + direction:
                    return True
                if start_row == start_rank and end_row == start_row + 2 * direction and self.board[start_row + direction][start_col] == "":
                    return True
            if abs(end_col - start_col) == 1 and end_row == start_row + direction and (self.board[end_row][end_col] != "" or self.en_passant_target == (end_row, end_col)):
                return True
        elif piece.lower() == "r":
            return self.is_valid_rook_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == "b":
            return self.is_valid_bishop_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == "q":
            return self.is_valid_queen_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == "n":
            return self.is_valid_knight_move(start_row, start_col, end_row, end_col)
        elif piece.lower() == "k":
            return self.is_valid_king_move(start_row, start_col, end_row, end_col)
        return False
