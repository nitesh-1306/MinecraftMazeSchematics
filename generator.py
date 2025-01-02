from utils.maze_generator import MazeGenerator
from utils.schematic_generator import SchematicGenerator
from utils.cloud_storage import CloudStorage


class Generator:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.maze_generator = MazeGenerator(height, width)
        self.schematic_generator = None
        self.cloud = CloudStorage()
    
    def generate(self):
        ...