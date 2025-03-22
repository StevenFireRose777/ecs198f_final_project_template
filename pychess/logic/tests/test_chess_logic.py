import unittest
from chess_logic import ChessLogic

class TestChessLogic(unittest.TestCase):
    def test_pawn_move(self):
        game = ChessLogic()
        self.assertEqual(game.play_move("e2e4"), "Move played")
        self.assertEqual(game.play_move("e7e5"), "Move played")
    
    def test_invalid_move(self):
        game = ChessLogic()
        self.assertEqual(game.play_move("e2e5"), "")  # Invalid pawn move
    
    def test_checkmate(self):
        game = ChessLogic()
        game.play_move("f2f3")
        game.play_move("e7e5")
        game.play_move("g2g4")
        self.assertEqual(game.play_move("d8h4"), "Move played")
        self.assertEqual(game.result, "w")  # White is checkmated
 
if __name__ == "__main__":
    unittest.main()
