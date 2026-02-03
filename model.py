import controller as ctrl

class Board:
    def __init__(self):
        self.pieces = []
        self.grid = [["R", "N", "B", "Q", "K", "B", "N", "R"],
                    ["P", "P", "P", "P", "P", "P", "P", "P"],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    ["p", "p", "p", "p", "p", "p", "p", "p"],
                    ["r", "n", "b", "q", "k", "b", "n", "r"]]
        self.turn = "white"
        self.enpassant = None

    # helps with movement of bishops, rooks, and queens even knights
    def move_linear(self, directions, x, y, color):
        moves = []

        for direction in directions:
                    dx, dy = direction
                    new_x, new_y = x + dx, y + dy

                    while 0 <= new_x <= 7 and 0 <= new_y <= 7:
                        if self.grid[new_y][new_x] == " ":
                            moves.append([new_x, new_y])
                        else:
                            # Ensure not capturing own piece
                            if ((color == "white" and self.grid[new_y][new_x].isupper()) or
                               (color == "black" and self.grid[new_y][new_x].islower())):
                                moves.append([new_x, new_y])
                            break
                        new_x += dx
                        new_y += dy
        return moves

    def get_available_moves(self, piece):
        x = piece.x
        y = piece.y
        
        piece_type = self.grid[y][x]

        # Checking color
        if piece_type == piece_type.lower():
            color = "white"
        else:
            color = "black"
        
        # Checking if it's the correct turn
        if color == self.turn:
            moves = []

            # Pawn movement
            if piece_type.lower() == "p":
                direction = -1 if color == "white" else 1
                
                # Standard move
                if self.grid[y + direction][x] == " ":
                    moves.append([x, y + direction])

                    # Initial double move
                    if (color == "white" and y == 6) or (color == "black" and y == 1):
                        # Checking blocking piece
                        if self.grid[y + 2 * direction][x] == " ":
                            moves.append([x, y + 2 * direction])
                    
                # En Passant
                if self.enpassant is not None:
                    if abs(self.enpassant - x) == 1 and y == (3 if color == "white" else 4):
                        moves.append([self.enpassant, y + direction])
                
                # Captures
                if x - 1 >= 0 and self.grid[y + direction][x - 1] != " ":
                    # Ensure not capturing own piece
                    if ((color == "white" and self.grid[y + direction][x - 1].isupper()) or
                       (color == "black" and self.grid[y + direction][x - 1].islower())):
                        moves.append([x - 1, y + direction])
                        
                if x + 1 <= 7 and self.grid[y + direction][x + 1] != " ":
                    # Ensure not capturing own piece
                    if ((color == "white" and self.grid[y + direction][x + 1].isupper()) or
                       (color == "black" and self.grid[y + direction][x + 1].islower())):
                        moves.append([x + 1, y + direction])
            
                return moves
            
            # Knight movement
            elif piece_type.lower() == "n":
                # Everything a knight can do
                x_directions = [2, 2, 1, 1, -1, -1, -2, -2]
                y_directions = [1, -1, 2, -2, 2, -2, 1, -1]

                for i in range(8):
                    new_x = x + x_directions[i]
                    new_y = y + y_directions[i]

                    if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                        if self.grid[new_y][new_x] == " ":
                            moves.append([new_x, new_y])
                        else:
                            # Ensure not capturing own piece
                            if ((color == "white" and self.grid[new_y][new_x].isupper()) or
                               (color == "black" and self.grid[new_y][new_x].islower())):
                                moves.append([new_x, new_y])
                return moves

            # Bishop movement
            elif piece_type.lower() == "b":
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                moves = self.move_linear(directions, x, y, color)
                return moves
            
            # Rook movement
            elif piece_type.lower() == "r":
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                moves = self.move_linear(directions, x, y, color)
                return moves
            
            # Queen movement
            elif piece_type.lower() == "q":
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                              (1, 1), (1, -1), (-1, 1), (-1, -1)]
                moves = self.move_linear(directions, x, y, color)
                return moves
            
            # King movement
            elif piece_type.lower() == "k":
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                              (1, 1), (1, -1), (-1, 1), (-1, -1)]

                for direction in directions:
                    dx, dy = direction
                    new_x, new_y = x + dx, y + dy

                    if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                        if self.grid[new_y][new_x] == " ":
                            moves.append([new_x, new_y])
                        else:
                            # Ensure not capturing own piece
                            if ((color == "white" and self.grid[new_y][new_x].isupper()) or
                               (color == "black" and self.grid[new_y][new_x].islower())):
                                moves.append([new_x, new_y])
                return moves

        else:
            return []

    def update_piece(self, piece, last_x, last_y):
        # Update the board grid
        piece_symbol = self.grid[last_y][last_x]

        # Check for double move for en passant
        if piece_symbol.lower() == "p" and abs(piece.y - last_y) == 2:
            self.enpassant = piece.x
        else:
            self.enpassant = None
        
        # Pawn Promotion
        if piece_symbol.lower() == "p" and (piece.y == 0 or piece.y == 7):
            self.grid[piece.y][piece.x] = piece_symbol
            self.grid[last_y][last_x] = " "
            
            # Switch turn
            self.turn = "black" if self.turn == "white" else "white"

            return [piece, "promotion"]
        # Capturing a piece
        elif self.grid[piece.y][piece.x] != " ":
            self.grid[piece.y][piece.x] = piece_symbol
            self.grid[last_y][last_x] = " "

            # Switch turn
            self.turn = "black" if self.turn == "white" else "white"

            return piece
        # Capturing using En Passant
        elif self.grid[piece.y][piece.x] == " " and piece_symbol.lower() == "p" and last_x != piece.x:
            self.grid[piece.y][piece.x] = piece_symbol
            self.grid[last_y][last_x] = " "
            
            self.grid[last_y][piece.x] = " "

            # Switch turn
            self.turn = "black" if self.turn == "white" else "white"

            return [piece, last_y]
        # Normal move without capture
        else:
            self.grid[piece.y][piece.x] = piece_symbol
            self.grid[last_y][last_x] = " "

            # Switch turn
            self.turn = "black" if self.turn == "white" else "white"

            return None

    def promote_piece(self, piece, new_type_path):
        x = piece.x
        y = piece.y

        match new_type_path[1:-4]: # removing 'w'/'b' and '.png'
            case "queen":
                self.grid[y][x] = "Q" if piece.color == "white" else "q"
            case "rook":
                self.grid[y][x] = "R" if piece.color == "white" else "r"
            case "bishop":
                self.grid[y][x] = "B" if piece.color == "white" else "b"
            case "knight":
                self.grid[y][x] = "N" if piece.color == "white" else "n"
