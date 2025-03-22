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

        result = self.game.play_move("h7h8")
        self.assertEqual(self.game.board[0][7], 'Q')
        self.assertEqual(result, "h7h8=Q")

        result = self.game.play_move("a2a1")
        self.assertEqual(self.game.board[7][0], 'q')
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

        result = self.game.play_move("g5h6")
        self.assertEqual(self.game.board[2][7], 'P')
        self.assertEqual(self.game.board[3][7], '')
        self.assertEqual(result, "gxh6")
    
    def test_checkmate(self):
        """Test a simple checkmate scenario (Fool’s Mate)."""
        self.game.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', '', 'p', 'p', 'p'],
            ['', '', '', '', '', 'p', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]

        self.game.play_move("d1h5")
        self.game.play_move("g7g5")
        result = self.game.play_move("h5f7")
        
        self.assertEqual(self.game.result, 'w')
        self.assertEqual(result, "Qh5xf7")

if __name__ == "__main__":
    unittest.main()