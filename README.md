# Notepad Chess

**Description:**
A fun project to play chess against a CPU in a minimal and concealed way. This application combines a basic text editor with chess functionality, allowing you to take notes while casually playing chess in the background.

---

## Features

- **Simple Notepad Interface**: Create, edit, and save text files as you would in any basic text editor.
- **Integrated Chess Engine**: Play chess against a CPU (Stockfish) directly within the text editor.
- **Concealed Gameplay**: Enter chess moves in UCI format (e.g., `e2e4`) while taking notes, and see the CPU's response printed in the next line.
- **Lightweight and Minimalistic**: Perfect for casual chess games without needing a full GUI.

---

## Getting Started

### Prerequisites

- **Python 3.10 or higher**
- **Dependencies**:
  - `tkinter` (comes pre-installed with most Python distributions)
  - `python-chess`
  - Stockfish Chess Engine

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/notepad-chess.git
   cd notepad-chess
   ```

2. Install the required Python library:
   ```bash
   pip install python-chess
   ```

3. Download and install Stockfish:
   - Download Stockfish from [https://stockfishchess.org/download/](https://stockfishchess.org/download/).
   - Extract the downloaded archive and locate the `stockfish.exe` file.

4. Update the code with the path to the Stockfish executable:
   ```python
   self.engine = chess.engine.SimpleEngine.popen_uci("C:\\Path\\To\\Stockfish\\stockfish.exe")
   ```

5. Run the application:
   ```bash
   python NotepadChess.py
   ```

---

## How to Play

1. Open the application.
2. Start typing your chess moves in UCI format (e.g., `e2e4`).
3. Press `Enter` after each move.
4. The CPU will respond with its move in the next line.
5. Continue taking notes or playing chess seamlessly!

---

## Example Gameplay

```
My meeting notes for today:
- Discuss project timeline.
- Follow up on deliverables.

Let's play some chess now:
e2e4
CPU: e7e5

Back to notes:
- Remember to email the client.
```

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the app.

### To Do:
- Add a game summary feature.
- Improve move validation messages.
- Introduce customizable themes for the editor.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **[python-chess](https://python-chess.readthedocs.io/)**: For enabling chess functionality.
- **[Stockfish](https://stockfishchess.org/)**: For being an incredibly powerful open-source chess engine.

---

Happy playing and note-taking! 📝♟️
