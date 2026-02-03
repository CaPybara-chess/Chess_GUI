from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path
import controller as ctrl


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Hedgehog Tkinter Chess engine")
        self.root.geometry("1000x700")

        # Current screen
        self.current = None
        self.show_menu()

        self.root.mainloop()

    def switch(self, Screen_name):
        # Switching screens
        if self.current:
            self.current.destroy()

        self.current = Screen_name(self.root, self)
        self.current.pack(fill="both", expand=True)

    def show_menu(self):
        self.switch(Menu_screen)

    def show_game(self):
        self.switch(Game_screen)


class Screens(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Change directory to Images folder
        self.IMAGE_DIR = Path(__file__).parent / "Images"

        # Create canvas for background
        self.canvas = Canvas(self, width=1000, height=700)
        self.canvas.pack(fill="both", expand=True)
    
    def set_background(self, image_path):
        # Set background image
        bg_img = Image.open(self.IMAGE_DIR / image_path)
        bg_img_resized = bg_img.resize((1000, 700), resample=Image.Resampling.NEAREST)
        self.bg_photo = ImageTk.PhotoImage(bg_img_resized)  # Keep reference to prevent garbage collection
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)


class Menu_screen(Screens):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.set_background("background.png")

        # Adding title and button on top of canvas
        self.title = Label(self, text="Hedgehog Chess", bg="black", fg="white", font=("Courier", 40, "bold"))
        self.button = Button(self, text="PLAY", bd=10, font=("Calibri", 30, "bold"), command=self.game)

         # Place title and button on canvas
        self.canvas.create_window(500, 50, window=self.title)
        self.canvas.create_window(500, 350, window=self.button)

    def game(self):
        self.app.show_game()


class Game_screen(Screens):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.set_background("chessboard.png")

        # Setting up grid for pieces
        self.x_grid = [266 + i * 67 for i in range(8)]
        self.y_grid = [118 + i * 67 for i in range(8)]

        # Creating pieces
        self.pieces = []
        # Pawns
        for pawn in range(8):
            self.pieces.append(Piece(self, "wpawn.png", "pawn", "white", pawn, 6))
        for pawn in range(8):
            self.pieces.append(Piece(self, "bpawn.png", "pawn", "black", pawn, 1))
        # Rooks
        self.pieces.append(Piece(self, "wrook.png", "rook", "white", 0, 7))
        self.pieces.append(Piece(self, "wrook.png", "rook", "white", 7, 7))
        self.pieces.append(Piece(self, "brook.png", "rook", "black", 0, 0))
        self.pieces.append(Piece(self, "brook.png", "rook", "black", 7, 0))
        # Knights
        self.pieces.append(Piece(self, "wknight.png", "knight", "white", 1, 7))
        self.pieces.append(Piece(self, "wknight.png", "knight", "white", 6, 7))
        self.pieces.append(Piece(self, "bknight.png", "knight", "black", 1, 0))
        self.pieces.append(Piece(self, "bknight.png", "knight", "black", 6, 0))
        # Bishops
        self.pieces.append(Piece(self, "wbishop.png", "bishop", "white", 2, 7))
        self.pieces.append(Piece(self, "wbishop.png", "bishop", "white", 5, 7))
        self.pieces.append(Piece(self, "bbishop.png", "bishop", "black", 2, 0))
        self.pieces.append(Piece(self, "bbishop.png", "bishop", "black", 5, 0))
        # Queens
        self.pieces.append(Piece(self, "wqueen.png", "queen", "white", 3, 7))
        self.pieces.append(Piece(self, "bqueen.png", "queen", "black", 3, 0))
        # Kings
        self.pieces.append(Piece(self, "wking.png", "king", "white", 4, 7))
        self.pieces.append(Piece(self, "bking.png", "king", "black", 4, 0))

        # Predefine highlights for deleting later
        self.highlights = []

        # Display pieces on the board
        for piece in self.pieces:
            piece.show()


class Piece():
    def __init__(self, parent, image_path, name, color, x, y):
        self.parent = parent
        self.image_path = image_path
        self.color = color
        self.name = name
        self.x = x
        self.y = y
        # Predefine move highlights for deleting later
        self.move_highlights = []
        # Keeping track of promotion buttons
        self.promo_buttons = []
        self.promo_photos = []

    def show_promotion(self, piece):
        promotion_pieces = ["queen", "rook", "bishop", "knight"]
        color = "w" if self.color == "white" else "b"
        promotion_images = [f"{color}{piece}.png" for piece in promotion_pieces]

        for i in promotion_images:
            promo_img = Image.open(self.parent.IMAGE_DIR / i)
            promo_img_resized = promo_img.resize((50, 50), resample=Image.Resampling.NEAREST)
            self.promo_photo = ImageTk.PhotoImage(promo_img_resized)  # Keep reference to prevent garbage collection
            self.promo_photos.append(self.promo_photo)

            # Determine x position for promotion buttons
            if promotion_images.index(i) %2 == 0:
                x_pos = self.parent.x_grid[piece.x] + 35
            else:
                x_pos = self.parent.x_grid[piece.x] - 35

            # Determine y position for promotion buttons
            if promotion_images.index(i) < 2:
                y_pos = self.parent.y_grid[piece.y] + 35
            else:
                y_pos = self.parent.y_grid[piece.y] - 35

            promo_button = self.parent.canvas.create_image(x_pos, y_pos, image=self.promo_photo)
            self.parent.canvas.tag_bind(promo_button, "<Button-1>", lambda event, pb=promo_button: self.promote(pb, i, piece, event))
            self.promo_buttons.append(promo_button)
            self.parent.canvas.itemconfigure(promo_button, state="normal")

    def promote(self, promo_button, image_path, piece, event=None):
        # Remove promotion buttons
        for button in self.promo_buttons:
            self.parent.canvas.delete(button)
        self.promo_buttons = []

        # Update piece image
        self.name = image_path
        self.color = "w" if self.color == "white" else "b"
        self.image_path = self.name
        piece_img = Image.open(self.parent.IMAGE_DIR / self.image_path)
        piece_img_resized = piece_img.resize((50, 50), resample=Image.Resampling.NEAREST)
        self.piece_photo = ImageTk.PhotoImage(piece_img_resized)  # Keep reference to prevent garbage collection

        self.image_button = self.parent.canvas.create_image(self.parent.x_grid[self.x], self.parent.y_grid[self.y], image=self.piece_photo)

        # Place piece on the board
        self.parent.canvas.tag_bind(self.image_button, "<Button-1>", self.move)
        
        # Update model
        ctrl.promote_pawn(self, self.image_path)

    def show(self):
        piece_img = Image.open(self.parent.IMAGE_DIR / self.image_path)
        piece_img_resized = piece_img.resize((50, 50), resample=Image.Resampling.NEAREST)
        self.piece_photo = ImageTk.PhotoImage(piece_img_resized)  # Keep reference to prevent garbage collection

        self.image_button = self.parent.canvas.create_image(self.parent.x_grid[self.x], self.parent.y_grid[self.y], image=self.piece_photo)

        # Place piece on the board
        self.parent.canvas.tag_bind(self.image_button, "<Button-1>", self.move)

    def move(self, event=None):
        self.highlight_path = "move_highlight.png"

        # Load highlight image
        move_img = Image.open(self.parent.IMAGE_DIR / self.highlight_path)
        move_img_resized = move_img.resize((50, 50), resample=Image.Resampling.NEAREST)
        self.move_photo = ImageTk.PhotoImage(move_img_resized)  # Keep reference to prevent garbage collection

        # Get available moves from controller
        moves = ctrl.available_moves(self)
        self.move_highlights = []

        # Delete previous highlights
        for highlight in self.parent.highlights:
            self.parent.canvas.delete(highlight)

        # Create highlights for available moves
        for move in moves:
            move_highlight = self.parent.canvas.create_image(self.parent.x_grid[move[0]], self.parent.y_grid[move[1]], image=self.move_photo)
            self.move_highlights.append(move_highlight)
            self.parent.canvas.tag_bind(move_highlight, "<Button-1>", lambda event, mh=move_highlight: self.move_to(mh, event))

        # Store highlights in parent for later deletion
        self.parent.highlights = self.move_highlights

    def move_to(self, move_highlight, event=None):
        # Get coordinates of the selected move highlight
        hx, hy = self.parent.canvas.coords(move_highlight)

        # Get coordinates of the piece
        px, py  = self.parent.canvas.coords(self.image_button)
        px = self.parent.x_grid.index(px)
        py = self.parent.y_grid.index(py)
        
        # Update Piece coordinates
        self.x = self.parent.x_grid.index(hx)
        self.y = self.parent.y_grid.index(hy)
        
        # Update model
        capturing_piece = ctrl.update_model_piece(self, px, py)

        # Special occurences handling
        if isinstance(capturing_piece, list):
            # Promoting pawn
            if capturing_piece[1] == "promotion":
                promoting_piece = capturing_piece[0]

                # Check for captured piece during promotion
                for piece in self.parent.pieces:
                    if piece != promoting_piece and piece.x == promoting_piece.x and piece.y == promoting_piece.y:
                        # Remove captured piece from board
                        self.parent.canvas.delete(piece.image_button)
                        self.parent.pieces.remove(piece)
                # Early remove highlights
                for highlight in self.parent.highlights:
                    self.parent.canvas.delete(highlight)
                self.parent.canvas.coords(self.image_button, hx, hy)

                self.show_promotion(promoting_piece)
            # En Passant capture
            else:
                last_y = capturing_piece[1]
                capturing_piece = capturing_piece[0]
                
                for piece in self.parent.pieces:
                    if piece.x == capturing_piece.x and piece.y == last_y:
                        # Remove captured piece from board
                        self.parent.canvas.delete(piece.image_button)
                        self.parent.pieces.remove(piece)
        # Check if there is a capture
        elif capturing_piece:
            for piece in self.parent.pieces:
                if piece != capturing_piece and piece.x == capturing_piece.x and piece.y == capturing_piece.y:
                    # Remove captured piece from board
                    self.parent.canvas.delete(piece.image_button)
                    self.parent.pieces.remove(piece)

        # Delete previous highlights
        for highlight in self.parent.highlights:
            self.parent.canvas.delete(highlight)

        # Move the piece to the new position
        self.parent.canvas.coords(self.image_button, hx, hy)
