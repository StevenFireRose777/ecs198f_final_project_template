
def array2grid(row: int, col: int) -> str:
    if col < 0 or col > 7 or row < 0 or row > 7:
        return str(-1)
    return chr(col + ord('a')) + str(8 - row)

def grid2array(position: str):
    col = ord(position[0]) - ord('a')
    row = 8 - int(position[1])
    if col < 0 or col > 7 or row < 0 or row > 7:
        return -1, -1
    return row, col
