import logging

logging.basicConfig(level=logging.DEBUG)
def expand_fen_row(row):
    expanded_row = ''
    for char in row:
        if char.isdigit():
            expanded_row += ' ' * int(char)
        else:
            expanded_row += char
    return expanded_row

def expand_fen(board_state):
    rows = board_state.split('/')
    return [expand_fen_row(row) for row in rows]



def is_valid_move(board_state, move):
    rows = expand_fen(board_state)
    logging.debug(f"Expanded board state: {rows}")
    row_from, col_from = divmod(int(move.split('-')[0]), 8)
    row_to, col_to = divmod(int(move.split('-')[1]), 8)

    piece = rows[row_from][col_from]
    target = rows[row_to][col_to]
    logging.debug(f"Move from ({row_from}, {col_from}) to ({row_to}, {col_to}) with piece {piece}")

    if piece == 'P':
        if col_from == col_to and target == ' ':
            if row_to == row_from - 1 or (row_from == 6 and row_to == 4 and rows[5][col_from] == ' '):
                return True
        if abs(col_from - col_to) == 1 and row_to == row_from - 1 and target.islower():
            return True

    return False

def update_board_state(board_state, move):
    rows = expand_fen(board_state)
    logging.debug(f"Expanded board state before update: {rows}")
    row_from, col_from = divmod(int(move.split('-')[0]), 8)
    row_to, col_to = divmod(int(move.split('-')[1]), 8)

    rows[row_to] = rows[row_to][:col_to] + rows[row_from][col_from] + rows[row_to][col_to + 1:]
    rows[row_from] = rows[row_from][:col_from] + ' ' + rows[row_from][col_from + 1:]

    new_board_state = '/'.join(rows).replace('        ', '8').replace('       ', '7').replace('      ', '6').replace('     ', '5').replace('    ', '4').replace('   ', '3').replace('  ', '2').replace(' ', '1')
    logging.debug(f"Board state after update: {new_board_state}")

    return new_board_state
