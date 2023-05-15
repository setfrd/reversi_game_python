import random
import sys
import time
def drawBoard(board):
    # This function prints out the board that it was passed. Returns None.
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)

    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')

        for x in range(8):
            print('| %s' % (board[x][y]), end=' ') #prints | + space + the value of board[x][y] + space

        print('|')
        print(VLINE)
        print(HLINE)

def resetBoard(board):
# Blanks out the board it is passed, except for the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '
# Starting pieces:
    board[3][3] = '1'
    board[3][4] = '2'
    board[4][3] = '2'
    board[4][4] = '1'

def getNewBoard():
# Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board

def isValidMove(board, tile, xstart, ystart):
# Returns False if the player's move on space xstart, ystart is invalid.
# If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == '1':
        otherTile = '2'
    else:
        otherTile = '1'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' ' # restore the empty space
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip

def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)
    
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard

def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys '1' and '2'.
    player_1_score = 0
    player_2_score = 0
    
    for x in range(8):
        for y in range(8):
            if board[x][y] == '1':
                player_1_score += 1
            if board[x][y] == '2':
                player_2_score += 1
    return {'1':player_1_score, '2':player_2_score}


def enterPlayerTile():
    # Lets the player type which tile they want to be.
    # Returns a list with the player's tile as the first item, and the computer's tile as the second.
    tile = ''
    
    while not (tile == '1' or tile == '2'):
        print('Do you want to be 1 or 2?')
        tile = input().upper()
    
    # the first element in the list is the player's tile, the second is the computer's tile.
    if tile == '1':
        return ['1', '2']
    else:
        return ['2', '1']


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'
def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard

def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')
    return [x, y]
def isGameOver(board , computerTile):
    playerTile = '1' if computerTile == '2' else '2'
    return not (getValidMoves(board, computerTile) or getValidMoves(board, playerTile))

def evaluateBoard(board, playerTile):
    opponentTile = '1' if playerTile == '2' else '2'
    
    # Strategy 1: Maximize number of tiles1
    
    playerScore, opponentScore = getScoreOfBoard(board)[playerTile], getScoreOfBoard(board)[opponentTile]
    tileScore = playerScore - opponentScore

    # Strategy 2: Favor corners and edges
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    cornerScore = sum([1 for corner in corners if board[corner[0]][corner[1]] == playerTile]) * 5
    edgeScore = 0
    for x in range(8):
        for y in range(8):
            if x in [0, 7] or y in [0, 7]:
                edgeScore += 1 if board[x][y] == playerTile else 0
    edgeScore *= 3

    # Strategy 3: Minimize opponent's mobility
    playerMoves = len(getValidMoves(board, playerTile))
    opponentMoves = len(getValidMoves(board, opponentTile))
    mobilityScore = playerMoves - opponentMoves

    # Weighted sum of all strategies
    totalScore = tileScore + cornerScore + edgeScore + mobilityScore

    return totalScore
def minimax(board, depth, maximizingPlayer, playerTile, opponentTile, alpha=float('-inf'), beta=float('inf')):
    computerTile = playerTile if maximizingPlayer else opponentTile
    if depth == 0 or isGameOver(board, computerTile):
        return None, evaluateBoard(board, playerTile)

    validMoves = getValidMoves(board, playerTile if maximizingPlayer else opponentTile)

    if not validMoves:
        return None, evaluateBoard(board, playerTile)

    best_move = None
    best_score = float('-inf') if maximizingPlayer else float('inf')

    for move in validMoves:
        new_board = getBoardCopy(board)
        makeMove(new_board, playerTile if maximizingPlayer else opponentTile, move[0], move[1])

        _, current_score = minimax(new_board, depth - 1, not maximizingPlayer, playerTile, opponentTile, alpha, beta)

        if maximizingPlayer:
            if current_score > best_score:
                best_score = current_score
                best_move = move

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        else:
            if current_score < best_score:
                best_score = current_score
                best_move = move

            beta = min(beta, best_score)
            if beta <= alpha:
                break

    return best_move, best_score


def getComputerMove(board, computerTile):
    playerTile = '1' if computerTile == '2' else '2'
    depth = 3  # Adjust the depth for stronger/weaker AI
    start_time = time.time()
    move, _ = minimax(board, depth, True, computerTile, playerTile)
    end_time = time.time()
    time_taken = end_time - start_time
    return move , time_taken


def showPoints(playerTile, computerTile):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))

print('Welcome to Reversi!')


while True:
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    total_minmax_time = 0 
    while True:
        if turn == 'player':
            # Player's turn.
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard(validMovesBoard)
            else:
                drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit() # terminate the program
            elif move == 'hints':
                showHints = not showHints
                continue
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])

            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'
        else:
            # Computer's turn.
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            move, minmax_time = getComputerMove(mainBoard, computerTile)
            total_minmax_time += minmax_time
            makeMove(mainBoard, computerTile,move[0] , move[1])

            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'

    # Display the final score.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('player_1 scored %s points. player_2 scored %s points.' % (scores['1'], scores['2']))
    print(f'computation time during this game was : {total_minmax_time}')
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')

    if not playAgain():
        break