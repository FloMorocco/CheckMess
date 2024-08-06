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
    row_from, col_from = divmod(int(move.split('-')[0]), 8)
    row_to, col_to = divmod(int(move.split('-')[1]), 8)

    piece = rows[row_from][col_from]
    target = rows[row_to][col_to]

    if piece == ' ':
        return False

    if piece == 'P':
        if col_from == col_to and rows[row_to][col_to] == ' ':
            if row_to == row_from - 1:
                return True
            if row_from == 6 and row_to == 4 and rows[5][col_from] == ' ':
                return True
        if abs(col_from - col_to) == 1 and row_to == row_from - 1 and target.islower():
            return True
    if piece == 'N':
        if (abs(row_from - row_to), abs(col_from - col_to)) in [(2, 1), (1, 2)] and target.islower():
            return True
    if piece == 'B':
        if abs(row_from - row_to) == abs(col_from - col_to):
            step_row = (row_to - row_from) // abs(row_to - row_from)
            step_col = (col_to - col_from) // abs(col_to - col_from)
            for i in range(1, abs(row_to - row_from)):
                if rows[row_from + i * step_row][col_from + i * step_col] != ' ':
                    return False
            return target.islower()
    if piece == 'R':
        if row_from == row_to:
            step = 1 if col_to > col_from else -1
            for col in range(col_from + step, col_to, step):
                if rows[row_from][col] != ' ':
                    return False
            return target.islower()
        if col_from == col_to:
            step = 1 if row_to > row_from else -1
            for row in range(row_from + step, row_to, step):
                if rows[row][col_from] != ' ':
                    return False
            return target.islower()
    if piece == 'Q':
        if abs(row_from - row_to) == abs(col_from - col_to) or row_from == row_to or col_from == col_to:
            if abs(row_from - row_to) == abs(col_from - col_to):
                step_row = (row_to - row_from) // abs(row_to - row_from)
                step_col = (col_to - col_from) // abs(col_to - col_from)
                for i in range(1, abs(row_to - row_from)):
                    if rows[row_from + i * step_row][col_from + i * step_col] != ' ':
                        return False
            if row_from == row_to:
                step = 1 if col_to > col_from else -1
                for col in range(col_from + step, col_to, step):
                    if rows[row_from][col] != ' ':
                        return False
            if col_from == col_to:
                step = 1 if row_to > row_from else -1
                for row in range(row_from + step, row_to, step):
                    if rows[row][col_from] != ' ':
                        return False
            return target.islower()
    if piece == 'K':
        if abs(row_from - row_to) <= 1 and abs(col_from - col_to) <= 1:
            return target.islower()
    return False

def update_board_state(board_state, move):
    rows = expand_fen(board_state)
    row_from, col_from = divmod(int(move.split('-')[0]), 8)
    row_to, col_to = divmod(int(move.split('-')[1]), 8)

    piece = rows[row_from][col_from]
    rows[row_to] = rows[row_to][:col_to] + piece + rows[row_to][col_to + 1:]
    rows[row_from] = rows[row_from][:col_from] + ' ' + rows[row_from][col_from + 1:]

    return '/'.join(rows)

def is_valid_spell_target(spell, target_piece):
    target_type = spell.target_type
    if target_type == 'any':
        return True
    if target_type == 'pawn' and target_piece.lower() == 'p':
        return True
    if target_type == 'knight' and target_piece.lower() == 'n':
        return True
    return False

def apply_spell(board_state, spell, target_piece):
    # Implement the effect of the spell here
    # This function should update the board state according to the spell's effect
    return board_state
