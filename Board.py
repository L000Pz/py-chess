import tkinter as tk
from PIL import Image, ImageTk
import pieces


piece_names = ["Bb", "Wb", "Bk", "Wk", "Bn",
               "Wn", "bp", "wp", "Bq", "Wq", "Br", "Wr"]


image_paths = [
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_bdt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_blt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_kdt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_klt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_ndt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_nlt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_pdt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_plt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_qdt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_qlt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_rdt60.png",
    "/Users/amiraliseyedzadegan/Documents/internalprojects/Python/Chess Game/img/Chess_rlt60.png"
]


class chess_game:
    def __init__(self):

        self.window = tk.Tk()

        self.window.title("Chess Game")
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.pack(side=tk.LEFT)

        self.move_history_frame = tk.Frame(self.window, width=200)
        self.move_history_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.move_history_text = tk.Text(self.move_history_frame, wrap=tk.WORD)
        self.move_history_text.pack(fill=tk.BOTH, expand=True)
        self.piece_images = {name: ImageTk.PhotoImage(Image.open(
            path)) for name, path in zip(piece_names, image_paths)}

        self.selected_piece = None

        self.create_board()

        self.canvas.bind("<Button-1>", self.on_click)

        self.window.mainloop()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                x1 = row * 50
                y1 = col * 50
                x2 = x1 + 50
                y2 = y1 + 50

                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color)
                piece_name = pieces.chessboard[col][row]
                if piece_name in self.piece_images:
                    self.canvas.create_image(
                        (x1 + x2) / 2, (y1 + y2) / 2, image=self.piece_images[piece_name])

    def on_click(self, event):
        x, y = event.x, event.y
        col = x // 50
        row = y // 50

        piece_name = pieces.chessboard[col][row]

        if not self.selected_piece and piece_name:
            self.selected_piece = (piece_name, col, row)
        elif self.selected_piece:
            selected_name, selected_col, selected_row = self.selected_piece
            pieces.chessboard[col][row] = selected_name
            pieces.chessboard[selected_col][selected_row] = ""
            self.create_board()

        square = f"{chr(97 + col)}{8 - row}"
        move = f"Moved to {square}"

        self.move_history_text.insert(tk.END, move + "\n")
        self.move_history_text.see(tk.END)


if __name__ == "__main__":
    chess_game()
