import model

# Initializing the board
board = model.Board()

# Get available moves from model
def available_moves(piece):
    moves = board.get_available_moves(piece)
    return moves

# Update piece position in model
def update_model_piece(piece, last_x, last_y):
    piece = board.update_piece(piece, last_x, last_y)
    return piece

# Promote pawn in model
def promote_pawn(piece, new_type_path):
    board.promote_piece(piece, new_type_path)
