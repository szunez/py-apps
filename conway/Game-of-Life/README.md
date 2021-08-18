# Conway's Game of Life

The Game of Life is a cellular automaton created by John H. Conway in 1970. The game is a zero-player game in which an initially configured 2D grid of cells evolves according to the Game of Life [ruleset](#Ruleset).

Built using Python 3.5, this implementation of Conway's Game of Life allows the user to easily run a choosen number of generations of the Game of Life using a 2D grid of choosen number of rows and columns in either a Linux or Windows terminal/console.

This project is licensed under the terms of the MIT license.

## Ruleset

Using the following ruleset the 2D grid of cells will evolve from generation to generation until it reaches a static state of either all dead cells or a mix of still, oscillating, or moving (spaceship) cells.

1. _**Underpopulation**_ - If a live cell has is surrounded by less than two surrounding neighbours it dies and does not make it to the next generation.
2. _**Equilibrium**_ - If a live cell is surrounded by two or three living neighbors the cell stays alive and makes it to the next generation.
3. _**Overpopulation**_ - If a live cell is surrounded by more than three living neighbors the cell dies and does not make it to the next generation.
4. _**Reproduction**_ - If a dead cell is surrounded by three living neighbors the cell stays alive and makes it to the next generation.

## How to Run

This project is built using Python 3.5 and requires that the user has at least Python 3 installed in order to run the program. Python 3+ can be installed [here](https://www.python.org/downloads/).

In order to run this project the user must open a terminal/console and navigate to the project folder and then into the script directory. Once inside of the script directory simply run **`python main.py`** in order to begin the program.

Once the program has been started the user will be prompted to input the number of **rows** and **columns** to make the Game of Life grid. After the user has decided on the grid's shape they must enter the number of **generations** to run the game for and then they will be presented with a randomized Game of Life grid that continuously evolves until all cells are dead, still, or the generations are over.

### Example Output
![Example Output](https://zj0l5w-sn3301.files.1drv.com/y3mCRjxuvhMBzKsaDbamx6HlqF5_oUOjGp0ExWsPaHEMhMk9m2fLgwrYKHLH4-1Ye3Dq3Cy9H_icYXxaaBdBV_GuABpNuv8B0Q6rxaLhE2jYnZ0LhCO-PdDs25j2vkSoJfZRA_2SwJPH8YYOT7RULaZ7voqsYK5vlENs2sNoY3ggK8?width=514&height=433&cropmode=none)
