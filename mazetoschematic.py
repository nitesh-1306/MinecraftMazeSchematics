from mazelib import Maze
from PIL import Image, ImageDraw
from mazelib.generate.Prims import Prims
from mcschematic import MCSchematic, Version
from mazelib.solve.BacktrackingSolver import BacktrackingSolver


class MazeToSchematic:
    def __init__(self, height = 25, width = 25):
        self.maze = Maze()
        self.schem = MCSchematic()

        self.height = height
        self.width = width
        self.__initiate_maze()
        self.solution = self.maze.solutions[0]
        self.grid = self.maze.grid

        self.wall_block = "minecraft:stone"
        self.path_block = "minecraft:air"
        self.start_block = "minecraft:gold_block"
        self.end_block = "minecraft:emerald_block"
        self.start = self.maze.start
        self.end = self.maze.end
        self.wall_height = 4
        self.wall_thickness = 2
        self.path_width = 2
    
    def __initiate_maze(self):
        self.maze.solver = BacktrackingSolver()
        self.maze.generator = Prims(self.height, self.width)
        self.maze.generate()
        self.maze.generate_entrances()
        self.maze.solve()
    
    def __start_schematic_generation(self):
        for z, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                block_type = self.wall_block if cell == 1 else self.path_block
                if self.start == (z,x):
                    block_type = self.start_block
                if self.end == (z,x):
                    block_type = self.end_block
                for y in range(self.wall_height):
                    for dx in range(self.path_width if cell == 0 else self.wall_thickness):
                        for dz in range(self.path_width if cell == 0 else self.wall_thickness):
                            self.schem.setBlock((x * self.path_width + dx, y, z * self.path_width + dz), block_type)
    
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
    
    def __generate_schematic(self):
        self.schem.save("","maze_schematic",Version.JE_1_20_1)
    
    def __generate_maze_image_and_solution(self):
        self.__maze_to_png("maze.png")
        self.__maze_to_png("solution.png", True)
    
    def start_generation(self):
        self.__start_schematic_generation()
        self.__generate_schematic()
        self.__generate_maze_image_and_solution()

if __name__ == '__main__':
    m = MazeToSchematic(30,30)
    m.start_generation()
