from uuid import uuid4
from mazelib import Maze
from PIL import Image, ImageDraw
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver


class MazeGenerator:
    def __init__(self, height = 25, width = 25):
        self.name = uuid4()
        self.maze = Maze()

        self.height = height
        self.width = width
        self.__initiate_maze()
        self.solution = self.maze.solutions[0]
        self.grid = self.maze.grid

        self.start = self.maze.start
        self.end = self.maze.end
    
    def __initiate_maze(self):
        self.maze.solver = BacktrackingSolver()
        self.maze.generator = Prims(self.height, self.width)
        self.maze.generate()
        self.maze.generate_entrances()
        self.maze.solve()
    
    def __maze_to_png(self, file_name, is_solution=False):
        cell_size = 20
        width = len(self.maze.grid[0]) * cell_size
        height = len(self.maze.grid) * cell_size
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        for y in range(len(self.maze.grid)):
            for x in range(len(self.maze.grid[y])):
                if self.maze.grid[x][y] == 1:
                    draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill="black")
                if (x,y) == self.start:
                    draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill="red")
                if (x,y) == self.end:
                    draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill="lime")
        if is_solution:
            for (x, y) in self.solution:
                draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill="blue")
        img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        img.save(file_name)
    
    def __generate_maze_image_and_solution(self):
        self.__maze_to_png(f"{self.name}_maze.png")
        self.__maze_to_png(f"{self.name}_solution.png", True)
    
    def generate_maze(self):
        self.__generate_maze_image_and_solution()
        return self.name, self.maze

if __name__ == '__main__':
    m = MazeGenerator(30,30)
    m.generate_maze()
