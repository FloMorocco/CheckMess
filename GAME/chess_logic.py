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

def compress_fen_row(row):
    compressed_row = ''
    empty_count = 0
    for char in row:
        if char == ' ':
            empty_count += 1
        else:
            if empty_count > 0:
                compressed_row += str(empty_count)
                empty_count = 0
            compressed_row += char
    if empty_count > 0:
        compressed_row += str(empty_count)
    return compressed_row

def compress_fen(rows):
    return '/'.join([compress_fen_row(row) for row in rows])

def is_valid_pawn_move(piece, row_from, col_from, row_to, col_to, target, rows):
    if col_from == col_to and target == ' ':
        if piece == 'P':
            if row_to == row_from - 1:  # Move forward by 1
                return True
            if row_from == 6 and row_to == 4 and rows[5][col_from] == ' ':  # Move forward by 2 from starting position
                return True
        if piece == 'p':
            if row_to == row_from + 1:  # Move forward by 1
                return True
            if row_from == 1 and row_to == 3 and rows[2][col_from] == ' ':  # Move forward by 2 from starting position
                return True
    if abs(col_from - col_to) == 1 and target != ' ' and target.islower() != piece.islower():
        if piece == 'P' and row_to == row_from - 1:  # Capture diagonally
            return True
        if piece == 'p' and row_to == row_from + 1:  # Capture diagonally
            return True
    return False

def is_valid_knight_move(row_from, col_from, row_to, col_to, target, piece):
    if (abs(row_from - row_to), abs(col_from - col_to)) in [(2, 1), (1, 2)]:
        return target == ' ' or target.islower() != piece.islower()
    return False

def is_valid_rook_move(row_from, col_from, row_to, col_to, target, piece, rows):
    if row_from == row_to:
        for col in range(min(col_from, col_to) + 1, max(col_from, col_to)):
            if rows[row_from][col] != ' ':
                return False
        return target == ' ' or target.islower() != piece.islower()
    if col_from == col_to:
        for row in range(min(row_from, row_to) + 1, max(row_from, row_to)):
            if rows[row][col_from] != ' ':
                return False
        return target == ' ' or target.islower() != piece.islower()
    return False

def is_valid_bishop_move(row_from, col_from, row_to, col_to, target, piece, rows):
    if abs(row_from - row_to) == abs(col_from - col_to):
        step_row = (row_to - row_from) // abs(row_to - row_from)
        step_col = (col_to - col_from) // abs(col_to - col_from)
        for step in range(1, abs(row_to - row_from)):
            if rows[row_from + step * step_row][col_from + step * step_col] != ' ':
                return False
        return target == ' ' or target.islower() != piece.islower()
    return False

def is_valid_queen_move(row_from, col_from, row_to, col_to, target, piece, rows):
    return is_valid_rook_move(row_from, col_from, row_to, col_to, target, piece, rows) or \
           is_valid_bishop_move(row_from, col_from, row_to, col_to, target, piece, rows)

def is_valid_king_move(row_from, col_from, row_to, col_to, target, piece):
    if max(abs(row_from - row_to), abs(col_from - col_to)) == 1:
        return target == ' ' or target.islower() != piece.islower()
    return False

def is_valid_move(board_state, move):
    rows = expand_fen(board_state)
    row_from, col_from = divmod(int(move.split('-')[0]), 8)
    row_to, col_to = divmod(int(move.split('-')[1]), 8)

    piece = rows[row_from][col_from]
    target = rows[row_to][col_to]

    # Prevent moving to a cell occupied by a piece of the same color
    if target != ' ' and target.islower() == piece.islower():
        return False

    if piece == 'P' or piece == 'p':
        return is_valid_pawn_move(piece, row_from, col_from, row_to, col_to, target, rows)
    if piece == 'N' or piece == 'n':
        return is_valid_knight_move(row_from, col_from, row_to, col_to, target, piece)
    if piece == 'R' or piece == 'r':
        return is_valid_rook_move(row_from, col_from, row_to, col_to, target, piece, rows)
    if piece == 'B' or piece == 'b':
        return is_valid_bishop_move(row_from, col_from, row_to, col_to, target, piece, rows)
    if piece == 'Q' or piece == 'q':
        return is_valid_queen_move(row_from, col_from, row_to, col_to, target, piece, rows)
    if piece == 'K' or piece == 'k':
        return is_valid_king_move(row_from, col_from, row_to, col_to, target, piece)

    return False

def update_board_state(board_state, move):
    rows = expand_fen(board_state)
    row_from, col_from = divmod(int(move.split('-')[0]), 8)
    row_to, col_to = divmod(int(move.split('-')[1]), 8)

    rows[row_to] = rows[row_to][:col_to] + rows[row_from][col_from] + rows[row_to][col_to + 1:]
    rows[row_from] = rows[row_from][:col_from] + ' ' + rows[row_from][col_from + 1:]

    return '/'.join(rows)

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


def apply_spell_effects(board_state, active_spells):
    # Logic to apply spell effects based on the active spells
    for active_spell in active_spells:
        spell = Spell.query.get(active_spell.spell_id)
        if spell.effect == "some_effect":  # Example effect
            # Apply the effect to the board_state
            pass
    return board_state

def is_valid_spell_target(spell, target):
    # Logic to determine if the target is valid for the spell
    piece = target['piece']
    target_type = spell.target_type
    piece_compatibility = spell.piece_compatibility.split(',')

    if target_type == 'self' and piece in piece_compatibility:
        return True
    elif target_type == 'opponent' and piece.islower() and piece.upper() in piece_compatibility:
        return True
    elif target_type == 'empty' and piece == ' ':
        return True

    return False

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