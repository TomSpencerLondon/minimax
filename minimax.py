# # minimax.py
#
# # Implements the minimax and alpha-beta algorithms.
#
# # Requires a class to be implemented based on the template below:
# class Game:
#     """Template Game class"""
#
#     def __init__(self, state=None):
#
#     def playerMove(self):
#         """Get a move from the player"""
#
#     def getPossibleMoves(self):
#         """Get a list of all possible moves from the current game state"""
#
#     def applyMove(self, move, computerTurn):
#         """Apply the given move"""
#
#     def getScore(self):
#         """
#         Get the score for the current game state.
#         The score is returned as a tuple (TSCOREVALUE, TGAMEOVER).
#         A TSCOREVALUE of 1 means computer wins.
#         A TSCOREVALUE of -1 means player wins.
#         A TSCOREVALUE of 0 means it is a draw.
#         TGAMEOVER is True if we have reached the end of the game, False otherwise
#         """
#
#     def show(self):
#         """Show the state on the screen"""
#
#     def copy(self):
#         """Return a copy of this game state"""

# The algorithm can be run like this:

# game = Game()
# play(game, ALG_MINIMAX)

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------

import random
import numpy as np

# -------------------------------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------------------------------

ALG_RANDOM  = 0      # use a random play algorithm
ALG_MINIMAX = 1      # use a minimax algorithm
ALG_ALPHABETA = 2    # use a minimax algorithm with alpha-beta pruning


def minimax(game, maxTurn, depth):
    """Apply the miminax algorithm recursively"""

    # Get the score for the current game
    score, gameOver = game.getScore()

    # If we have reached the end of the game or reached the max depth then return the score
    if gameOver or depth==game.maxDepth:                     
        return score

    # Search the tree, generating the values for all the moves
    bestScore = None
    for option in game.getPossibleMoves():
        # Try a move, all the way down the tree
        newGame = game.copy()
        newGame.applyMove(option, maxTurn)
        score = minimax(newGame, not maxTurn, depth+1)

        # Check if this move beats our best move
        if maxTurn:
            if bestScore is None or score > bestScore:                                              # trying to maximise the score
                bestScore = score
        else: # minTurn
            if bestScore is None or score < bestScore:                                              # trying to minimise the score
                bestScore = score

    return bestScore


def alphabeta(game, maxTurn, alpha, beta, depth):
    """Apply the miminax with alpha-beta pruning algorithm recursively"""

    # Get the score for the current game
    scope, gameOver = game.getScore()

    # If we have reached the end of the game or reached the max depth then return the score
    if gameOver or depth==game.maxDepth:                     
        return score

    # Search the tree, generating the values for all the moves
    for option in game.getPossibleMoves():
        # Try a move, all the way down the tree
        newGame = game.copy()
        newGame.applyMove(option, maxTurn)
        score = alphabeta(newGame, not maxTurn, alpha, beta, depth+1)

        # Check if this move beats our best move
        if maxTurn:
            if score > alpha:                                                                       # trying to maximise the score
                alpha = score                                                                       # alpha is the max score so far
            if alpha >= beta:
                break
        else: # minTurn
            if score < beta:                                                                        # trying to minimise the score
                beta = score
            if beta <= alpha:
                break

    if maxTurn:
        bestScore = alpha
    else:
        bestScore = beta

    return bestScore


def computerMoveRandom(game):
    """Generate a random move"""

    options = game.getPossibleMoves()

    move = random.randrange(len(options))

    return options[move]



def computerMoveMinimax(game, algorithm):
    """Generate a move based on the minimax algorithm"""

    # Search the tree, generating the values for all the moves
    bestScore = None
    bestOptions = []
    shortestPath = 99999
    for option in game.getPossibleMoves():
        # Try a move, all the way down the tree
        newGame = game.copy()
        newGame.applyMove(option, True)

        # Recurse down the tree
        if algorithm==ALG_MINIMAX:
            score = minimax(newGame, False, depth=0)
        else:
            score = alphabeta(newGame, False, -200, 200, depth=0)

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
    """Execute alternating player / computer moves"""

    while True:
        #Get player move and stop if the game is over
        game.playerMove()
        score, gameOver = game.getScore()
        if gameOver:
            break

        # Get computer move and stop if the game is over
        computerMove(game, ALG_MINIMAX)
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


