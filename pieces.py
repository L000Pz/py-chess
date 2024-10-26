
chessboard = [
    ['Br', 'Bn', 'Bb', 'Bq', 'Bk', 'Bb', 'Bn', 'Br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['Wr', 'Wn', 'Wb', 'Wq', 'Wk', 'Wb', 'Wn', 'Wr']
]


def move_pawn(board, from_square, to_square):

    from_row, from_col = ord('8')-ord(
        from_square[1]), ord(from_square[0]) - ord('a')
    print(from_row, from_col)
    to_row, to_col = ord('8') - ord(to_square[1]), ord(to_square[0]) - ord('a')

    if abs(from_row - to_row) <= 2 and from_col == to_col and 'p' in board[from_row][from_col]:
        board[to_row][to_col] = board[from_row][from_col]
        board[from_row][from_col] = '.'
        show_chessboard(chessboard)

    else:
        print("Invalid move for the pawn.")


def show_chessboard(chessboard):
    print('\n'.join(map(''.join, chessboard)))


move_pawn(chessboard, "e2", "e4")
