
from .utils import array2grid, grid2array
from .pieces import *


from typing import List
from typing import Tuple  


class ChessLogic:
      
 
    def __init__(self):
        """
        Initalize the ChessLogic Object. External fields are chess_board and game_result

        chess_board -> Two Dimensional List of string Representing the Current State of the Board
            P, R, N, B, Q, K - White Pieces

            p, r, n, b, q, k - Black Pieces

            '' - Empty Square

        game_result -> The current game_result of the chess_game
            w - White Win

            b - Black Win

            d - Draw

            '' - Game In Progress
        """
        self.chess_board = [
			['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
			['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
			['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
		]
        self.game_result = "" 
        self.last_move = None
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_left_rook_moved = False
        self.white_right_rook_moved = False
        self.black_left_rook_moved = False
        self.black_right_rook_moved = False
        self.check_order = True
        self.side = "w"
        
        
        
        
        
    # given the array index, print the grid string    
    def array2grid(self, row: int, col: int) -> str:
        if(col<0 or col>7 or row<0 or row>7):
            return str(-1)
        return chr(col + ord('a')) + str(8 - row)
        
    # given the grid string, get the array index
    def grid2array(self, position: str) -> Tuple[int, int]:
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        if(col<0 or col>7 or row<0 or row>7):
            return (-1,-1)
        return (row, col)
        
    # get the name of the chess_piece based on given position in the grid
    def get_piece(self, position: str) -> str:
        
        row, column = self.grid2array(position)
        
        return self.chess_board[row][column]
    
    def get_white_pawn_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        
        # Implement logic for white pawn
        # if this is its first move, it can move 1 or 2    
        front_position = self.array2grid(row-1, column)
        # if the chess_piece is not at the top row
        if(front_position != "-1"):
            piece_at_front = self.get_piece(front_position)
            # if no chess_piece at front
            if(piece_at_front == ''):
                valid_move_list.append(front_position)
                # can move twice
                if(row == 6): 
                    double_front_position = self.array2grid(row-2, column)
                    if double_front_position != "-1":
                        valid_move_list.append(double_front_position)
        # now check diagonally left and right
        left_diagonal_position = self.array2grid(row-1, column-1)
        if left_diagonal_position != "-1" and self.get_piece(left_diagonal_position).islower():
            valid_move_list.append(left_diagonal_position)
        right_diagonal_position = self.array2grid(row-1, column+1)
        if right_diagonal_position != "-1" and self.get_piece(right_diagonal_position).islower():
            valid_move_list.append(right_diagonal_position)
            
            
        if self.last_move != None:
            last_piece, last_start_pos, last_end_pos = self.last_move
            if chess_piece == 'P' and last_piece == 'p':
                # if I'm white pawn and last move is black pawn
                # I want to check
                # 1. Does the last pawn move twice ahead?
                # 2. Am I at the correct position
                # with both is true, do I want to move at the correct position?
                # If I do want to move at the correct position, then eat it
                if abs(int(last_start_pos[1]) - int(last_end_pos[1])) == 2:
                    if position[1] == "5":
                        valid_move_list.append(last_end_pos[0] + str(int(last_end_pos[1]) + 1))
        
        return valid_move_list

    def get_black_pawn_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        # Implement logic for black pawn
        # if this is its first move, it can move 1 or 2    
        front_position = self.array2grid(row+1, column)
        # if the chess_piece is not at the top row
        if(front_position != "-1"):
            piece_at_front = self.get_piece(front_position)
            # if no chess_piece at front
            if(piece_at_front == ''):
                valid_move_list.append(front_position)
                # can move twice
                if(row == 1): 
                    double_front_position = self.array2grid(row+2, column)
                    if double_front_position != "-1":
                        valid_move_list.append(double_front_position)
        # now check diagonally left and right
        left_diagonal_position = self.array2grid(row+1, column-1)
        if left_diagonal_position != "-1" and self.get_piece(left_diagonal_position).isupper():
            valid_move_list.append(left_diagonal_position)
        right_diagonal_position = self.array2grid(row+1, column+1)
        if right_diagonal_position != "-1" and self.get_piece(right_diagonal_position).isupper():
            valid_move_list.append(right_diagonal_position)
        
        if self.last_move != None:
            last_piece, last_start_pos, last_end_pos = self.last_move
            if chess_piece == 'p' and last_piece == 'P':
                if abs(int(last_start_pos[1]) - int(last_end_pos[1])) == 2:
                    if position[1] == "4":
                        valid_move_list.append(last_end_pos[0] + str(int(last_end_pos[1]) - 1))
        return valid_move_list

    def get_white_rook_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        
        # Implement logic for white rook
        for i in range(row-1, -1, -1):
            pos_up = self.array2grid(i, column)
            piece_up = self.get_piece(pos_up)
            if piece_up == '':
                valid_move_list.append(pos_up)
            elif piece_up.islower():
                valid_move_list.append(pos_up)
                break
            else:
                break
        for j in range(row+1, 8):
            pos_down = self.array2grid(j, column)
            piece_down = self.get_piece(pos_down)
            if piece_down == '':
                valid_move_list.append(pos_down)
            elif piece_down.islower():
                valid_move_list.append(pos_down)
                break
            else:
                break
        for k in range(column-1, -1, -1):
            pos_left = self.array2grid(row, k)
            piece_left = self.get_piece(pos_left)
            if piece_left == '':
                valid_move_list.append(pos_left)
            elif piece_left.islower():
                valid_move_list.append(pos_left)
                break
            else:
                break
        for l in range(column+1, 8):
            pos_right = self.array2grid(row, l)
            piece_right = self.get_piece(pos_right)
            if piece_right == '':
                valid_move_list.append(pos_right)
            elif piece_right.islower():
                valid_move_list.append(pos_right)
                break
            else:
                break
        return valid_move_list
    
    def get_black_rook_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        
        # Implement logic for black rook
        for i in range(row-1, -1, -1):
            pos_up = self.array2grid(i, column)
            piece_up = self.get_piece(pos_up)
            if piece_up == '':
                valid_move_list.append(pos_up)
            elif piece_up.isupper():
                valid_move_list.append(pos_up)
                break
            else:
                break
        for j in range(row+1, 8):
            pos_down = self.array2grid(j, column)
            piece_down = self.get_piece(pos_down)
            if piece_down == '':
                valid_move_list.append(pos_down)
            elif piece_down.isupper():
                valid_move_list.append(pos_down)
                break
            else:
                break
        for k in range(column-1, -1, -1):
            pos_left = self.array2grid(row, k)
            piece_left = self.get_piece(pos_left)
            if piece_left == '':
                valid_move_list.append(pos_left)
            elif piece_left.isupper():
                valid_move_list.append(pos_left)
                break
            else:
                break
        for l in range(column+1, 8):
            pos_right = self.array2grid(row, l)
            piece_right = self.get_piece(pos_right)
            if piece_right == '':
                valid_move_list.append(pos_right)
            elif piece_right.isupper():
                valid_move_list.append(pos_right)
                break
            else:
                break   
        return valid_move_list

    def get_white_knight_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        
        # Implement logic for white knight
        knight_moves = [
        (row - 2, column - 1),
        (row - 2, column + 1),
        (row - 1, column + 2),
        (row + 1, column + 2),
        (row + 2, column + 1),
        (row + 2, column - 1),
        (row + 1, column - 2),
        (row - 1, column - 2)
        ]
        for move in knight_moves:
            new_pos = self.array2grid(move[0], move[1])
            if new_pos != "-1" and (self.get_piece(new_pos) == "" or self.get_piece(new_pos).islower()):
                valid_move_list.append(new_pos)
                
        return valid_move_list
    
    def get_black_knight_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        # Implement logic for black knight
        knight_moves = [
            (row - 2, column - 1),
            (row - 2, column + 1),
            (row - 1, column + 2),
            (row + 1, column + 2),
            (row + 2, column + 1),
            (row + 2, column - 1),
            (row + 1, column - 2),
            (row - 1, column - 2)
        ]
        for move in knight_moves:
            new_pos = self.array2grid(move[0], move[1])
            if new_pos != "-1" and (self.get_piece(new_pos) == "" or self.get_piece(new_pos).isupper()):
                valid_move_list.append(new_pos)
        return valid_move_list


    def get_white_bishop_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        
        for i in range(1, 8):
            pos_up_right = self.array2grid(row - i, column + i)
            if pos_up_right == "-1":
                break
            piece_up_right = self.get_piece(pos_up_right)
            if piece_up_right == '':
                valid_move_list.append(pos_up_right)
            elif piece_up_right.islower():
                valid_move_list.append(pos_up_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_up_left = self.array2grid(row - i, column - i)
            if pos_up_left == "-1":
                break
            piece_up_left = self.get_piece(pos_up_left)
            if piece_up_left == '':
                valid_move_list.append(pos_up_left)
            elif piece_up_left.islower():
                valid_move_list.append(pos_up_left)
                break
            else:
                break
        for i in range(1, 8):
            pos_down_right = self.array2grid(row + i, column + i)
            if pos_down_right == "-1":
                break
            piece_down_right = self.get_piece(pos_down_right)
            if piece_down_right == '':
                valid_move_list.append(pos_down_right)
            elif piece_down_right.islower():
                valid_move_list.append(pos_down_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_down_left = self.array2grid(row + i, column - i)
            if pos_down_left == "-1":
                break
            piece_down_left = self.get_piece(pos_down_left)
            if piece_down_left == '':
                valid_move_list.append(pos_down_left)
            elif piece_down_left.islower():
                valid_move_list.append(pos_down_left)
                break
            else:
                break
            
        return valid_move_list   
    
    def get_black_bishop_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        # Implement logic for black bishop
        for i in range(1, 8):
            pos_up_right = self.array2grid(row - i, column + i)
            if pos_up_right == "-1":
                break
            piece_up_right = self.get_piece(pos_up_right)
            if piece_up_right == '':
                valid_move_list.append(pos_up_right)
            elif piece_up_right.isupper():
                valid_move_list.append(pos_up_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_up_left = self.array2grid(row - i, column - i)
            if pos_up_left == "-1":
                break
            piece_up_left = self.get_piece(pos_up_left)
            if piece_up_left == '':
                valid_move_list.append(pos_up_left)
            elif piece_up_left.isupper():
                valid_move_list.append(pos_up_left)
                break
            else:
                break
        for i in range(1, 8):
            pos_down_right = self.array2grid(row + i, column + i)
            if pos_down_right == "-1":
                break
            piece_down_right = self.get_piece(pos_down_right)
            if piece_down_right == '':
                valid_move_list.append(pos_down_right)
            elif piece_down_right.isupper():
                valid_move_list.append(pos_down_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_down_left = self.array2grid(row + i, column - i)
            if pos_down_left == "-1":
                break
            piece_down_left = self.get_piece(pos_down_left)
            if piece_down_left == '':
                valid_move_list.append(pos_down_left)
            elif piece_down_left.isupper():
                valid_move_list.append(pos_down_left)
                break
            else:
                break
        return valid_move_list

    def get_white_queen_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        # Implement logic for white queen
        for i in range(row-1, -1, -1):
            pos_up = self.array2grid(i, column)
            piece_up = self.get_piece(pos_up)
            if piece_up == '':
                valid_move_list.append(pos_up)
            elif piece_up.islower():
                valid_move_list.append(pos_up)
                break
            else:
                break
        for j in range(row+1, 8):
            pos_down = self.array2grid(j, column)
            piece_down = self.get_piece(pos_down)
            if piece_down == '':
                valid_move_list.append(pos_down)
            elif piece_down.islower():
                valid_move_list.append(pos_down)
                break
            else:
                break
        for k in range(column-1, -1, -1):
            pos_left = self.array2grid(row, k)
            piece_left = self.get_piece(pos_left)
            if piece_left == '':
                valid_move_list.append(pos_left)
            elif piece_left.islower():
                valid_move_list.append(pos_left)
                break
            else:
                break
        for l in range(column+1, 8):
            pos_right = self.array2grid(row, l)
            piece_right = self.get_piece(pos_right)
            if piece_right == '':
                valid_move_list.append(pos_right)
            elif piece_right.islower():
                valid_move_list.append(pos_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_up_right = self.array2grid(row - i, column + i)
            if pos_up_right == "-1":
                break
            piece_up_right = self.get_piece(pos_up_right)
            if piece_up_right == '':
                valid_move_list.append(pos_up_right)
            elif piece_up_right.islower():
                valid_move_list.append(pos_up_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_up_left = self.array2grid(row - i, column - i)
            if pos_up_left == "-1":
                break
            piece_up_left = self.get_piece(pos_up_left)
            if piece_up_left == '':
                valid_move_list.append(pos_up_left)
            elif piece_up_left.islower():
                valid_move_list.append(pos_up_left)
                break
            else:
                break
        for i in range(1, 8):
            pos_down_right = self.array2grid(row + i, column + i)
            if pos_down_right == "-1":
                break
            piece_down_right = self.get_piece(pos_down_right)
            if piece_down_right == '':
                valid_move_list.append(pos_down_right)
            elif piece_down_right.islower():
                valid_move_list.append(pos_down_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_down_left = self.array2grid(row + i, column - i)
            if pos_down_left == "-1":
                break
            piece_down_left = self.get_piece(pos_down_left)
            if piece_down_left == '':
                valid_move_list.append(pos_down_left)
            elif piece_down_left.islower():
                valid_move_list.append(pos_down_left)
                break
            else:
                break
        return valid_move_list
    
    def get_black_queen_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        # Implement logic for black queen
        for i in range(row-1, -1, -1):
            pos_up = self.array2grid(i, column)
            piece_up = self.get_piece(pos_up)
            if piece_up == '':
                valid_move_list.append(pos_up)
            elif piece_up.isupper():
                valid_move_list.append(pos_up)
                break
            else:
                break
        for j in range(row+1, 8):
            pos_down = self.array2grid(j, column)
            piece_down = self.get_piece(pos_down)
            if piece_down == '':
                valid_move_list.append(pos_down)
            elif piece_down.isupper():
                valid_move_list.append(pos_down)
                break
            else:
                break
        for k in range(column-1, -1, -1):
            pos_left = self.array2grid(row, k)
            piece_left = self.get_piece(pos_left)
            if piece_left == '':
                valid_move_list.append(pos_left)
            elif piece_left.isupper():
                valid_move_list.append(pos_left)
                break
            else:
                break
        for l in range(column+1, 8):
            pos_right = self.array2grid(row, l)
            piece_right = self.get_piece(pos_right)
            if piece_right == '':
                valid_move_list.append(pos_right)
            elif piece_right.isupper():
                valid_move_list.append(pos_right)
                break
            else:
                break   
        for i in range(1, 8):
            pos_up_right = self.array2grid(row - i, column + i)
            if pos_up_right == "-1":
                break
            piece_up_right = self.get_piece(pos_up_right)
            if piece_up_right == '':
                valid_move_list.append(pos_up_right)
            elif piece_up_right.isupper():
                valid_move_list.append(pos_up_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_up_left = self.array2grid(row - i, column - i)
            if pos_up_left == "-1":
                break
            piece_up_left = self.get_piece(pos_up_left)
            if piece_up_left == '':
                valid_move_list.append(pos_up_left)
            elif piece_up_left.isupper():
                valid_move_list.append(pos_up_left)
                break
            else:
                break
        for i in range(1, 8):
            pos_down_right = self.array2grid(row + i, column + i)
            if pos_down_right == "-1":
                break
            piece_down_right = self.get_piece(pos_down_right)
            if piece_down_right == '':
                valid_move_list.append(pos_down_right)
            elif piece_down_right.isupper():
                valid_move_list.append(pos_down_right)
                break
            else:
                break
        for i in range(1, 8):
            pos_down_left = self.array2grid(row + i, column - i)
            if pos_down_left == "-1":
                break
            piece_down_left = self.get_piece(pos_down_left)
            if piece_down_left == '':
                valid_move_list.append(pos_down_left)
            elif piece_down_left.isupper():
                valid_move_list.append(pos_down_left)
                break
            else:
                break
        return valid_move_list

    def get_white_king_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        # Implement logic for white king
        king_moves = [
            (row - 1, column - 1),  
            (row - 1, column),      
            (row - 1, column + 1), 
            (row, column + 1),      
            (row + 1, column + 1),  
            (row + 1, column),      
            (row + 1, column - 1),  
            (row, column - 1)   
        ]

        for move in king_moves:
            new_pos = self.array2grid(move[0], move[1])
            if new_pos != "-1":
                piece_at_pos = self.get_piece(new_pos)
                if (piece_at_pos == '' or piece_at_pos.islower()):
                    valid_move_list.append(new_pos)
        
        if self.white_king_moved == False and self.get_piece("e1") == "K":
            if self.white_left_rook_moved == False and self.get_piece("a1") == "R":
                valid_move_list.append("c1")
            if self.white_right_rook_moved == False and self.get_piece("h1") == "R":
                valid_move_list.append("g1")
        
        return valid_move_list  

    def get_black_king_valid_moves(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        # Implement logic for black king
        king_moves = [
            (row - 1, column - 1),  
            (row - 1, column),      
            (row - 1, column + 1), 
            (row, column + 1),      
            (row + 1, column + 1),  
            (row + 1, column),      
            (row + 1, column - 1),  
            (row, column - 1)   
        ]
        
        for move in king_moves:
            new_pos = self.array2grid(move[0], move[1])
            if new_pos != "-1":
                piece_at_pos = self.get_piece(new_pos)
                if (piece_at_pos == '' or piece_at_pos.isupper()):
                    valid_move_list.append(new_pos)
                    
        if self.black_king_moved == False and self.get_piece("e8") == "k":
            if self.black_left_rook_moved == False and self.get_piece("a8") == "r":
                valid_move_list.append("c8")
            if self.black_right_rook_moved == False and self.get_piece("h8") == "r":
                valid_move_list.append("g8")
                
        return valid_move_list    
    
    # get the array of valid ending position
    def get_valid_end_pos(self, position: str, chess_piece: str) -> List[str]:
        row, column = self.grid2array(position)
        valid_move_list = []
        
        
        
        
        if chess_piece == "P":
            valid_move_list = self.get_white_pawn_valid_moves(position, chess_piece)
        
        elif chess_piece == "R":
            valid_move_list = self.get_white_rook_valid_moves(position, chess_piece)
        
        elif chess_piece == "N":
            valid_move_list = self.get_white_knight_valid_moves(position, chess_piece)
        
        elif chess_piece == "B":
            valid_move_list = self.get_white_bishop_valid_moves(position, chess_piece)
            
        elif chess_piece == "Q":
            valid_move_list = self.get_white_queen_valid_moves(position, chess_piece)
        
        elif chess_piece == "K":
            valid_move_list = self.get_white_king_valid_moves(position, chess_piece)
             
        elif chess_piece == "p":
            valid_move_list = self.get_black_pawn_valid_moves(position, chess_piece)

        elif chess_piece == "r":
            valid_move_list = self.get_black_rook_valid_moves(position, chess_piece)
        
        elif chess_piece == "n":
            valid_move_list = self.get_black_knight_valid_moves(position, chess_piece)
        
        elif chess_piece == "b":
            valid_move_list = self.get_black_bishop_valid_moves(position, chess_piece)
        
        elif chess_piece == "q":
            valid_move_list = self.get_black_queen_valid_moves(position, chess_piece)
        
        elif chess_piece == "k":
            valid_move_list = self.get_black_king_valid_moves(position, chess_piece)
        
        return valid_move_list  
    
    def check_winning_status(self):
        # get all moves for white pieces
        white_moves = set()
        white_king_pos = ""
        for col in range(ord('a'), ord('h') + 1):
            for row in range(1, 9):
                square = chr(col) + str(row)
                if self.get_piece(square) == 'K':
                    white_king_pos = square
                if self.get_piece(square).isupper():
                    white_moves.update(self.get_valid_end_pos(square, self.get_piece(square)))
        # get all moves for black pieces
        black_moves = set()
        black_king_pos = ""
        for col in range(ord('a'), ord('h') + 1):
            for row in range(1, 9):
                square = chr(col) + str(row)
                if self.get_piece(square) == 'k':
                    black_king_pos = square
                if self.get_piece(square).islower():
                    black_moves.update(self.get_valid_end_pos(square, self.get_piece(square)))
                    
        # Check if either king is in check
        white_in_check = white_king_pos in black_moves
        black_in_check = black_king_pos in white_moves
        
        # Check if white pieces has any legal moves
        white_has_legal_moves = False
        for col in range(ord('a'), ord('h') + 1):
            for row in range(1, 9):
                position = chr(col) + str(row)
                chess_piece = self.get_piece(position)
                if chess_piece.isupper():
                    for move in self.get_valid_end_pos(position, chess_piece):
                        temp_board = [row[:] for row in self.chess_board]
                        temp_result = self.game_result
                        temp_last_move = self.last_move
                        temp_white_king_moved = self.white_king_moved
                        temp_black_king_moved = self.black_king_moved
                        temp_white_left_rook_moved = self.white_left_rook_moved
                        temp_white_right_rook_moved = self.white_right_rook_moved
                        temp_black_left_rook_moved = self.black_left_rook_moved
                        temp_black_right_rook_moved = self.black_right_rook_moved
                        
                        move_result = self.simulate_move(position + move)
                        
                        self.chess_board = temp_board
                        self.game_result = temp_result
                        self.last_move = temp_last_move
                        self.white_king_moved = temp_white_king_moved
                        self.black_king_moved = temp_black_king_moved
                        self.white_left_rook_moved = temp_white_left_rook_moved
                        self.white_right_rook_moved = temp_white_right_rook_moved
                        self.black_left_rook_moved = temp_black_left_rook_moved
                        self.black_right_rook_moved = temp_black_right_rook_moved
                        
                        if move_result != "":
                            white_has_legal_moves = True
                            break
                if white_has_legal_moves:
                    break
            if white_has_legal_moves:
                break
                        
        # Check for black now
        black_has_legal_moves = False
        for col in range(ord('a'), ord('h') + 1):
            for row in range(1, 9):
                position = chr(col) + str(row)
                chess_piece = self.get_piece(position)
                if chess_piece.islower():
                    for move in self.get_valid_end_pos(position, chess_piece):
                        temp_board = [row[:] for row in self.chess_board]
                        temp_result = self.game_result
                        temp_last_move = self.last_move
                        temp_white_king_moved = self.white_king_moved
                        temp_black_king_moved = self.black_king_moved
                        temp_white_left_rook_moved = self.white_left_rook_moved
                        temp_white_right_rook_moved = self.white_right_rook_moved
                        temp_black_left_rook_moved = self.black_left_rook_moved
                        temp_black_right_rook_moved = self.black_right_rook_moved
                        
                        move_result = self.simulate_move(position + move)
    
                        self.chess_board = temp_board
                        self.game_result = temp_result
                        self.last_move = temp_last_move
                        self.white_king_moved = temp_white_king_moved
                        self.black_king_moved = temp_black_king_moved
                        self.white_left_rook_moved = temp_white_left_rook_moved
                        self.white_right_rook_moved = temp_white_right_rook_moved
                        self.black_left_rook_moved = temp_black_left_rook_moved
                        self.black_right_rook_moved = temp_black_right_rook_moved
                        
                        if move_result != "":
                            black_has_legal_moves = True
                            break
                        
                if black_has_legal_moves:
                    break
            if black_has_legal_moves:
                break
        
        print("White King in Check:", white_in_check)
        print("White has legal moves:", white_has_legal_moves)
        print("Black King in Check:", black_in_check)
        print("Black has legal moves:", black_has_legal_moves)
        print("Current Side when checking: ", self.side)
        
        if white_in_check and not white_has_legal_moves:
            self.game_result = "b"
        elif black_in_check and not black_has_legal_moves:
            self.game_result = "w"
        elif ((not white_in_check and not white_has_legal_moves and self.side == "b") or 
            (not black_in_check and not black_has_legal_moves and self.side == "w")):
            self.game_result = "d"
        else:
            self.game_result = ""
        print("Current Winning Status is: " + self.game_result)
        
    
    

    def play_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the chess_board

        Args:
            move (str): The move which is proposed. The format is the following: starting_sqaure}{ending_square}
            
            i.e. e2e4 - This means that whatever chess_piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """
        #Implement this
        start_pos = move[:2]
        end_pos = move[2:]
        chess_piece = self.get_piece(start_pos)
        print("start_pos: ", start_pos, " = ", chess_piece)
        print("end_pos: ", end_pos, " = ", self.get_piece(end_pos))
        promotion = False
        capture = False
        
        if self.check_order:
            if self.last_move != None:
                if chess_piece.isupper() and self.last_move[0].isupper():
                    print("Invalid Order, should be black's move now")
                    return ""
                if chess_piece.islower() and self.last_move[0].islower():
                    print("Invalid Order, should be white's move now")
                    return ""
            else:
                if chess_piece.islower():
                    print("First move should be white")
                    return ""
            if chess_piece.isupper(): 
                self.side = "w"
            elif chess_piece.islower(): 
                self.side = "b"
             
            print("It's " + self.side + " move now")
        

        opponent_moves = set()
        my_king_pos = ""
        if chess_piece != "-1" and chess_piece.isupper():
            # get opponent_color's possible moves
            for col in range(ord('a'), ord('h') + 1):
                for row in range(1, 9):
                    square = chr(col) + str(row)
                    if self.get_piece(square) == 'K':
                        my_king_pos = square
                    if self.get_piece(square).islower():
                        opponent_moves.update(self.get_valid_end_pos(square, self.get_piece(square)))
                        
        elif chess_piece != "-1" and chess_piece.islower():
            # get opponent_color's possible moves
            for col in range(ord('a'), ord('h') + 1):
                for row in range(1, 9):
                    square = chr(col) + str(row)
                    if self.get_piece(square) == 'k':
                        my_king_pos = square
                    if self.get_piece(square).isupper():
                        opponent_moves.update(self.get_valid_end_pos(square, self.get_piece(square)))
        if chess_piece == 'k' or chess_piece == 'K':
            if end_pos in opponent_moves:
                print("This move will leave King in Check")
                self.check_winning_status()
                return ""
        if my_king_pos in opponent_moves:
            print("This move will leave King in Check")
            self.check_winning_status()
            return ""
        
        # check for castling
        if(chess_piece == "K" and self.white_king_moved == False):
            start_row_index, start_col_index = self.grid2array(start_pos)
            end_row_index, end_col_index = self.grid2array(end_pos)
            if(start_row_index == end_row_index == 7 and start_col_index == 4 ):
                if(end_col_index == 2 and self.white_left_rook_moved == False):
                    # move to the left
                    if(self.chess_board[7][1] == self.chess_board[7][2] == self.chess_board[7][3] == "" and 
                       "b1" not in opponent_moves and "c1" not in opponent_moves and  "d1" not in opponent_moves and "e1" not in opponent_moves):
                        # then it's a valid castling
                        print("Is valid castling for white king to the left")
                        print(self.get_piece("b1"))
                        self.chess_board[7][4] = ""
                        self.chess_board[7][0] = ""
                        self.chess_board[7][2] = "K"
                        self.chess_board[7][3] = "R"
                        self.white_king_moved = True
                        self.white_left_rook_moved = True
                        self.last_move = chess_piece, start_pos, end_pos
                        extended_chess_notation = "0-0-0"
                        print("extended_chess_notation: " + extended_chess_notation)
                        self.check_winning_status()
                        return extended_chess_notation
                    else:
                        print("Invalid Castling")
                        self.check_winning_status()
                        return ""
                if(end_col_index == 6 and self.white_right_rook_moved == False):
                    # move to the right
                    if(self.chess_board[7][5] == self.chess_board[7][6] == "" and 
                       "e1" not in opponent_moves and "f1" not in opponent_moves and  "g1" not in opponent_moves):
                        # then it's a valid castling
                        print("Is valid castling for white king to the right")
                        self.chess_board[7][4] = ""
                        self.chess_board[7][7] = ""
                        self.chess_board[7][6] = "K"
                        self.chess_board[7][5] = "R"
                        self.white_king_moved = True
                        self.white_right_rook_moved = True
                        self.last_move = chess_piece, start_pos, end_pos
                        extended_chess_notation = "0-0"
                        print("extended_chess_notation: " + extended_chess_notation)
                        self.check_winning_status()
                        return extended_chess_notation
                    else:
                        print("Invalid Castling")
                        self.check_winning_status()
                        return ""
        elif(chess_piece == "k" and self.black_king_moved == False):
            start_row_index, start_col_index = self.grid2array(start_pos)
            end_row_index, end_col_index = self.grid2array(end_pos)
            if(start_row_index == end_row_index == 0 and start_col_index == 4 ):
                if(end_col_index == 2 and self.black_left_rook_moved == False):
                    # move to the left
                    if(self.chess_board[0][1] == self.chess_board[0][2] == self.chess_board[0][3] == "" and 
                       "b8" not in opponent_moves and "c8" not in opponent_moves and  "d8" not in opponent_moves and "e8" not in opponent_moves):
                        # then it's a valid castling
                        print("Is valid castling for black king to the left")
                        self.chess_board[0][4] = ""
                        self.chess_board[0][0] = ""
                        self.chess_board[0][2] = "k"
                        self.chess_board[0][3] = "r"
                        self.black_king_moved = True
                        self.black_left_rook_moved = True
                        self.last_move = chess_piece, start_pos, end_pos
                        extended_chess_notation = "0-0-0"
                        print("extended_chess_notation: " + extended_chess_notation)
                        self.check_winning_status()
                        return extended_chess_notation
                    else:
                        print("Invalid Castling")
                        self.check_winning_status()
                        return ""
                if(end_col_index == 6 and self.black_right_rook_moved == False):
                    # move to the right
                    if(self.chess_board[0][5] == self.chess_board[0][6] == "" and 
                       "e8" not in opponent_moves and "f8" not in opponent_moves and  "g8" not in opponent_moves):
                        # then it's a valid castling
                        print("Is valid castling for black king to the right")
                        self.chess_board[0][4] = ""
                        self.chess_board[0][7] = ""
                        self.chess_board[0][6] = "k"
                        self.chess_board[0][5] = "r"
                        self.black_king_moved = True
                        self.black_right_rook_moved = True
                        self.last_move = chess_piece, start_pos, end_pos
                        extended_chess_notation = "0-0"
                        print("extended_chess_notation: " + extended_chess_notation)
                        self.check_winning_status()
                        return extended_chess_notation
                    else:
                        print("Invalid Castling")
                        self.check_winning_status()
                        return ""
        valid_end_pos = self.get_valid_end_pos(start_pos, chess_piece)
        print("Valid End Pos: ", valid_end_pos)
        
        # now check for En Passant Capture
        if self.last_move != None:
            last_piece, last_start_pos, last_end_pos = self.last_move
            if chess_piece == 'P' and last_piece == 'p':
                # if I'm white pawn and last move is black pawn
                # I want to check
                # 1. Does the last pawn move twice ahead?
                # 2. Am I at the correct position
                # with both is true, do I want to move at the correct position?
                # If I do want to move at the correct position, then eat it
                
                if abs(int(last_start_pos[1]) - int(last_end_pos[1])) == 2:
                    if start_pos[1] == "5":
                        if end_pos == last_end_pos[0] + str(int(last_end_pos[1]) + 1):
                            start_index = self.grid2array(start_pos)
                            end_index = self.grid2array(end_pos)
                            last_end_index = self.grid2array(last_end_pos)
                            self.chess_board[end_index[0]][end_index[1]] = self.chess_board[start_index[0]][start_index[1]]
                            self.chess_board[start_index[0]][start_index[1]] = ""
                            self.chess_board[last_end_index[0]][last_end_index[1]] = ""
                            capture = True
                            self.last_move = chess_piece, start_pos, end_pos
                            if end_pos[1] == "8":
                                self.chess_board[end_index[0]][end_index[1]] = "Q"
                            extended_chess_notation = (chess_piece.lower() if chess_piece.lower() != "p" else "") + start_pos + "x" + end_pos
                            print("extended_chess_notation: " + extended_chess_notation)
                            self.check_winning_status()
                            return extended_chess_notation
            elif chess_piece == 'p' and last_piece == 'P':
                if abs(int(last_start_pos[1]) - int(last_end_pos[1])) == 2:
                    if start_pos[1] == "4":
                        if end_pos == last_end_pos[0] + str(int(last_end_pos[1]) - 1):
                            start_index = self.grid2array(start_pos)
                            end_index = self.grid2array(end_pos)
                            last_end_index = self.grid2array(last_end_pos)
                            self.chess_board[end_index[0]][end_index[1]] = self.chess_board[start_index[0]][start_index[1]]
                            self.chess_board[start_index[0]][start_index[1]] = ""
                            self.chess_board[last_end_index[0]][last_end_index[1]] = ""
                            capture = True
                            self.last_move = chess_piece, start_pos, end_pos
                            if end_pos[1] == "1":
                                self.chess_board[end_index[0]][end_index[1]] = "q"
                            extended_chess_notation = (chess_piece.lower() if chess_piece.lower() != "p" else "") + start_pos + ("x" if capture else "") + end_pos + ("=Q" if promotion else "")
                            print("extended_chess_notation: " + extended_chess_notation)
                            self.check_winning_status()
                            return extended_chess_notation
        if end_pos in valid_end_pos:   
            start_index = self.grid2array(start_pos)
            end_index = self.grid2array(end_pos)
            if(self.chess_board[end_index[0]][end_index[1]] != ""):
                capture = True
 
            self.chess_board[end_index[0]][end_index[1]] = self.chess_board[start_index[0]][start_index[1]]
            self.chess_board[start_index[0]][start_index[1]] = ""
            self.last_move = chess_piece, start_pos, end_pos
            
            if chess_piece == 'P' and end_pos[1] == "8":
                self.chess_board[end_index[0]][end_index[1]] = "Q"
                promotion = True
            if chess_piece == 'p' and end_pos[1] == "1":
                self.chess_board[end_index[0]][end_index[1]] = "q"
                promotion = True
            if chess_piece == "K" and self.white_king_moved == False:
                self.white_king_moved = True
            if chess_piece == "k" and self.black_king_moved == False:
                self.black_king_moved = True
            if chess_piece == "R" and start_pos == "a1" and self.white_left_rook_moved == False:
                self.white_left_rook_moved = True
            if chess_piece == "R" and start_pos == "h1" and self.white_right_rook_moved == False:
                self.white_right_rook_moved = True
            if chess_piece == "r" and start_pos == "a8" and self.black_left_rook_moved == False:
                self.black_left_rook_moved = True
            if chess_piece == "r" and start_pos == "h8" and self.black_right_rook_moved == False:
                self.black_right_rook_moved = True
            
            
            
            extended_chess_notation = (chess_piece.lower() if chess_piece.lower() != "p" else "") + start_pos + ("x" if capture else "") + end_pos + ("=Q" if promotion else "")
            print("extended_chess_notation: " + extended_chess_notation)
            self.check_winning_status()
            return extended_chess_notation
        
        print("Invalid Moves")
        self.check_winning_status()
        return ""

    def simulate_move(self, move: str) -> str:
        """
        Function to make a move if it is a valid move. This function is called everytime a move in made on the chess_board

        Args:
            move (str): The move which is proposed. The format is the following: starting_sqaure}{ending_square}
            
            i.e. e2e4 - This means that whatever chess_piece is on E2 is moved to E4

        Returns:
            str: Extended Chess Notation for the move, if valid. Empty str if the move is invalid
        """
        #Implement this
        start_pos = move[:2]
        end_pos = move[2:]

        chess_piece = self.get_piece(start_pos)
        promotion = False
        capture = False
        
        # if self.check_order:
        #     if self.last_move != None:
        #         if chess_piece.isupper() and self.last_move[0].isupper():
        #             return ""
        #         if chess_piece.islower() and self.last_move[0].islower():
        #             return ""
        #     else:
        #         if chess_piece.islower():
        #             return ""
        self.side == "w" if chess_piece.isupper() else "b"

        opponent_moves = set()
        my_king_pos = ""
        if chess_piece != "-1" and chess_piece.isupper():
            # get opponent_color's possible moves
            for col in range(ord('a'), ord('h') + 1):
                for row in range(1, 9):
                    square = chr(col) + str(row)
                    if self.get_piece(square) == 'K':
                        my_king_pos = square
                    if self.get_piece(square).islower():
                        opponent_moves.update(self.get_valid_end_pos(square, self.get_piece(square)))
                        
        elif chess_piece != "-1" and chess_piece.islower():
            # get opponent_color's possible moves
            for col in range(ord('a'), ord('h') + 1):
                for row in range(1, 9):
                    square = chr(col) + str(row)
                    if self.get_piece(square) == 'k':
                        my_king_pos = square
                    if self.get_piece(square).isupper():
                        opponent_moves.update(self.get_valid_end_pos(square, self.get_piece(square)))
        if chess_piece == 'k' or chess_piece == 'K':
            if end_pos in opponent_moves:

                return ""
        if my_king_pos in opponent_moves:
            return ""
        
        # check for castling
        if(chess_piece == "K" and self.white_king_moved == False):
            start_row_index, start_col_index = self.grid2array(start_pos)
            end_row_index, end_col_index = self.grid2array(end_pos)
            if(start_row_index == end_row_index == 7 and start_col_index == 4 ):
                if(end_col_index == 2 and self.white_left_rook_moved == False):
                    # move to the left
                    if(self.chess_board[7][1] == self.chess_board[7][2] == self.chess_board[7][3] == "" and 
                       "b1" not in opponent_moves and "c1" not in opponent_moves and  "d1" not in opponent_moves and "e1" not in opponent_moves):
                        # then it's a valid castling
                        self.chess_board[7][4] = ""
                        self.chess_board[7][0] = ""
                        self.chess_board[7][2] = "K"
                        self.chess_board[7][3] = "R"
                        self.white_king_moved = True
                        self.white_left_rook_moved = True
                        self.last_move = chess_piece, start_pos, end_pos
                        extended_chess_notation = "0-0-0"
                        return extended_chess_notation
                    else:
                        return ""
                if(end_col_index == 6 and self.white_right_rook_moved == False):
                    # move to the right
                    if(self.chess_board[7][5] == self.chess_board[7][6] == "" and 
                       "e1" not in opponent_moves and "f1" not in opponent_moves and  "g1" not in opponent_moves):
                        # then it's a valid castling
                        self.chess_board[7][4] = ""
                        self.chess_board[7][7] = ""
                        self.chess_board[7][6] = "K"
                        self.chess_board[7][5] = "R"
                        self.white_king_moved = True
                        self.white_right_rook_moved = True
                        self.last_move = chess_piece, start_pos, end_pos
                        extended_chess_notation = "0-0"
                        return extended_chess_notation
                    else:
                        return ""
        elif(chess_piece == "k" and self.black_king_moved == False):
            start_row_index, start_col_index = self.grid2array(start_pos)
            end_row_index, end_col_index = self.grid2array(end_pos)
            if(start_row_index == end_row_index == 0 and start_col_index == 4 ):
                if(end_col_index == 2 and self.black_left_rook_moved == False):
                    # move to the left
                    if(self.chess_board[0][1] == self.chess_board[0][2] == self.chess_board[0][3] == "" and 
                       "b8" not in opponent_moves and "c8" not in opponent_moves and  "d8" not in opponent_moves and "e8" not in opponent_moves):
                        # then it's a valid castling
                        self.chess_board[0][4] = ""
                        self.chess_board[0][0] = ""
                        self.chess_board[0][2] = "k"
                        self.chess_board[0][3] = "r"
                        self.black_king_moved = True
                        self.black_left_rook_moved = True
                        self.last_move = chess_piece, start_pos, end_pos
                        extended_chess_notation = "0-0-0"
                        return extended_chess_notation
                    else:
                        return ""
                if(end_col_index == 6 and self.black_right_rook_moved == False):
                    # move to the right
                    if(self.chess_board[0][5] == self.chess_board[0][6] == "" and 
                       "e8" not in opponent_moves and "f8" not in opponent_moves and  "g8" not in opponent_moves):
                        # then it's a valid castling
                        self.chess_board[0][4] = ""
                        self.chess_board[0][7] = ""
                        self.chess_board[0][6] = "k"
                        self.chess_board[0][5] = "r"
                        self.black_king_moved = True
                        self.black_right_rook_moved = True
                        self.last_move = chess_piece, start_pos, end_pos
                        extended_chess_notation = "0-0"
                        return extended_chess_notation
                    else:
                        return ""
        valid_end_pos = self.get_valid_end_pos(start_pos, chess_piece)
        
        # now check for En Passant Capture
        if self.last_move != None:
            last_piece, last_start_pos, last_end_pos = self.last_move
            if chess_piece == 'P' and last_piece == 'p':
                # if I'm white pawn and last move is black pawn
                # I want to check
                # 1. Does the last pawn move twice ahead?
                # 2. Am I at the correct position
                # with both is true, do I want to move at the correct position?
                # If I do want to move at the correct position, then eat it
                
                if abs(int(last_start_pos[1]) - int(last_end_pos[1])) == 2:
                    if start_pos[1] == "5":
                        if end_pos == last_end_pos[0] + str(int(last_end_pos[1]) + 1):
                            start_index = self.grid2array(start_pos)
                            end_index = self.grid2array(end_pos)
                            last_end_index = self.grid2array(last_end_pos)
                            self.chess_board[end_index[0]][end_index[1]] = self.chess_board[start_index[0]][start_index[1]]
                            self.chess_board[start_index[0]][start_index[1]] = ""
                            self.chess_board[last_end_index[0]][last_end_index[1]] = ""
                            capture = True
                            self.last_move = chess_piece, start_pos, end_pos
                            if end_pos[1] == "8":
                                self.chess_board[end_index[0]][end_index[1]] = "Q"
                            extended_chess_notation = (chess_piece.lower() if chess_piece.lower() != "p" else "") + start_pos + "x" + end_pos
                            return extended_chess_notation
            elif chess_piece == 'p' and last_piece == 'P':
                if abs(int(last_start_pos[1]) - int(last_end_pos[1])) == 2:
                    if start_pos[1] == "4":
                        if end_pos == last_end_pos[0] + str(int(last_end_pos[1]) - 1):
                            start_index = self.grid2array(start_pos)
                            end_index = self.grid2array(end_pos)
                            last_end_index = self.grid2array(last_end_pos)
                            self.chess_board[end_index[0]][end_index[1]] = self.chess_board[start_index[0]][start_index[1]]
                            self.chess_board[start_index[0]][start_index[1]] = ""
                            self.chess_board[last_end_index[0]][last_end_index[1]] = ""
                            capture = True
                            self.last_move = chess_piece, start_pos, end_pos
                            if end_pos[1] == "1":
                                self.chess_board[end_index[0]][end_index[1]] = "q"
                            extended_chess_notation = (chess_piece.lower() if chess_piece.lower() != "p" else "") + start_pos + ("x" if capture else "") + end_pos + ("=Q" if promotion else "")
                            return extended_chess_notation
        
        if end_pos in valid_end_pos:   
            start_index = self.grid2array(start_pos)
            end_index = self.grid2array(end_pos)
            if(self.chess_board[end_index[0]][end_index[1]] != ""):
                capture = True
                
            self.chess_board[end_index[0]][end_index[1]] = self.chess_board[start_index[0]][start_index[1]]
            self.chess_board[start_index[0]][start_index[1]] = ""
            self.last_move = chess_piece, start_pos, end_pos
            
            if chess_piece == 'P' and end_pos[1] == "8":
                self.chess_board[end_index[0]][end_index[1]] = "Q"
                promotion = True
            if chess_piece == 'p' and end_pos[1] == "1":
                self.chess_board[end_index[0]][end_index[1]] = "q"
                promotion = True
            if chess_piece == "K" and self.white_king_moved == False:
                self.white_king_moved = True
            if chess_piece == "k" and self.black_king_moved == False:
                self.black_king_moved = True
            if chess_piece == "R" and start_pos == "a1" and self.white_left_rook_moved == False:
                self.white_left_rook_moved = True
            if chess_piece == "R" and start_pos == "h1" and self.white_right_rook_moved == False:
                self.white_right_rook_moved = True
            if chess_piece == "r" and start_pos == "a8" and self.black_left_rook_moved == False:
                self.black_left_rook_moved = True
            if chess_piece == "r" and start_pos == "h8" and self.black_right_rook_moved == False:
                self.black_right_rook_moved = True
            
            
            extended_chess_notation = (chess_piece.lower() if chess_piece.lower() != "p" else "") + start_pos + ("x" if capture else "") + end_pos + ("=Q" if promotion else "")
            return extended_chess_notation
        

        return ""