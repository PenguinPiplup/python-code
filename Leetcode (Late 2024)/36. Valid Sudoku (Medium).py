"""
Problem Link: https://leetcode.com/problems/valid-sudoku/description/
(Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated.)
"""

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        return self.validaterows(board) and self.validatecolumns(board) and self.validate3x3(board)

    # Check if each row does not contain duplicate numbers
    def validaterows(self, board):
        for row in board:
            mem = []
            for num in row:
                if num == ".":
                    pass
                elif num in mem:
                    return False
                else:
                    mem += [num]
        return True

    # Check if each column does not contain duplicate numbers
    def validatecolumns(self, board):
        for column in range(9):
            mem = []
            for row in board:
                if row[column] == ".":
                    pass
                elif row[column] in mem:
                    return False
                else:
                    mem += row[column]
        return True

    # Check if each 3x3 box does not contain duplicate numbers
    def validate3x3(self, board):
        for nines in range(9):
            init_row = (nines // 3) * 3
            init_column = (nines % 3) * 3
            mem = []
            for i in range(3):
                for j in range(3):
                    item = board[init_row + i][init_column + j]
                    if item == ".":
                        pass
                    elif item in mem:
                        return False
                    else:
                        mem += item
        return True