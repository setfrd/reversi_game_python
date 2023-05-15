# reversi_game_python
Reversi AI - A Game-playing Program
This is a program that plays Reversi, a board game for two players, using an AI algorithm. The goal of the game is to have the most pucks of your color on the board at the end.

Game Rules
The game is played on an 8x8 board.
Two players take turns placing their colored pucks on the board.
A player's move must form a straight line where their pucks are at both ends, and the opponent's pucks are in between.
When a player creates such a line, all the opponent's pucks located in the middle of the line are flipped to their color.
The game continues until the board is completely filled with pucks.
The player with the most pucks of their color on the board wins.
Program Features
The program includes the following features:

Game State and Move Generation:

The game state is represented by an 8x8 board where each field can be empty (0) or occupied by a player's disc (1 or 2).
A function generates possible moves for the current state and player.
Heuristics:

The program includes multiple strategies to assess the state of the game for each player.
Each player has at least three different strategies to adapt their gameplay.
Minimax Algorithm (Player 1's Perspective):

The program implements the Minimax algorithm, an AI search algorithm, from the perspective of Player 1.
Minimax evaluates the game tree by recursively considering all possible moves and outcomes to determine the best move for Player 1.
Alpha-Beta Pruning:

The program enhances the Minimax algorithm with alpha-beta pruning.
Alpha-beta pruning reduces the number of nodes visited by eliminating branches that are guaranteed to be worse than previously explored moves.
Adaptive Strategy:

The program supports playing against another program by making a single move.
The heuristics adaptively change the player's strategy to increase the chances of winning.
Usage
To use the program, provide the current game state as input on the standard input. The state should consist of eight lines, each containing eight space-separated numbers (1 for Player 1's disc, 2 for Player 2's disc, and 0 for an empty field). The program will return the updated game state on the standard output, where each line contains eight numbers.

Additionally, the program outputs the number of decision tree nodes visited and the running time of the algorithm on the standard error output.
