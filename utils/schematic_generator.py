import random
from mcschematic import MCSchematic, Version


class SchematicGenerator:
    def __init__(self, maze, name, wall_blocks = None):
        self.name = name
        self.maze = maze
        self.schem = MCSchematic()
        self.grid = self.maze.grid

        self.wall_blocks = ["minecraft:stone"] if not wall_blocks else wall_blocks
        self.path_block = "minecraft:air"
        self.start_block = "minecraft:gold_block"
        self.end_block = "minecraft:emerald_block"
        self.start = self.maze.start
        self.end = self.maze.end
        self.wall_height = 4
        self.wall_thickness = 2
        self.path_width = 2
    
    def __start_schematic_generation(self):
        for z, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                block_type = random.choice(self.wall_blocks) if cell == 1 else self.path_block
                if self.start == (z,x):
                    block_type = self.start_block
                if self.end == (z,x):
                    block_type = self.end_block
                for y in range(self.wall_height):
                    for dx in range(self.path_width if cell == 0 else self.wall_thickness):
                        for dz in range(self.path_width if cell == 0 else self.wall_thickness):
                            self.schem.setBlock((x * self.path_width + dx, y, z * self.path_width + dz), block_type)
    
    def __save_schematic(self):
        self.schem.save("",f"{self.name}_maze_schematic",Version.JE_1_20_1)
    
    def generate_schematic(self):
        self.__start_schematic_generation()
        self.__save_schematic()
        return self.name

if __name__ == '__main__':
    from utils.maze_generator import MazeGenerator
    t = MazeGenerator(25,25)
    name, maze = t.generate_maze()
    m = SchematicGenerator(maze, name)
    print(m.generate_schematic())
