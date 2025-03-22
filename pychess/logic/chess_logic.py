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
        self.en_passant_target = None  # Track en passant position
    
    def parse_move(self, move: str):
        start, end = move[:2], move[2:]
        return self.to_index(start), self.to_index(end)
    
    def to_index(self, pos: str):
        col = ord(pos[0]) - ord('a')
        row = 8 - int(pos[1])
        return row, col
    
    def play_move(self, move: str) -> str:
        (start_row, start_col), (end_row, end_col) = self.parse_move(move)
        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]
        
        if not piece or (piece.isupper() and target.isupper()) or (piece.islower() and target.islower()):
            return ""
        
        if not self.is_valid_move(piece, start_row, start_col, end_row, end_col):
            return ""
        
        # En passant capture
        if piece.lower() == "p" and abs(start_col - end_col) == 1 and target == "" and (end_row, end_col) == self.en_passant_target:
            self.board[start_row][end_col] = ""
        
        # Move piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = ""
        
        # Handle pawn promotion
        if piece.lower() == "p" and (end_row == 0 or end_row == 7):
            self.board[end_row][end_col] = "Q" if piece.isupper() else "q"
            return f"{chr(start_col + ord('a'))}{8 - start_row}{chr(end_col + ord('a'))}{8 - end_row}=Q"
        
        # Check for checkmate
        opponent = "b" if piece.isupper() else "w"
        if self.is_checkmate(opponent):
            self.result = opponent
        
        return self.get_notation(piece, start_row, start_col, end_row, end_col, target)
    
    def is_valid_move(self, piece, start_row, start_col, end_row, end_col):
        if piece.lower() == "p":
            direction = -1 if piece.isupper() else 1
            start_rank = 6 if piece.isupper() else 1
            if start_col == end_col and self.board[end_row][end_col] == "":
                if end_row == start_row + direction:
                    return True
                if start_row == start_rank and end_row == start_row + 2 * direction and self.board[start_row + direction][start_col] == "":
                    return True
            if abs(end_col - start_col) == 1 and end_row == start_row + direction and self.board[end_row][end_col] != "":
                return True
        return False
    
    def find_king(self, color):
        king = "K" if color == "w" else "k"
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    return (row, col)
        return None
    
    def is_king_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        opponent_color = "b" if color == "w" else "w"
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and (piece.isupper() if opponent_color == "w" else piece.islower()):
                    if self.is_valid_move(piece, row, col, king_pos[0], king_pos[1]):
                        return True
        return False
    
    def is_checkmate(self, color):
        if not self.is_king_in_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and (piece.isupper() if color == "w" else piece.islower()):
                    for r in range(8):
                        for c in range(8):
                            if self.is_valid_move(piece, row, col, r, c):
                                original_piece = self.board[r][c]
                                self.board[r][c] = piece
                                self.board[row][col] = ""
                                still_in_check = self.is_king_in_check(color)
                                self.board[row][col] = piece
                                self.board[r][c] = original_piece
                                if not still_in_check:
                                    return False
        return True
