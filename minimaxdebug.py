'''
minimaxdebug.py

Implements a debugging version of the minimax and alpha-beta algorithms found in minimax.py.

Requires the implementation of an additional method in the Game class:

    def prettyPath(self, path):
        """
        Show the evaluation path neatly formatted.
        path is a list of (bestScore, state, level) tuples
        """
'''

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------

import random
import numpy as np

# -------------------------------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------------------------------
visitedNodes = 0                                                                                    # debug

ALG_RANDOM  = 0      # use a random play algorithm
ALG_MINIMAX = 1      # use a minimax algorithm
ALG_ALPHABETA = 2    # use a minimax algorithm with alpha-beta pruning


def minimax(game, maxTurn, depth, path):
    """Apply the minimax algorithm recursively"""

    global visitedNodes                                                                             # debug
    visitedNodes += 1                                                                               # debug

    # Get the score for the current game
    score, gameOver = game.getScore()

    # If we have reached the end of the game or reached the max depth then return the score
    if gameOver or depth==game.maxDepth:                     
        path.append((score, game, depth))                                                          # debug
        return score

    # Search the tree, generating the values for all the moves
    bestScore = None
    bestPath = None                                                                                 # debug
    for option in game.getPossibleMoves():
        # Try a move, all the way down the tree
        newGame = game.copy()
        newGame.applyMove(option, maxTurn)
        newPath = []                                                                                # debug
        score = minimax(newGame, not maxTurn, depth+1, newPath)

        # Check if this move beats our best move
        if maxTurn:
            if bestScore is None or score > bestScore:                                              # trying to maximise the score
                bestScore = score
                bestPath = newPath.copy()                                                           # debug
        else: # minTurn
            if bestScore is None or score < bestScore:                                              # trying to minimise the score
                bestScore = score
                bestPath = newPath.copy()                                                           # debug

    #if bestScore is None:
    #    raise Exception("No possible moves found - have you missed a game end scenario?")

    # For debug purposes gather the path to the best option decision
    path.extend(bestPath)                                                                           # debug
    path.append((bestScore, game, depth))                                                           # debug

    return bestScore


def alphabeta(game, maxTurn, alpha, beta, depth, path):
    """Apply the miminax with alpha-beta pruning algorithm recursively"""

    global visitedNodes                                                                             # debug
    visitedNodes += 1                                                                               # debug

    # Get the score for the current game
    score, gameOver = game.getScore()

    # If we have reached the end of the game or reached the max depth then return the score
    if gameOver or depth==game.maxDepth:                     
        path.append((score, game, depth))                                                          # debug
        return score

    # Search the tree, generating the values for all the moves
    bestPath = None                                                                                 # debug
    for option in game.getPossibleMoves():
        # Try a move, all the way down the tree
        newGame = game.copy()
        newGame.applyMove(option, maxTurn)
        newPath = []                                                                                # debug
        score = alphabeta(newGame, not maxTurn, alpha, beta, depth+1, newPath)

        # Check if this move beats our best move
        if maxTurn:
            if score > alpha:                                                                       # trying to maximise the score
                alpha = score                                                                       # alpha is the max score so far
                bestPath = newPath.copy()                                                           # debug
            if alpha >= beta:
                break
        else: # minTurn
            if score < beta:                                                                        # trying to minimise the score
                beta = score
                bestPath = newPath.copy()                                                           # debug
            if beta <= alpha:
                break

    #if bestPath is None:
    #    raise Exception("No possible moves found - have you missed a game end scenario?")

    if maxTurn:
        bestScore = alpha
    else:
        bestScore = beta

    # For debug purposes gather the path to the best option decision
    if bestPath is not None:
        path.extend(bestPath)                                                                       # debug
    path.append((bestScore, game, depth))                                                          # debug

    return bestScore


def computerMoveRandom(game):
    """Generate a random move"""

    options = game.getPossibleMoves()

    move = random.randrange(len(options))

    return options[move]


def computerMoveMinimax(game, algorithm):
    """Generate a move based on the minimax algorithm"""

    global visitedNodes                                                                             # debug
    visitedNodes = 0                                                                                # debug

    # Search the tree, generating the values for all the moves
    bestScore = None
    bestOptions = []
    shortestPath = 99999
    for option in game.getPossibleMoves():
        # Try a move, all the way down the tree
        newGame = game.copy()
        newGame.applyMove(option, True)
        path = []                                                                                   # debug

        # Recurse down the tree
        if algorithm==ALG_MINIMAX:
            score = minimax(newGame, False, 0, path)
        else:
            score = alphabeta(newGame, False, -200, 200, 0, path)

        # Check if this move beats our best move
        if bestScore is None or score > bestScore:
            # First option or best score
            bestScore = score
            bestOptions = [option]
            shortestPath = len(path)
        elif score == bestScore and len(path) < shortestPath:
            # Same score but shorter path to it
            bestScore = score
            bestOptions = [option]
            shortestPath = len(path)
        elif score == bestScore and len(path) == shortestPath:
            # Same score and same path length
            bestOptions.append(option)


        path.reverse()                                                                              # debug
        print("      Option ", option, " score ", score)                                            # debug
        game.prettyPath(path)                                                                       # debug

    print("      Evaluated {} nodes".format(visitedNodes))                                          # debug

    # Apply the winning move (randomly choose from moves with equal best score)
    move = random.choice(bestOptions)

    return move

def computerMove(game, algorithm=ALG_RANDOM):
    # Get computer move and stop if the game is over
    print("\nComputer move:")
    if algorithm==ALG_MINIMAX:
        move = computerMoveMinimax(game, ALG_MINIMAX)
    elif algorithm==ALG_ALPHABETA:
        move = computerMoveMinimax(game, ALG_ALPHABETA)
    else:
        move = computerMoveRandom(game)

    game.applyMove(move, True)

    return move


def play(game, algorithm=ALG_RANDOM):
    # Execute alternating player / computer moves
    while True:
        # Get player move and stop if the game is over
        game.playerMove()
        score, gameOver = game.getScore()
        if gameOver:
            break

        # Get computer move and stop if the game is over
        computerMove(game, algorithm)
        score, gameOver = game.getScore()
        if gameOver:
            break

    # Show the result
    print("\n\nGame Over")
    if score==-100:
        print("Player wins")
    elif score==100:
        print("Computer wins")
    else:
        print("It's a draw")
    game.show()


