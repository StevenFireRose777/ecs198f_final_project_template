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
        self.result = ""  # Game status: "", "w", "b", or "d"
    
    def parse_move(self, move: str):
        """Converts move string (e.g., 'e2e4') to board indices."""
        start, end = move[:2], move[2:]
        return self.to_index(start), self.to_index(end)
    
    def to_index(self, pos: str):
        """Converts chess notation (e.g., 'e2') to board indices (row, col)."""
        col = ord(pos[0]) - ord('a')  # Convert 'a'-'h' to 0-7
        row = 8 - int(pos[1])  # Convert '1'-'8' to 7-0
        return row, col
    
    def play_move(self, move: str) -> str:
        """Handles making a move and returns extended chess notation."""
        (start_row, start_col), (end_row, end_col) = self.parse_move(move)
        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]
        
        if not piece:
            return ""  # No piece to move
        
        if piece.isupper() and target.isupper() or piece.islower() and target.islower():
            return ""  # Cannot capture own piece
        
        if not self.is_valid_move(piece, start_row, start_col, end_row, end_col):
            return ""
        
        # Move piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = ""
        
        # Check for special moves (capture, promotion, castling, en passant)
        notation = self.get_notation(piece, start_row, start_col, end_row, end_col, target)
        return notation
    
    def is_valid_move(self, piece, start_row, start_col, end_row, end_col):
        """Checks if the move follows the rules for the piece."""
        # TODO: Implement rules for each piece
        return True
    
    def get_notation(self, piece, start_row, start_col, end_row, end_col, target):
        """Generates extended chess notation."""
        move_notation = "" if piece.lower() == 'p' else piece.lower()
        if target:
            move_notation += "x"  # Capture notation
        move_notation += chr(start_col + ord('a')) + str(8 - start_row)
        move_notation += chr(end_col + ord('a')) + str(8 - end_row)
        return move_notation
