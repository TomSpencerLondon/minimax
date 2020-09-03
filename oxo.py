"""
Oxo Template

A noughts and crosses game
"""

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------

from minimaxdebug import play
from minimaxdebug import ALG_MINIMAX, ALG_RANDOM
from gamestate import *

# -------------------------------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------------------------------

ROWS = 3  # number of rows in the grid
COLS = 3  # number of cols in the grid
RUNLENGTH = 3  # length of a run that the winner needs to make
MAXDEPTH = 999  # maximum depth we want the minimax algorithm to search


# -------------------------------------------------------------------------------------------------
# Classes
# -------------------------------------------------------------------------------------------------

class Oxo:
    """The Oxo class implements the functionality required by the minimax algorithm"""

    def __init__(self, state=None):
        """Set up the initial state of the game board"""

        if state is None:
            self.state = Board2D(ROWS, COLS)  # if no state was provided set it up with an empty state
        else:
            self.state = state  # if a state was provided, set it up with that state
        self.maxDepth = MAXDEPTH

    def playerMove(self):
        """Get a move from the player"""

        self.show()

        # Allow the player to select a move
        while True:
            try:
                move = int(input("Your move (0-8):"))
                if self.isValidMove(move):
                    self.applyMove(move, False)
                    break
                else:
                    print("Invalid move")
            except ValueError:
                print("Please enter a number between 0 and 8")

        self.show()

    def isValidMove(self, move):
        """Is the given move valid?  Checks that the cell is empty"""

        # Is the move number valid?
        if move not in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            return False

        # Is the move in an empty cell?
        row = int(move / 3)
        col = move % 3
        if self.state.getCell(row, col) != '_':
            return False

        return True

    def getPossibleMoves(self):
        """Get a list of all possible moves from the current game state"""

        return self.state.getAvailableCells()

    def applyMove(self, move, computerTurn):
        """Apply the given move"""

        row = int(move / 3)
        col = move % 3
        self.state.setCell(row, col, 'X' if computerTurn else 'O')

    def getScore(self):
        """
        Get the score for the current game state.
        The score is returned as a tuple (TSCOREVALUE, TGAMEOVER).
        A TSCOREVALUE of 100 means computer wins.
        A TSCOREVALUE of -100 means player wins.
        A TSCOREVALUE of 0 means it is a draw.
        TGAMEOVER is True if we have reached the end of the game, False otherwise
        """

        board = self.state

        def findWin(value):

            # Check for win on horizontal
            if (board.isHorizRun(1, 0, 3, value)):
                return True

            # Check for win on vertical
            # ***TODO***: Enter your code here

            # Check for win on diagonal
            # ***TODO***: Enter your code here

            # No winning line found
            # ***TODO***: Enter your code here

            return False

        # Check for computer win
        if findWin('X'):
            return (100, True)

        # Check for player win
        if findWin('O'):
            return (-100, True)

        # Check if grid full, i.e. it's a draw
        if board.boardIsFull():
            return (0, True)

        # Game still not over
        return (0, False)

    def show(self):
        """Show the state of the board on the screen"""

        self.state.show()

    def copy(self):
        """Return a copy of this game state"""

        return Oxo(self.state.copy())

    def prettyPath(self, path):
        """
        Show the evaluation path neatly formatted.
        path is a list of (bestScore, game, level) tuples
        """

        # Print the score for each state in the path
        print("      ", end="")
        for scoreState in path:
            bestScore = scoreState[0]
            print("{:3}".format(bestScore), " ", end="")
        print("")

        # Print the board for each state in the path.  We need to print all states one row at a time
        for row in range(0, 3):
            print("      ", end="")
            for scoreState in path:
                for col in range(0, 3):
                    game = scoreState[1]
                    print(game.state.getCell(row, col), end="")
                print("  ", end="")
            print("")
        print("")


# -------------------------------------------------------------------------------------------------
# Main program
# -------------------------------------------------------------------------------------------------

game = Oxo()
play(game, ALG_MINIMAX)

