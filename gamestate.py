# -------------------------------------------------------------------------------------------------
# gamestate.py
# -------------------------------------------------------------------------------------------------

import numpy as np


class Board2D:
    """
    A class to represent a general 2D game board.
    E.g. this can be used for Noughts and Crosses.
    """

    def __init__(self, rows, cols, grid=None):
        """Set the board up"""

        self.rows = rows
        self.cols = cols
        if grid is None:
            self.grid = np.full((rows, cols), '_')
        else:
            self.grid = grid
        self.flipped = False

    def show(self):
        """Show the state on the screen"""

        if self.flipped:
            startRow = self.rows - 1
            endRow = -1
            increment = -1
        else:
            startRow = 0
            endRow = self.rows
            increment = 1

        for row in range(startRow, endRow, increment):
            for col in range(0, self.cols):
                print(self.grid[row, col], " ", end="")
            print("")
        print("")

    def setCell(self, row, col, value):
        """Set the value of the given cell"""

        self.grid[row, col] = value

    def getCell(self, row, col):
        """Get the value of the given cell"""

        return self.grid[row, col]

    def isHorizRun(self, row, col, runLength, value):
        """
        Do we have a horizontal run of the same value starting at row,col.
        runLength is the length of the sequence we are looking for.
        value is the value in the cell.
        """
        possibleRun = self.grid[row, col:col + runLength]  # slice board so that desired starting point is top left

        # Check if we have a run of the right length and right value
        return len(possibleRun) == runLength and np.all(possibleRun == value)

    def isVertRun(self, row, col, runLength, value):
        """
        Do we have a vertical run of the same value starting at row,col.
        runLength is the length of the sequence we are looking for.
        value is the value in the cell.
        """
        possibleRun = self.grid[row:row + runLength, col]  # slice board so that desired starting point is top left

        # Check if we have a run of the right length and right value
        return len(possibleRun) == runLength and np.all(possibleRun == value)

    def isDiagRun(self, row, col, runLength, value):
        """
        Do we have a diagonal run of the same value starting at row,col.
        runLength is the length of the sequence we are looking for.
        value is the value in the cell.
        """

        boardSlice = self.grid[row:]  # slice board so that desired row is at the top
        diagonal = boardSlice.diagonal(offset=col)  # diagonal from that slice
        possibleRun = diagonal[0:runLength]  # slice diagnonal down to desired run length

        # Check if we have a run of the right length and right value
        return len(possibleRun) == runLength and np.all(possibleRun == value)

    def isReverseDiagRun(self, row, col, runLength, value):
        """
        Do we have a reverse diagonal run of the same value starting at row,col.
        runLength is the length of the sequence we are looking for.
        value is the value in the cell.
        The row number provided should be the lowest in the possible run
        """

        boardSlice = np.fliplr(self.grid[row:])  # slice board so that desired row is at the top
        flippedCol = self.cols - 1 - col
        diagonal = boardSlice.diagonal(offset=flippedCol)  # diagonal from that slice
        possibleRun = diagonal[0:runLength]  # slice diagnonal down to desired run length

        # Check if we have a run of the right length and right value
        return len(possibleRun) == runLength and np.all(possibleRun == value)

    def isHorizStreak(self, row, col, runLength, value, streakLength):
        """
        Do we have a horizontal streak, i.e. n out of m of the same value starting at row,col.
        runLength is the length of the sequence we are looking for.
        value is the value in the cell.
        """
        possibleRun = self.grid[row, col:col + runLength]  # slice board so that desired starting point is top left

        # Check if we have a run of the right length and right value
        return len(possibleRun) == runLength and (possibleRun == value).sum() == streakLength and (
                    possibleRun == '_').sum() == runLength - streakLength

    def isVertStreak(self, row, col, runLength, value, streakLength):
        """
        Do we have a vertical streak, i.e. n out of m of the same value starting at row,col.
        runLength is the length of the sequence we are looking for.
        value is the value in the cell.
        """
        possibleRun = self.grid[row:row + runLength, col]  # slice board so that desired starting point is top left

        # Check if we have a run of the right length and right value
        return len(possibleRun) == runLength and (possibleRun == value).sum() == streakLength and (
                    possibleRun == '_').sum() == runLength - streakLength

    def isDiagStreak(self, row, col, runLength, value, streakLength):
        """
        Do we have a diagonal streak, i.e. n out of m of the same value starting at row,col.
        runLength is the length of the sequence we are looking for.
        value is the value in the cell.
        """

        boardSlice = self.grid[row:]  # slice board so that desired row is at the top
        diagonal = boardSlice.diagonal(offset=col)  # diagonal from that slice
        possibleRun = diagonal[0:runLength]  # slice diagnonal down to desired run length

        # Check if we have a run of the right length and right value
        return len(possibleRun) == runLength and (possibleRun == value).sum() == streakLength and (
                    possibleRun == '_').sum() == runLength - streakLength

    def isReverseDiagStreak(self, row, col, runLength, value, streakLength):
        """
        Do we have a reverse diagonal streak, i.e. n out of m of the same value starting at row,col.
        runLength is the length of the sequence we are looking for.
        value is the value in the cell.
        The row number provided should be the lowest in the possible run
        """

        boardSlice = np.fliplr(self.grid[row:])  # slice board so that desired row is at the top
        flippedCol = self.cols - 1 - col
        diagonal = boardSlice.diagonal(offset=flippedCol)  # diagonal from that slice
        possibleRun = diagonal[0:runLength]  # slice diagnonal down to desired run length

        # Check if we have a run of the right length and right value
        return len(possibleRun) == runLength and (possibleRun == value).sum() == streakLength and (
                    possibleRun == '_').sum() == runLength - streakLength

    def boardIsFull(self):
        """Check if the board is full"""

        return len(self.grid[self.grid == '_']) == 0

    def getAvailableCells(self):
        """Cells numbered in sequence starting with 0 in top left"""

        allMoves = np.arange(0, 9).reshape(3, 3)  # generate a 3x3 array with position numbers 0 to 8
        options = np.where(self.grid == '_', allMoves,
                           self.grid)  # find all empty squares and replace with position number 0 to 8
        options = options[options != 'O']  # remove all O moves
        options = options[options != 'X']  # remove all X moves
        options = options.astype(np.int)  # convert from string to int
        return options

    def copy(self):
        return Board2D(self.rows, self.cols, self.grid.copy())


class Stack2D(Board2D):
    """
    A class to represent a 2D game board where columns are stacks, i.e. pieces dropped in a column stack on top of each other.
    E.g. this can be used for Connect 4.
    """

    def __init__(self, rows, cols, grid=None, stackHeight=None):
        """Set the board up"""

        super().__init__(rows, cols, grid)
        if stackHeight is None:
            self.stackHeight = [0] * self.cols
        else:
            self.stackHeight = stackHeight

    def stackIsFull(self, stack):
        """Check if the given stack is full"""

        return self.stackHeight[stack] == self.rows

    def getFullStacks(self):
        """Get a list of all stacks that are full"""

        stacks = []
        for stack in range(self.cols):
            if self.stackHeight[stack] == self.rows:
                stacks.append(stack)

        return stacks

    def getNonFullStacks(self):
        """Get a list of all stacks that are not full"""

        stacks = []
        for stack in range(self.cols):
            if self.stackHeight[stack] < self.rows:
                stacks.append(stack)

        return stacks

    def getEmptyStacks(self):
        """Get a list of all stacks that are empty"""

        stacks = []
        for stack in range(self.cols):
            if self.stackHeight[stack] == 0:
                stacks.append(stack)

        return stacks

    def addToStack(self, stack, value):
        """Add the piece 'value' to the given stack"""

        row = self.stackHeight[stack]  # make sure counter is dropped at top of column
        super().setCell(row, stack, value)
        self.stackHeight[stack] += 1

    def copy(self):
        return Stack2D(self.rows, self.cols, self.grid.copy(), self.stackHeight.copy())


# -------------------------------------------------------------------------------------------------
# Code to test the Board2D and Stack2D classes
# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # Check for horizontal win state
    board = Board2D(3, 3, np.array([['X', 'X', 'X'], ['O', 'O', '_'], ['O', '_', '_']]))
    assert (board.isHorizRun(0, 0, 3, 'X'))
    assert (not board.isHorizRun(1, 0, 3, 'X'))
    assert (not board.isHorizRun(2, 0, 3, 'X'))

    # Check for vertical win state
    board = Board2D(3, 3, np.array([['X', 'O', 'O'], ['X', 'O', '_'], ['X', '_', '_']]))
    assert (board.isVertRun(0, 0, 3, 'X'))
    assert (not board.isVertRun(0, 1, 3, 'X'))
    assert (not board.isVertRun(0, 2, 3, 'X'))

    # Check for diagonal win state
    board = Board2D(3, 3, np.array([['X', 'O', 'O'], ['O', 'X', '_'], ['_', '_', 'X']]))
    assert (board.isDiagRun(0, 0, 3, 'X'))
    assert (not board.isReverseDiagRun(0, 2, 3, 'X'))

    # Check for reverse diagonal win state
    board = Board2D(3, 3, np.array([['O', 'O', 'X'], ['O', 'X', '_'], ['X', '_', '_']]))
    assert (not board.isDiagRun(0, 0, 3, 'X'))
    assert (board.isReverseDiagRun(0, 2, 3, 'X'))

    # Check for horizontal streak
    board = Board2D(3, 3, np.array([['X', 'X', '_'], ['X', 'X', 'O'], ['X', '_', '_']]))
    assert (board.isHorizStreak(0, 0, 3, 'X', 2))
    assert (not board.isHorizStreak(0, 0, 3, 'O', 2))
    assert (not board.isHorizStreak(1, 0, 3, 'X', 2))
    assert (not board.isHorizStreak(1, 0, 3, 'O', 1))
    assert (board.isHorizStreak(2, 0, 3, 'X', 1))

    # Check for vertical streak
    board = Board2D(3, 3, np.array([['X', 'X', 'X'], ['X', 'X', '_'], ['_', 'O', '_']]))
    assert (board.isVertStreak(0, 0, 3, 'X', 2))
    assert (not board.isVertStreak(0, 0, 3, 'O', 2))
    assert (not board.isVertStreak(0, 1, 3, 'X', 2))
    assert (not board.isVertStreak(0, 1, 3, 'O', 1))
    assert (board.isVertStreak(0, 2, 3, 'X', 1))

    # Check for diagonal streak
    board = Board2D(3, 3, np.array([['X', '_', '_'], ['_', '_', '_'], ['_', '_', 'X']]))
    assert (board.isDiagStreak(0, 0, 3, 'X', 2))
    assert (not board.isReverseDiagStreak(0, 0, 3, 'X', 2))

    # Check for diagonal streak
    board = Board2D(3, 3, np.array([['_', '_', 'X'], ['_', 'X', '_'], ['_', '_', '_']]))
    assert (not board.isReverseDiagStreak(0, 0, 3, 'X', 2))
    assert (board.isReverseDiagStreak(0, 2, 3, 'X', 2))

    # Test out some Connect4 scenarios
    _ROWS = 6
    _COLS = 7
    _RUNLENGTH = 4
    board = Stack2D(6, 7, np.array([['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                                    ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                                    ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                                    ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                                    ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
                                    ['X', 'X', 'X', 'X', 'X', 'X', 'X']]))
    board.flipped

    # Check for win on horizontal
    for row in range(0, _ROWS):
        for col in range(0, _COLS - (_RUNLENGTH - 1)):
            if board.isHorizRun(row, col, _RUNLENGTH, 'X'):
                print("Horz run", row, col)

    # Check for win on vertical
    for row in range(0, _ROWS - (_RUNLENGTH - 1)):
        for col in range(0, _COLS):

            if board.isVertRun(row, col, _RUNLENGTH, 'X'):
                print("Vert run", row, col)

    # Check normal diagonals
    for row in range(0, _ROWS - (_RUNLENGTH - 1)):
        for col in range(0, _COLS - (_RUNLENGTH - 1)):
            if board.isDiagRun(row, col, _RUNLENGTH, 'X'):
                print("Diag run", row, col)

    # Check flipped diagonals
    for row in range(0, _ROWS - (_RUNLENGTH - 1)):
        for col in range(_COLS - _RUNLENGTH, _COLS):
            if board.isReverseDiagRun(row, col, _RUNLENGTH, 'X'):
                print("Reverse diag", row, col)


