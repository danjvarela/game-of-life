"""
A program to implement Conway's Game of Life.

Available commands:
  left click:       spawn a cell
  right click:      kill a cell
  left mouse drag:  spawn cells
  right mouse drag: kill cells
  space:            start the game
  q:                stop the game
  r:                randomize the grid
  b:                blank the grid
  g:                generate a gosper glider gun
  n:                next generation
"""

from p5 import *
import numpy as np
from sample_patterns import *

global width, height
pixelPerTile = 10 # size of each tile
col = None
row = None
grid = None
BLACK = 40, 44, 52
WHITE = 171, 178, 191
tileWithChanges = [] # keeps track of tiles that have changed


# generates a random col x row array of 1s and 0s
def randomGrid(col, row):
  return np.random.randint(0, 2, (row, col), dtype=int)


# generates col x row array with values set to 0
def blankGrid(col, row):
  return np.zeros((row, col), dtype=int)


# renders the supplied grid of col x row list of 1s and 0s
def renderGrid(grid):
  gridArr = np.nditer(grid, flags=['multi_index'])
  for element in gridArr:
    renderTile(gridArr.multi_index[1], gridArr.multi_index[0])


# render a specific tile
def renderTile(col, row):
  no_stroke()
  if grid[row, col] == 1:
    fill(*WHITE)
  else:
    fill(*BLACK)
  rect(col * pixelPerTile, row * pixelPerTile, pixelPerTile - 1, pixelPerTile - 1)


# updates the grid by applying the rules of the game
def updateGrid():
  global grid, tileWithChanges, col, row
  neighborCount = 0 # tracks number of neighbors
  paddedGrid = np.pad(grid, 1, mode='constant') # surround the grid with 0s
  newGrid = grid.copy()
  for c in range(1, col + 1):
    for r in range(1, row + 1):
      neighborCount = np.sum([
        paddedGrid[r - 1, c - 1], paddedGrid[r - 1, c], paddedGrid[r - 1, c + 1],
        paddedGrid[r, c - 1], paddedGrid[r, c + 1],
        paddedGrid[r + 1, c - 1], paddedGrid[r + 1, c], paddedGrid[r + 1, c + 1]
      ])
      if grid[r-1, c-1] == 1: # cell alive
        if neighborCount < 2 or neighborCount > 3:
          newGrid[r-1, c-1] = 0 # kill cell
          tileWithChanges.append((r-1, c-1)) # add this to tileWithChanges
      else: # cell dead
        if neighborCount == 3:
          newGrid[r-1, c-1] = 1 # spawn cell
          tileWithChanges.append((r-1, c-1)) # add this to tileWithChanges
  grid = newGrid # update grid


# generate a pattern
def generatePattern(pattern):
  global grid
  for element in pattern:
    grid[element[0], element[1]] = 1 


def setup():
  no_loop()
  size(500, 500)
  global col, row, grid
  col = int(width / pixelPerTile)
  row = int(height / pixelPerTile)
  grid = blankGrid(col, row)
  

firstLoop = True
loopMode = False # somehow, draw is called one more time after no_loop() is called
def draw():
  global firstLoop, tileWithChanges
  if firstLoop:
    background(0)
    renderGrid(grid) # render the grid on the first loop
    firstLoop = False

  if loopMode:
    updateGrid()
    for tile in tileWithChanges: # render tileWithChanges
      renderTile(tile[1], tile[0])
    tileWithChanges.clear() # reset tileWithChanges


# spawns/kills a cell when mouse is clicked
def mouse_pressed():
  global mouse_x, mouse_y, mouse_button, grid
  col = int(mouse_x / pixelPerTile)
  row = int(mouse_y / pixelPerTile)

  if mouse_button == "LEFT":
    if grid[row, col] == 0: grid[row, col] = 1 # if cell is dead, make it alive
  elif mouse_button == "RIGHT":
    if grid[row, col] == 1: grid[row, col] = 0 # if cell is alive, make it dead
  renderTile(col, row)


# spawns cells when mouse is dragged
def mouse_dragged():
  global mouse_x, mouse_y, mouse_button, grid
  col = int(mouse_x / pixelPerTile)
  row = int(mouse_y / pixelPerTile)
  if mouse_button == "LEFT":
    if grid[row, col] == 0: grid[row, col] = 1  # if cell is dead, make it alive
  elif mouse_button == "RIGHT":
    if grid[row, col] == 1: grid[row, col] = 0  # if cell is alive, kill it
  renderTile(col, row)


# runs the game of life
def key_pressed():
  global grid, key, col, row, firstLoop, loopMode
  if key == ' ':
    loopMode = True
    loop() # start the game
  elif key == 'q':
    loopMode = False
    no_loop() # stop the game
  elif key == 'r':
    loopMode = False
    no_loop()
    grid = randomGrid(col, row) # randomize the grid
    renderGrid(grid)
  elif key == 'b':
    loopMode = False
    no_loop()
    grid = blankGrid(col, row) # blank the grid
    renderGrid(grid)
  elif key == 'g': # generate a glider
    loopMode = False
    no_loop()
    generatePattern(gosper_glider_gun)
    renderGrid(grid)
  elif key =='n': # next generation
    loopMode = True # set loopMode to true so that updateGrid() is called
    no_loop()
    redraw()



if __name__ == "__main__":
  builtins.title = "Conway's Game of Life"
  run(frame_rate)