from mazelib import Maze
from mazelib.generate.Prims import Prims
from mcschematic import MCSchematic, Version

maze = Maze()
maze.generator = Prims(25, 25)
maze.generate()

grid = maze.grid

schem = MCSchematic()

wall_block = "minecraft:stone"
path_block = "minecraft:air"
height = 4
wall_thickness = 2
path_width = 2

for z, row in enumerate(grid):
    for x, cell in enumerate(row):
        block_type = wall_block if cell == 1 else path_block
        for y in range(height):
            # Scale x and z to account for 2-block-wide paths
            for dx in range(path_width if cell == 0 else wall_thickness):
                for dz in range(path_width if cell == 0 else wall_thickness):
                    schem.setBlock((x * path_width + dx, y, z * path_width + dz), block_type)

schem.save("","25x25_maze",Version.JE_1_20_1)
print("Schematic saved as '25x25_maze.schem'")
