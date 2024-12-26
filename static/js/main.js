function generateMaze() {
    const genButton = document.getElementById('generate');
    genButton.innerText = "Generating...";
    setTimeout(() => {
    genButton.innerText = "Generate Maze";
        const width = document.getElementById('width').value;
        const height = document.getElementById('height').value;

        const mazeContainer = document.getElementById('mazeContainer');
        mazeContainer.classList.add('visible');
    }, 2000);

}

function downloadMaze() {
    alert('Download functionality would go here!');
}