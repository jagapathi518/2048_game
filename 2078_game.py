# ```python

import tkinter as tk
import random


class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.master.resizable(False, False)
        self.master.configure(bg="#faf8ef")

        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False

        self.colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }

        self.score_label = tk.Label(
            master,
            text="Score: 0",
            font=("Helvetica", 16, "bold"),
            bg="#faf8ef",
        )
        self.score_label.grid(
            row=0, column=0, columnspan=4, pady=(10, 5)
        )

        self.tiles = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                tile = tk.Label(
                    master,
                    text="",
                    font=("Helvetica", 24, "bold"),
                    width=5,
                    height=2,
                    bg=self.colors[0],
                    fg="#776e65",
                    relief="flat",
                )
                tile.grid(row=i + 1, column=j, padx=4, pady=4)
                row.append(tile)
            self.tiles.append(row)

        self.message_label = tk.Label(
            master,
            text="Use the arrow keys to play",
            font=("Helvetica", 10),
            bg="#faf8ef",
        )
        self.message_label.grid(
            row=5, column=0, columnspan=4, pady=5
        )

        self.restart_button = tk.Button(
            master,
            text="New Game",
            command=self.restart,
        )
        self.restart_button.grid(
            row=6, column=0, columnspan=4, pady=(0, 10)
        )

        self.master.bind("<KeyPress>", self.handle_key)
        self.master.bind("<Button-1>", self.focus_window)

        self.restart()

    def focus_window(self, event):
        self.master.focus_set()

    def restart(self):
        self.grid = [
            [0] * self.grid_size
            for _ in range(self.grid_size)
        ]
        self.score = 0
        self.game_over = False
        self.add_tile()
        self.add_tile()
        self.update_grid()
        self.message_label.config(
            text="Use the arrow keys to play"
        )
        self.master.focus_set()

    def add_tile(self):
        empty_cells = [
            (i, j)
            for i in range(self.grid_size)
            for j in range(self.grid_size)
            if self.grid[i][j] == 0
        ]

        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = (
                2 if random.random() < 0.9 else 4
            )

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                tile = self.tiles[i][j]

                tile.config(
                    text=str(value) if value else "",
                    bg=self.colors.get(value, "#3c3a32"),
                    fg="#776e65" if value <= 4 else "#ffffff",
                )

        self.score_label.config(text=f"Score: {self.score}")
        self.master.update_idletasks()

    @staticmethod
    def compress(row):
        """Move all nonzero values to the left."""
        return [value for value in row if value != 0] + [
            0
        ] * row.count(0)

    def merge_row(self, row):
        """Merge equal adjacent tiles once per move."""
        row = self.compress(row)
        merged = []
        gained_score = 0
        i = 0

        while i < len(row):
            if (
                i + 1 < len(row)
                and row[i] == row[i + 1]
                and row[i] != 0
            ):
                value = row[i] * 2
                merged.append(value)
                gained_score += value
                i += 2
            else:
                merged.append(row[i])
                i += 1

        merged += [0] * (self.grid_size - len(merged))
        return merged, gained_score

    @staticmethod
    def transpose(matrix):
        return [list(row) for row in zip(*matrix)]

    @staticmethod
    def reverse(matrix):
        return [row[::-1] for row in matrix]

    def move_tiles(self, direction):
        old_grid = [row[:] for row in self.grid]
        gained_score = 0

        if direction in ("Up", "Down"):
            working_grid = self.transpose(self.grid)

            if direction == "Down":
                working_grid = self.reverse(working_grid)

            new_grid = []
            for row in working_grid:
                merged_row, gained = self.merge_row(row)
                new_grid.append(merged_row)
                gained_score += gained

            if direction == "Down":
                new_grid = self.reverse(new_grid)

            self.grid = self.transpose(new_grid)

        else:
            working_grid = [row[:] for row in self.grid]

            if direction == "Right":
                working_grid = self.reverse(working_grid)

            new_grid = []
            for row in working_grid:
                merged_row, gained = self.merge_row(row)
                new_grid.append(merged_row)
                gained_score += gained

            if direction == "Right":
                new_grid = self.reverse(new_grid)

            self.grid = new_grid

        if self.grid != old_grid:
            self.score += gained_score
            self.add_tile()
            self.update_grid()

            if self.check_game_over():
                self.game_over = True
                self.message_label.config(
                    text="Game Over! Click New Game to restart."
                )

    def handle_key(self, event):
        if self.game_over:
            return

        if event.keysym in ("Up", "Down", "Left", "Right"):
            self.move_tiles(event.keysym)

    def check_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False

                if (
                    j + 1 < self.grid_size
                    and self.grid[i][j] == self.grid[i][j + 1]
                ):
                    return False

                if (
                    i + 1 < self.grid_size
                    and self.grid[i][j] == self.grid[i + 1][j]
                ):
                    return False

        return True


def main():
    root = tk.Tk()
    Game2048(root)
    root.mainloop()


if __name__ == "__main__":
    main()
# ```python 