import tkinter as tk
from tkinter import messagebox
from mazelib import Maze
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import matplotlib.pyplot as plt
import numpy as np

class MazeEditor:
    def __init__(self, master, maze):
        self.master = master
        self.master.title("Maze Editor")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame, width=min(self.cols * 20, 800), height=min(self.rows * 20, 600), bg="white")

        self.scroll_x = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.config(scrollregion=(0, 0, self.cols * 20, self.rows * 20))

        self.draw_maze()

        self.canvas.bind("<Button-1>", self.toggle_cell)

        tk.Button(master, text="Save Maze", command=self.save_images).pack()

    def draw_maze(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) == getattr(self, 'start', (-1, -1)):
                    color = "red"
                elif (i, j) == getattr(self, 'end', (-1, -1)):
                    color = "green"
                else:
                    color = "black" if self.maze[i][j] == 1 else "white"
                self.canvas.create_rectangle(
                    j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=color, outline="gray"
                )

    def toggle_cell(self, event):
        col = int(self.canvas.canvasx(event.x) // 20)
        row = int(self.canvas.canvasy(event.y) // 20)

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.maze[row][col] = 1 - self.maze[row][col]  # Toggle between 0 and 1
            self.draw_maze()

    def save_images(self):
        # Save the maze as an image
        maze_array = np.array(self.maze)
        plt.imshow(maze_array, cmap="binary")
        plt.axis("off")
        plt.savefig("maze.png", bbox_inches='tight')
        
        # Solve the maze
        maze_solver = Maze()
        maze_solver.grid = self.maze
        maze_solver.generate_entrances()
        maze_solver.solver = BacktrackingSolver()
        maze_solver.solve()

        # Set start and end points
        self.start = maze_solver.start
        self.end = maze_solver.end
        
        # Overlay the solution on the maze
        solution_path = maze_solver.solution
        solution_maze = np.array(self.maze, dtype=float)
        for x, y in solution_path:
            solution_maze[x][y] = 0.5  # Mark the solution path

        # Mark the start and end points
        solution_maze[self.start[0]][self.start[1]] = 0.7  # Start in red
        solution_maze[self.end[0]][self.end[1]] = 0.3    # End in green

        cmap = plt.cm.binary
        cmap.set_under("red")
        cmap.set_over("green")

        plt.imshow(solution_maze, cmap=cmap, vmin=0, vmax=1)
        plt.axis("off")
        plt.savefig("maze_with_solution.png", bbox_inches='tight')

        messagebox.showinfo("Saved", "Maze and solution images have been saved!")

        # Redraw the maze with updated start and end points
        self.draw_maze()

    def on_close(self):
        self.master.destroy()


def generate_maze():
    # Create a larger grid with space for a square
    maze = [[0 for _ in range(15)] for _ in range(15)]

    # Define a square pattern in the center
    for i in range(1, 4):
        for j in range(1, 4):
            maze[i][j] = 1

    return maze

def main():
    maze_grid = generate_maze()

    root = tk.Tk()
    editor = MazeEditor(root, maze_grid)
    root.mainloop()

if __name__ == "__main__":
    main()
