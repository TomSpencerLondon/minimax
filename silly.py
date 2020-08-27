"""
Silly

A silly game where the first to go in the middle wins
"""

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------

from minimaxdebug import play
from minimaxdebug import ALG_MINIMAX, ALG_RANDOM


# -------------------------------------------------------------------------------------------------
# Classes
# -------------------------------------------------------------------------------------------------

class Silly:
    """The Silly class implements the functionality required by the minimax algorithm"""

    def __init__(self, state=None):
        """Set up the state"""

        if state is None:
            self.state = ['_', '_', '_', '_', '_']      # if no state was provided set it up with an empty state
        else:
            self.state = state                          # if a state was provided, set it up with that state
        self.maxDepth = 100


    def playerMove(self):
        """Get a move from the player"""

        self.show()

        # Allow the player to select a move
        while True:
            try:
                move = int(input("\nYour move (0-4):"))
                if self.isValidMove(move):
                    self.applyMove(move, computerTurn=False)
                    break
                else:
                    print("Invalid move")
            except ValueError:
                print("Please enter a number between 0 and 4")
        self.show()


    def isValidMove(self, move):
        """Is the given move valid?  Checks that the cell is empty"""

        # Is the move number valid?
        if move not in [0,1,2,3,4]:
            return False

        # Is the move in an empty cell?
        if self.state[move] != '_':
            return False

        return True


    def getPossibleMoves(self):
        """Get a list of all possible moves from the current game state"""

        moves = []
        for position in range(5):
            if self.state[position] == '_':
                moves.append(position)
        return moves


    def applyMove(self, move, computerTurn):
        """Apply the given move"""

        board = self.state

        board[move] = 'X' if computerTurn else 'O'


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

        if (board[2]=='X'):
            return (100, True)            # computer wins if we have an X in position 2
        elif (board[2]=='O'):
            return (-100, True)           # player wins if we have a O in position 2
        else:
            return (0, False)             # game not over


    def show(self):
        """Show the state on the screen"""

        print(self.state, "\n")


    def copy(self):
        """Return a copy of this game state"""

        return Silly(self.state.copy())

       
    def prettyPath(self, path):
        """
        Show the evaluation path neatly formatted.
        path is a list of (bestScore, state, level) tuples
        """

        # Print the score for each state in the path
        print("      ", end="")
        for scoreState in path:
            bestScore = scoreState[0]
            print("{:<6}".format(bestScore), " ", end="")
        print("")

        # Print the board for each state in the path.  
        print("      ", end="")
        for scoreState in path:
            board = scoreState[1].state
            for col in range(5):
                print(board[col], end="")
            print("   ", end="")
        print("\n")


# -------------------------------------------------------------------------------------------------
# Main program
# -------------------------------------------------------------------------------------------------

game = Silly()
play(game, ALG_MINIMAX)
