import unittest
from chess_logic import ChessLogic

class TestChessLogic(unittest.TestCase):
    def setUp(self):
        self.game = ChessLogic()

    def test_pawn_move(self):
        result = self.game.play_move("e2e4")
        self.assertEqual(result, "e2e4", "Failed: Incorrect Extended Chess Notation for e2e4")
        result = self.game.play_move("e7e5")
        self.assertEqual(result, "e7e5", "Failed: Incorrect Extended Chess Notation for e7e5")
    
    def test_invalid_move(self):
        result = self.game.play_move("e2e5")
        self.assertEqual(result, "Invalid move", "Failed: Invalid move did not return expected message")
    
    def test_checkmate(self):
        self.game.play_move("f2f3")
        self.game.play_move("e7e5")
        self.game.play_move("g2g4")
        result = self.game.play_move("d8h4")
        self.assertEqual(result, "d8h4", "Failed: Incorrect Extended Chess Notation for checkmate move")
        self.assertEqual(self.game.result, "w", "Failed: White should be in checkmate")
 
if __name__ == "__main__":
    unittest.main()