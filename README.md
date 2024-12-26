# Maze to Minecraft Schematic Generator

A Flask web application that generates mazes and converts them into Minecraft schematic files. Users can specify the maze dimensions and height, and receive a zip file containing the maze visualization, solution path, and a Minecraft schematic file ready for importing into the game.

## Features

- Generate random mazes using the `mazelib` library
- Convert mazes into Minecraft schematic files using `msschematic`
- Customize maze dimensions (width, length) and height
- Download results as a ZIP file containing:
  - PNG visualization of the maze
  - PNG visualization of the solution
  - Minecraft schematic file (.schem)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/maze-schematic-generator
cd maze-schematic-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.8+
- Flask
- mazelib
- msschematic
- Pillow
- numpy

All dependencies are listed in `requirements.txt`

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter the desired maze dimensions:
   - Width (blocks)
   - Length (blocks)
   - Height (blocks)

4. Click "Generate Maze" to create and download your maze package

## Project Structure

```
maze-schematic-generator/
├── examples/
├── app.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   ├── index.html
│   └── error.html
└── utils/
    ├── maze_generator.py
    ├── cloud_storage.py
    └── schematic_converter.py
```

## API Reference

### Main Route

- **URL**: `/`
- **Method**: `GET`
- **Description**: Renders the main page with the maze generation form

### Generate Maze

- **URL**: `/generate`
- **Method**: `POST`
- **Parameters**:
  - `width` (integer): Maze width in blocks
  - `length` (integer): Maze length in blocks
  - `height` (integer): Maze height in blocks
- **Response**: ZIP file containing maze files
- **Error Response**: 400 Bad Request if parameters are invalid
