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
    
    def is_valid_move(self, piece, start_row, start_col, end_row, end_col):
        """Check if the move is valid based on piece movement rules."""
        piece_type = piece.lower()
        
        # Basic movement validation
        if start_row == end_row and start_col == end_col:
            return False  # Can't move to the same position
        
        # Check if the path is clear for applicable pieces
        if piece_type in 'rqb' and not self.is_path_clear(start_row, start_col, end_row, end_col):
            return False
        
        if piece_type == 'p':  # Pawn
            return self.is_valid_pawn_move(piece, start_row, start_col, end_row, end_col)
        elif piece_type == 'r':  # Rook
            return start_row == end_row or start_col == end_col
        elif piece_type == 'n':  # Knight
            return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
                  (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)
        elif piece_type == 'b':  # Bishop
            return abs(start_row - end_row) == abs(start_col - end_col)
        elif piece_type == 'q':  # Queen
            return start_row == end_row or start_col == end_col or \
                  abs(start_row - end_row) == abs(start_col - end_col)
        elif piece_type == 'k':  # King
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1
        
        return False
    
    def is_valid_pawn_move(self, piece, start_row, start_col, end_row, end_col):
        """Validate pawn movement."""
        is_white = piece.isupper()
        direction = -1 if is_white else 1  # White pawns move up (-1 in row), black pawns move down (+1 in row)
        
        # Regular move forward
        if start_col == end_col and self.board[end_row][end_col] == '':
            # Single square forward
            if end_row == start_row + direction:
                return True
            
            # Double square forward from starting position
            if (is_white and start_row == 6 and end_row == 4) or \
               (not is_white and start_row == 1 and end_row == 3):
                return self.board[start_row + direction][start_col] == ''
        
        # Capture (including en passant)
        if end_row == start_row + direction and abs(end_col - start_col) == 1:
            # Normal capture
            if self.board[end_row][end_col] != '' and \
               (self.board[end_row][end_col].isupper() != is_white):
                return True
            
            # En passant capture
            if (end_row, end_col) == self.en_passant_target:
                return True
        
        return False
    
    def is_path_clear(self, start_row, start_col, end_row, end_col):
        """Check if the path between start and end positions is clear."""
        row_step = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        col_step = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        
        row, col = start_row + row_step, start_col + col_step
        while (row, col) != (end_row, end_col):
            if self.board[row][col] != '':
                return False
            row += row_step
            col += col_step
        
        return True
    
    def get_notation(self, piece, start_row, start_col, end_row, end_col, target):
        """Generate algebraic chess notation for the move."""
        piece_type = piece.lower()
        piece_symbol = piece_type.upper() if piece_type != 'p' else ''
        
        # Convert board indices to chess notation
        start_pos = f"{chr(start_col + ord('a'))}{8 - start_row}"
        end_pos = f"{chr(end_col + ord('a'))}{8 - end_row}"
        
        # Check for capture
        capture = 'x' if target != '' or (piece_type == 'p' and start_col != end_col) else ''
        
        # For pawns capturing, include the file
        if piece_type == 'p' and capture:
            notation = f"{start_pos[0]}{capture}{end_pos}"
        else:
            notation = f"{piece_symbol}{capture}{end_pos}" if capture else f"{piece_symbol}{end_pos}"
        
        # Check for pawn promotion
        if piece_type == 'p' and (end_row == 0 or end_row == 7):
            notation += "=Q"
        
        # Check for check or checkmate
        opponent_color = "b" if piece.isupper() else "w"
        if self.is_checkmate(opponent_color):
            notation += "#"  # Checkmate
        elif self.is_king_in_check(opponent_color):
            notation += "+"  # Check
        
        return notation
    
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
            # In en passant, the captured pawn is on the same row as the attacking pawn
            self.board[start_row][end_col] = ""
        
        # Move piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = ""
        
        # Handle pawn promotion
        if piece.lower() == "p" and (end_row == 0 or end_row == 7):
            promotion_piece = "Q" if piece.isupper() else "q"
            self.board[end_row][end_col] = promotion_piece
        
        # Set en passant target for double pawn move
        self.en_passant_target = None
        if piece.lower() == "p" and abs(start_row - end_row) == 2:
            mid_row = (start_row + end_row) // 2
            self.en_passant_target = (mid_row, end_col)
        
        # Check for checkmate
        opponent_color = "b" if piece.isupper() else "w"
        if self.is_checkmate(opponent_color):
            self.result = opponent_color
        
        return self.get_notation(piece, start_row, start_col, end_row, end_col, target)
    
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