# Tetris AI
Tetris AI Bot using computer vision to play game automatically
* `bot.py` is the main application.
* `criteria.py` is AI part, includes fitness function and attributes
* `recognition.py` is the Computer Vision 
* `tetromino.py` is the some information about tetrominoes (shape, color, start position).


[![Watch the video](https://www.youtube.com/s/desktop/40777624/img/favicon_96x96.png)](https://www.youtube.com/watch?v=PIeq2S0EXQ0) 
*click on the picture to see the demo*
## Computer Vision

How it works? 
When bot started he try to find game aplication and wait until game is started. When game is started bot detectes the board, the tetrominoes in the game using Opencv. Grabs the images in realtime and transfroms board to bollean matrix (0 - empty cell , 1 - occupied cell) and identify current tetromino...

## AI algorithm
When all information about the board is known, AI determines all possible positions of the current tetromino on the board. Choose the best possible position via fitness function and transmits all the necessary moves by emulating keystrokes on the keyboard.
#### Fitness function parameters:
- **Height** - maximum height of the grid.
- **Aggregate Height** - the sum of the height of each column
- **Number of lines cleared** - the number of complete lines in the grid.
- **Number of holes** - empty space such that there is at least one tile in the same column above.
- **Bumpiness** - sum of the difference between heights of adjacent pairs of columns.
