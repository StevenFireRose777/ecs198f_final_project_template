
from utils import array2grid, grid2array

def get_white_pawn_valid_moves(pos: str, piece: str, board):
    row_index, col_index = grid2array(pos)
    valid_moves = []
    
    pos_at_front = array2grid(row_index-1, col_index)
    if pos_at_front != "-1" and board[row_index-1][col_index] == '':
        valid_moves.append(pos_at_front)
        if row_index == 6:
            pos_at_front_twice = array2grid(row_index-2, col_index)
            if board[row_index-2][col_index] == '':
                valid_moves.append(pos_at_front_twice)
                
    pos_at_left_diag = array2grid(row_index-1, col_index-1)
    if pos_at_left_diag != "-1" and board[row_index-1][col_index-1].islower():
        valid_moves.append(pos_at_left_diag)
    pos_at_right_diag = array2grid(row_index-1, col_index+1)
    if pos_at_right_diag != "-1" and board[row_index-1][col_index+1].islower():
        valid_moves.append(pos_at_right_diag)

    return valid_moves
