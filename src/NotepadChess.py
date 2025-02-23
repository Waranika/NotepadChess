import tkinter as tk 
from tkinter import filedialog, messagebox
import chess
import chess.engine
import threading
import time
import os
import signal
from PIL import Image, ImageTk
import sys
import subprocess



class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NormalNotepad")
        self.root.geometry("800x600")

        # Bind the window close button (X) to exit_app()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        # Create Text Area
        self.text_area = tk.Text(self.root, wrap='word', undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind("<Return>", self.handle_chess_move)

        # Adding Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_area)   
        self.text_area.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.text_area.yview)

        # Create Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=lambda: self.text_area.event_generate("<<SelectAll>>"))
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Show Board", command=self.show_board_canvas)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Track current file
        self.current_file = None

        # Initialize chess board and engine
        self.board = chess.Board()
        # Figure out the base path
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        # Path to Stockfish engine
        engine_path = os.path.join(base_path, "stockfish", "stockfish-windows-x86-64-avx2.exe")

        # Only define creationflags on Windows
        creationflags = 0
        if os.name == "nt":
            creationflags = subprocess.CREATE_NO_WINDOW

        # Launch the engine
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path , creationflags=creationflags)

         # Pre-load images so they stay in memory
        self.piece_images = {}
        self.load_piece_images()

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("New File - Notepad App")
        self.board.reset()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.root.title(f"{file_path} - Notepad App")

    def save_file(self):
        if self.current_file:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, "w") as file:
                file.write(content)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.current_file = file_path
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.root.title(f"{file_path} - Notepad App")

    def exit_app(self):
        self.engine.quit()
        self.root.destroy()

    def show_about(self):
        messagebox.showinfo("About", "Notepad App with Chess made with Python and tkinter!")

    
    def handle_chess_move(self, event):
        # Get the last line typed by the user
        content = self.text_area.get(1.0, tk.END).strip()
        if not content:
            return "break"

        last_line = content.splitlines()[-1]
        if self.board.is_game_over():
            self.text_area.insert(tk.END, "\nGame Over!\n")
            return "break"

        try:
            # Attempt to make the move
            move = chess.Move.from_uci(last_line.strip())
            if move in self.board.legal_moves:
                self.board.push(move)

                # Get CPU move
                result = self.engine.play(self.board, chess.engine.Limit(time=1))
                cpu_move = result.move
                self.board.push(cpu_move)

                # Append CPU move to the text area
                self.text_area.insert(tk.END, f"\n{cpu_move.uci()}\n")
            '''
            else:
                self.text_area.insert(tk.END, "\nInvalid move!\n")

            '''   
        except ValueError:
            pass
        return 
    
    def load_piece_images(self):
        """
        Loads each piece image at a consistent size.
        For an 8×8 board with e.g. 60px squares, 50-60px is a good piece size.
        """
        square_size = 60
        # Mapping from piece symbol to image filename
        # uppercase = White pieces, lowercase = Black pieces
        piece_filenames = {
            'P': 'wP.png', 'R': 'wR.png', 'N': 'wN.png', 'B': 'wB.png',
            'Q': 'wQ.png', 'K': 'wK.png',
            'p': 'bP.png', 'r': 'bR.png', 'n': 'bN.png', 'b': 'bB.png',
            'q': 'bQ.png', 'k': 'bK.png',
        }

       # Use the same base_path logic you used for the Stockfish engine
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        # Construct the path to the images folder under base_path
        images_folder = os.path.join(base_path, 'images')
        
        for symbol, filename in piece_filenames.items():
            image_file_path = os.path.join(images_folder, filename)
            img = Image.open(image_file_path).convert("RGBA")
            img = img.resize((square_size, square_size), Image.ANTIALIAS)
            self.piece_images[symbol] = ImageTk.PhotoImage(img)


    def show_board_canvas(self):
        """
        Displays the chessboard on a Canvas widget in a new window,
        coloring squares in a checker pattern and drawing piece images.
        """
        board_window = tk.Toplevel(self.root)
        board_window.title("Chess Board (Canvas)")

        square_size = 60
        canvas_size = square_size * 8
        canvas = tk.Canvas(board_window, width=canvas_size, height=canvas_size)
        canvas.pack()

        # Typical "light wood" / "dark wood" colors from popular chess websites
        light_color = "#F0D9B5"
        dark_color = "#B58863"

        # Draw checkerboard squares
        for row in range(8):
            for col in range(8):
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                # Alternate square color
                if (row + col) % 2 == 0:
                    fill_color = light_color
                else:
                    fill_color = dark_color
                # Draw the square (no outline)
                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="")
        # Place the chess pieces according to self.board
        # Note: python-chess squares go from 0..63, left-to-right, bottom-to-top
        # We want row=0 at the top in the canvas, so row in canvas = 7 - rank
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                # Convert square index to (row, col)
                rank = square // 8
                file = square % 8
                row = 7 - rank         # row 0 at top
                col = file             # col 0 at left

                x = col * square_size
                y = row * square_size
                symbol = piece.symbol()  # e.g. 'P', 'p', 'R', etc.

                # Use the pre-loaded piece image
                if symbol in self.piece_images:
                    canvas.create_image(x, y, image=self.piece_images[symbol], anchor="nw")

        # Optionally close board after 10 seconds in a background thread
        def close_board():
            time.sleep(10)
            board_window.destroy()

        threading.Thread(target=close_board, daemon=True).start()



if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop() 
