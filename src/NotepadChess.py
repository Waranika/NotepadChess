import tkinter as tk 
from tkinter import filedialog, messagebox
import chess
import chess.engine
import threading
import time



class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NormalNotepad")
        self.root.geometry("800x600")

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
        help_menu.add_command(label="Show Board", command=self.show_board)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Track current file
        self.current_file = None

        # Initialize chess board and engine
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\kizer\stockfish\stockfish-windows-x86-64-avx2.exe")  # Ensure you have Stockfish installed

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
    
    def show_board(self):
        board_window = tk.Toplevel(self.root)
        board_window.title("Chess Board")
        board_label = tk.Label(board_window, font=("Courier", 16), justify=tk.LEFT)

        def render_board():
            unicode_board = ""
            for row in str(self.board).split("\n"):
                unicode_row = row.replace("P", " ♙ ").replace("p", " ♟ ")
                unicode_row = unicode_row.replace("R", " ♖ ").replace("r", " ♜ ")
                unicode_row = unicode_row.replace("N", " ♘ ").replace("n", " ♞ ")
                unicode_row = unicode_row.replace("B", " ♗ ").replace("b", " ♝ ")
                unicode_row = unicode_row.replace("Q", " ♕ ").replace("q", " ♛ ")
                unicode_row = unicode_row.replace("K", " ♔ ").replace("k", " ♚ ")
                unicode_row = unicode_row.replace(".", "·   ")  
                unicode_board += unicode_row + "\n"
            board_label.config(text=unicode_board, font=("Courier", 20))

        render_board()
        board_label.pack(padx=10, pady=10)

        # Close the board after 10 seconds
        def close_board():
            time.sleep(10)
            board_window.destroy()

        threading.Thread(target=close_board, daemon=True).start()



if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()
