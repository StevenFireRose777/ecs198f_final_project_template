import unittest
from pychess.logic.chess_logic import ChessLogic

class TestChessLogic(unittest.TestCase):
    def setUp(self):
        """Initialize a new ChessLogic object before each test."""
        self.game = ChessLogic()
    
    def test_pawn_promotion(self):
        """Test if a pawn promotes to a queen upon reaching the last rank."""
        self.game.board = [
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', 'P'],  # White pawn at h7
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['p', '', '', '', '', '', '', ''],  # Black pawn at a2
            ['', '', '', '', '', '', '', '']
        ]
        
        # Move white pawn from h7 to h8 (should promote)
        result = self.game.play_move("h7h8")
        self.assertEqual(self.game.board[0][7], 'Q')  # Pawn should become a Queen
        self.assertEqual(result, "h7h8=Q")
        
        # Move black pawn from a2 to a1 (should promote)
        result = self.game.play_move("a2a1")
        self.assertEqual(self.game.board[7][0], 'q')  # Pawn should become a Queen
        self.assertEqual(result, "a2a1=Q")
    
    def test_en_passant(self):
        """Test en passant capture."""
        self.game.board = [
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', 'p'],  # Black pawn at h5
            ['', '', '', '', '', '', '', ''],  
            ['', '', '', '', '', '', '', 'P'],  # White pawn at g5
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '']
        ]
        self.game.en_passant_target = (2, 7)  # Simulate h7-h5 move
        
        # White pawn captures en passant at h6
        result = self.game.play_move("g5h6")
        self.assertEqual(self.game.board[2][7], 'P')  # White pawn should be at h6
        self.assertEqual(self.game.board[3][7], '')   # Black pawn at h5 should be gone
        self.assertEqual(result, "gxh6")
    
    def test_checkmate(self):
        """Test a simple checkmate scenario (Fool's Mate)."""
        self.game.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', '', 'p', 'p', 'p'],  # f7 pawn moved
            ['', '', '', '', '', 'p', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        
        # Move white queen to h5
        self.game.play_move("d1h5")
        # Move black pawn to g5
        self.game.play_move("g7g5")
        # Move white queen to f7 (checkmate)
        result = self.game.play_move("h5f7")
        
        self.assertEqual(self.game.result, 'b')  # Black loses
        self.assertEqual(result, "Qxf7#")  # Queen checkmates

if __name__ == "__main__":
    unittest.main()