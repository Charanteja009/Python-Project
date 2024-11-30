import tkinter as tk
from tkinter import ttk
import random


TILE_COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2")
}


class Game2048:
    def __init__(self):
        self.size = 4
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.add_new_tile()
        self.add_new_tile()
        self.score = 0
        self.history = []

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = random.choice([2, 4])

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (len(row) - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(len(row) - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        self.save_state()
        for r in range(self.size):
            self.grid[r] = self.compress(self.grid[r])
            self.grid[r] = self.merge(self.grid[r])
            self.grid[r] = self.compress(self.grid[r])
        self.add_new_tile()

    def move_right(self):
        self.save_state()
        for r in range(self.size):
            self.grid[r] = self.compress(self.grid[r][::-1])
            self.grid[r] = self.merge(self.grid[r])
            self.grid[r] = self.compress(self.grid[r])
            self.grid[r].reverse()
        self.add_new_tile()

    def move_up(self):
        self.save_state()
        for c in range(self.size):
            col = [self.grid[r][c] for r in range(self.size)]
            col = self.compress(col)
            col = self.merge(col)
            col = self.compress(col)
            for r in range(self.size):
                self.grid[r][c] = col[r]
        self.add_new_tile()

    def move_down(self):
        self.save_state()
        for c in range(self.size):
            col = [self.grid[r][c] for r in range(self.size)]
            col = self.compress(col[::-1])
            col = self.merge(col)
            col = self.compress(col)
            col.reverse()
            for r in range(self.size):
                self.grid[r][c] = col[r]
        self.add_new_tile()

    def save_state(self):

        self.history.append((self.grid, self.score))

    def undo(self):
        if self.history:
            self.grid, self.score = self.history.pop()
        self.add_new_tile()

    def game_over(self):
        for row in self.grid:
            for num in row:
                if num == 0:
                    return False
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return False
        for r in range(self.size - 1):
            for c in range(self.size):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True



class Game2048App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2048 Game")
        self.geometry("400x500")
        self.game = Game2048()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Start Screen
        self.start_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.start_frame, text="Start Game")
        self.start_label = ttk.Label(self.start_frame, text="Welcome to 2048!", font=("Arial", 24))
        self.start_label.pack(pady=50)
        self.start_button = ttk.Button(self.start_frame, text="Start", command=self.show_game_screen)
        self.start_button.pack()

        # Game Screen
        self.game_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.game_frame, text="Play")
        self.grid_labels = []
        for r in range(4):
            row_labels = []
            for c in range(4):
                label = tk.Label(self.game_frame, text='', font=("Arial", 24), width=4, height=2, relief="solid", anchor="center")
                label.grid(row=r, column=c, padx=5, pady=5)
                row_labels.append(label)
            self.grid_labels.append(row_labels)

        self.score_label = ttk.Label(self.game_frame, text="Score: 0", font=("Arial", 18))
        self.score_label.grid(row=4, column=0, columnspan=4, pady=10)

        self.bind("<Key>", self.key_press)
        self.update_grid()

        # Undo Button
        self.undo_button = ttk.Button(self.game_frame, text="Undo", command=self.undo_move)
        self.undo_button.grid(row=5, column=0, columnspan=4, pady=10)

        # Game Over Screen
        self.over_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.over_frame, text="Game Over")
        self.over_label = ttk.Label(self.over_frame, text="Game Over!", font=("Arial", 24))
        self.over_label.pack(pady=50)
        
        # Add Score to Game Over Screen
        self.final_score_label = ttk.Label(self.over_frame, text="Final Score: 0", font=("Arial", 18))
        self.final_score_label.pack(pady=10)

        self.restart_button = ttk.Button(self.over_frame, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        self.notebook.hide(self.game_frame)
        self.notebook.hide(self.over_frame)

    def show_game_screen(self):
        self.notebook.hide(self.start_frame)
        self.notebook.add(self.game_frame, text="Play")
        self.notebook.select(self.game_frame)

    def show_game_over_screen(self):
        self.notebook.hide(self.game_frame)
        self.notebook.add(self.over_frame, text="Game Over")
        self.notebook.select(self.over_frame)

        self.final_score_label.config(text=f"Final Score: {self.game.score}")

    def key_press(self, event):
        if not self.game.game_over():
            if event.keysym == 'Left':
                self.game.move_left()
            elif event.keysym == 'Right':
                self.game.move_right()
            elif event.keysym == 'Up':
                self.game.move_up()
            elif event.keysym == 'Down':
                self.game.move_down()
            self.update_grid()

        if self.game.game_over():
            self.show_game_over_screen()

    def update_grid(self):
        for r in range(4):
            for c in range(4):
                num = self.game.grid[r][c]
                text = str(num) if num != 0 else ''
                bg_color, fg_color = TILE_COLORS.get(num, ("#cdc1b4", "#776e65"))
                self.grid_labels[r][c].config(text=text, bg=bg_color, fg=fg_color)
  
        self.score_label.config(text=f"Score: {self.game.score}")

    def undo_move(self):
        self.game.undo()
        self.update_grid()

    def restart_game(self):
        self.game = Game2048()
        self.update_grid()
        self.notebook.hide(self.over_frame)
        self.notebook.add(self.start_frame, text="Start Game")
        self.notebook.select(self.start_frame)


if __name__ == "__main__":
    app = Game2048App()
    app.mainloop()
