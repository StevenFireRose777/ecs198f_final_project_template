
from utils import array2grid, grid2array

def get_white_pawn_valid_moves(position: str, chess_piece: str, chess_board):
    row, column = grid2array(position)
    valid_move_list = []
    
    front_position = array2grid(row-1, column)
    if front_position != "-1" and chess_board[row-1][column] == '':
        valid_move_list.append(front_position)
        if row == 6:
            double_front_position = array2grid(row-2, column)
            if chess_board[row-2][column] == '':
                valid_move_list.append(double_front_position)
                
    left_diagonal_position = array2grid(row-1, column-1)
    if left_diagonal_position != "-1" and chess_board[row-1][column-1].islower():
        valid_move_list.append(left_diagonal_position)
    right_diagonal_position = array2grid(row-1, column+1)
    if right_diagonal_position != "-1" and chess_board[row-1][column+1].islower():
        valid_move_list.append(right_diagonal_position)

    return valid_move_list
