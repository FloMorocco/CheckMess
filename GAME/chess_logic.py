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

    if piece.islower():
        return False  # Moving opponent's piece

    if target.isupper():
        return False  # Moving to a spot occupied by the player's own piece

    # Example: Add rules for the pawn (P)
    if piece == 'P':
        if col_from == col_to and rows[row_to][col_to] == ' ':  # Moving forward
            if row_to == row_from - 1:
                return True
            if row_from == 6 and row_to == 4 and rows[5][col_from] == ' ':  # Moving two squares from starting position
                return True
        if abs(col_from - col_to) == 1 and row_to == row_from - 1 and target.islower():  # Capturing diagonally
            return True

    # Rules for knight (N)
    if piece == 'N':
        if (abs(row_from - row_to), abs(col_from - col_to)) in [(2, 1), (1, 2)]:
            return True

    # Rules for bishop (B)
    if piece == 'B':
        if abs(row_from - row_to) == abs(col_from - col_to):
            step_row = 1 if row_to > row_from else -1
            step_col = 1 if col_to > col_from else -1
            for i in range(1, abs(row_from - row_to)):
                if rows[row_from + i * step_row][col_from + i * step_col] != ' ':
                    return False
            return True

    # Rules for rook (R)
    if piece == 'R':
        if row_from == row_to or col_from == col_to:
            if row_from == row_to:
                step = 1 if col_to > col_from else -1
                for i in range(col_from + step, col_to, step):
                    if rows[row_from][i] != ' ':
                        return False
            else:
                step = 1 if row_to > row_from else -1
                for i in range(row_from + step, row_to, step):
                    if rows[i][col_from] != ' ':
                        return False
            return True

    # Rules for queen (Q)
    if piece == 'Q':
        if row_from == row_to or col_from == col_to:
            return is_valid_move(board_state, f"{row_from * 8 + col_from}-{'row_to * 8 + col_to'}")  # Rook-like move
        if abs(row_from - row_to) == abs(col_from - col_to):
            return is_valid_move(board_state, f"{row_from * 8 + col_from}-{'row_to * 8 + col_to'}")  # Bishop-like move

    # Rules for king (K)
    if piece == 'K':
        if max(abs(row_from - row_to), abs(col_from - col_to)) == 1:
            return True

    return False

def update_board_state(board_state, move):
    rows = expand_fen(board_state)
    row_from, col_from = divmod(int(move.split('-')[0]), 8)
    row_to, col_to = divmod(int(move.split('-')[1]), 8)

    piece = rows[row_from][col_from]
    rows[row_to] = rows[row_to][:col_to] + piece + rows[row_to][col_to + 1:]
    rows[row_from] = rows[row_from][:col_from] + ' ' + rows[row_from][col_from + 1:]

    return '/'.join(''.join(str(len(group)) if len(group) > 1 else group[0] for group in ''.join(row).split(' ')) for row in rows)

def fen_to_board_list(board_state):
    """Convert FEN string to board list representation."""
    board_list = []
    for char in board_state:
        if char.isdigit():
            board_list.extend([' '] * int(char))
        elif char != '/':
            board_list.append(char)
    return board_list

def board_list_to_fen(board_list):
    """Convert board list representation to FEN string."""
    updated_board_state = ''
    empty_count = 0
    for i, square in enumerate(board_list):
        if square == ' ':
            empty_count += 1
        else:
            if empty_count > 0:
                updated_board_state += str(empty_count)
                empty_count = 0
            updated_board_state += square
        if (i + 1) % 8 == 0:
            if empty_count > 0:
                updated_board_state += str(empty_count)
                empty_count = 0
            if i < 63:
                updated_board_state += '/'
    return updated_board_state.rstrip('/')
