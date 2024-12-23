import tkinter as tk
from tkinter import messagebox
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import matplotlib.pyplot as plt
import numpy as np

class MazeEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Rectangular Maze Editor")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Define dimensions for different sections
        self.horizontal_size = (10, 50)  # height, width for top/bottom
        self.vertical_size = (10, 10)    # height, width for sides
        
        # Calculate full maze dimensions
        self.rows = self.horizontal_size[0] * 2 + self.vertical_size[0]
        self.cols = self.horizontal_size[1]

        # Generate full maze first
        self.generate_full_maze()

        # Cell size for drawing
        self.cell_size = 20

        # Create main container frame
        self.container = tk.Frame(master)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Create button frame at the top
        self.button_frame = tk.Frame(self.container)
        self.button_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Add buttons to button frame
        tk.Button(self.button_frame, text="Save Maze", command=self.save_images).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.button_frame, text="Regenerate Maze", command=self.regenerate_mazes).pack(side=tk.LEFT, padx=5, pady=5)

        # Create frame for canvas and scrollbars
        self.frame = tk.Frame(self.container)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas with scrollbars
        self.canvas = tk.Canvas(
            self.frame,
            width=min(self.cols * self.cell_size, 800),
            height=min(self.rows * self.cell_size, 600)
        )

        # Create scrollbars
        self.scrollbar_y = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)

        # Configure canvas scrolling
        self.canvas.configure(
            xscrollcommand=self.scrollbar_x.set,
            yscrollcommand=self.scrollbar_y.set,
            scrollregion=(0, 0, self.cols * self.cell_size, self.rows * self.cell_size)
        )

        # Grid layout for canvas and scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Configure frame grid weights
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.canvas.bind("<B1-Motion>", self.toggle_cell)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)
        self.canvas.bind("<Button-5>", self.on_mousewheel)

        # Draw initial maze
        self.draw_maze()

    def generate_full_maze(self):
        # Generate a single large maze
        maze = Maze()
        maze.generator = Prims(self.rows, self.cols)
        maze.generate()
        
        # Store the generated maze
        self.maze = maze.grid
        
        # Create entrance and exit
        self.maze[0, 1] = 0  # entrance at top
        self.entrance = (0, 1)
        
        center_y = self.rows // 2
        center_x = self.cols // 2
        self.maze[center_y, center_x] = 0  # exit in center
        self.exit = (center_y, center_x)

    def on_mousewheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def regenerate_mazes(self):
        self.generate_full_maze()
        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if (i, j) == self.entrance:
                    color = "green"
                elif (i, j) == self.exit:
                    color = "red"
                else:
                    color = "black" if self.maze[i][j] == 1 else "white"
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="gray",
                    tags="cell"
                )

    def toggle_cell(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        col = int(canvas_x // self.cell_size)
        row = int(canvas_y // self.cell_size)

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.maze[row][col] = 1 - self.maze[row][col]
            self.draw_maze()

    def save_images(self):
        # Save maze without solution
        maze_array = np.array(self.maze)
        maze_array[self.entrance[0]][self.entrance[1]] = 0.7
        maze_array[self.exit[0]][self.exit[1]] = 0.3
        
        plt.figure(figsize=(15, 10))
        plt.imshow(maze_array, cmap="binary")
        plt.axis("off")
        plt.savefig("rectangular_maze.png", bbox_inches='tight', dpi=300)
        plt.close()

        # Create solution
        maze_solver = Maze()
        maze_solver.grid = self.maze
        maze_solver.start = self.entrance
        maze_solver.end = self.exit
        maze_solver.solver = BacktrackingSolver()
        maze_solver.solve()

        solution_maze = np.array(self.maze, dtype=float)
        if maze_solver.solutions:
            for x, y in maze_solver.solutions[0]:
                solution_maze[x][y] = 0.5

        solution_maze[self.entrance[0]][self.entrance[1]] = 0.7
        solution_maze[self.exit[0]][self.exit[1]] = 0.3

        cmap = plt.cm.binary
        cmap.set_under("green")
        cmap.set_over("red")

        plt.figure(figsize=(15, 10))
        plt.imshow(solution_maze, cmap=cmap, vmin=0, vmax=1)
        plt.axis("off")
        plt.savefig("rectangular_maze_with_solution.png", bbox_inches='tight', dpi=300)
        plt.close()

        messagebox.showinfo("Saved", "Maze and solution have been saved!")

    def on_close(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    editor = MazeEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()