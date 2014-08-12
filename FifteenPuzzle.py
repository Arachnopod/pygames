"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

Author: John Liu
Date:   August 7, 2014
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0:
            return False
        for rowiter in range(target_row+1,self.get_height()):
            for coliter in range(self.get_width()):
                if self.get_number(rowiter,coliter) != rowiter * self.get_width() + coliter:
                    return False
        for coliter in range(target_col+1,self.get_width()):
            if self.get_number(target_row,coliter) != target_row * self.get_width() + coliter:
                return False        
        return True

    def find_and_move_tile(self, tile_row, tile_col, target_row, target_col):
        """
        Place correct tile at target position
        """
        move_string = 'u' * (target_row - tile_row)
        if (target_row - tile_row) > 1 and (tile_col > target_col):
            move_string += 'r' * (tile_col - target_col)
            move_string += "dllur" * (tile_col - target_col - 1)              
            move_string += "dlu"         
            move_string += "lddru" * (target_row - tile_row - 1)               
            move_string += "ld"
            
        elif (target_row - tile_row) > 1 and (tile_col < target_col):
            move_string += 'l' * (target_col - tile_col)      
            move_string += "drrul" * (target_col - tile_col - 1)                
            move_string += "dru"
            move_string += "lddru" * (target_row - tile_row - 1)                
            move_string += "ld"
            
        elif (target_row - tile_row) > 1 and (tile_col == target_col):
            move_string += 'lddru' * (target_row - tile_row - 1)
            move_string += "ld"
            
        elif (target_row - tile_row) == 1 and tile_row == 0 and (tile_col > target_col):  
            move_string += 'r' * (tile_col - target_col)
            move_string += "dllur" * (tile_col - target_col - 1)                
            move_string += "dlu"
            move_string += "ld"
            
        elif (target_row - tile_row) == 1 and tile_row == 0 and (tile_col < target_col):
            move_string += 'l' * (target_col - tile_col)      
            move_string += "drrul" * (target_col - tile_col - 1)                
            move_string += "dru"
            move_string += "ld"
        
        elif (target_row - tile_row) == 1 and (tile_col > target_col):
            move_string += 'r' * (tile_col - target_col)
            move_string += "ulldr" * (tile_col - target_col - 1)                
            move_string += "ul"
            move_string += "lddru"
            move_string += "ld"
            
        elif (target_row - tile_row) == 1 and (tile_col < target_col):
            move_string += 'l' * (target_col - tile_col)      
            move_string += "urrdl" * (target_col - tile_col - 1)                
            move_string += "ur"
            move_string += "lddru"
            move_string += "ld"
            
        elif (target_row - tile_row) == 1 and tile_col == target_col:
            move_string += 'ld'
            
        elif (target_row == tile_row):
            move_string += "l" * (target_col - tile_col)
            move_string += "urrdl" * ( target_col - tile_col - 1)
            
        return move_string
    
    
    
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.lower_row_invariant(target_row, target_col), "lower row invariance failed"
        tile = self.current_position(target_row, target_col)        
        move_string = self.find_and_move_tile(tile[0],tile[1],target_row,target_col)                        
        self.update_puzzle(move_string)        
        assert self.lower_row_invariant(target_row,target_col-1), "invalid row="+str(target_row)+" col-1="+str(target_col-1)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.lower_row_invariant(target_row,0), "target_row,0"
        tile = self.current_position(target_row,0)
        
        if tile == (target_row-1,0):
            move_string = 'u'
            move_string += 'r' * (self.get_width()-1)
            self.update_puzzle(move_string)
            return move_string
        
        if tile == (target_row-1,1):
            move_string = 'u'
            
        elif tile[0] == target_row-1:
            move_string = 'u'
            move_string += 'r' * tile[1]
            move_string += 'ulldr' * ( tile[1] - 1 )
            move_string += 'l'
            
        else:
            move_string = 'ur'
            move_string += self.find_and_move_tile(tile[0],tile[1],target_row-1,1)
            
        move_string += 'ruldrdlurdluurddlu'
        move_string += 'r' * (self.get_width()-1)
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row-1,self.get_width()-1),"target_row-1,_width-1"
        return move_string

    #############################################################
    # Phase two methods

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(1, target_col) != 0:
            return False
        for rowiter in range(2,self.get_height()):
            for coliter in range(self.get_width()):
                if self.get_number(rowiter,coliter) != rowiter * self.get_width() + coliter:
                    return False
        for coliter in range(target_col+1,self.get_width()):
            if self.get_number(1,coliter) != self.get_width() + coliter:
                return False        
        return True
        
        
    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(0, target_col) != 0:
            return False
        for rowiter in range(2,self.get_height()):
            for coliter in range(self.get_width()):
                if self.get_number(rowiter,coliter) != rowiter * self.get_width() + coliter:
                    return False
        for coliter in range(target_col+1,self.get_width()):
            if self.get_number(0,coliter) != coliter:
                return False        
            if self.get_number(1,coliter) != self.get_width() + coliter:
                return False
            if self.get_number(1,target_col) != self.get_width() + target_col:
                return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row0_invariant(target_col), "row0 invariant"
        tile = self.current_position(0,target_col)
        
        if tile[0] == 0 and tile[1]==target_col-1:
            move_string = "ld"
            
        elif tile[0] == 1 and tile[1] == target_col-1:
            move_string = "lld"
            move_string += 'urdlurrdluldrruld'
            
        else:
            move_string = 'ld'
            move_string += self.find_and_move_tile(tile[0],tile[1],1,target_col-1)
            move_string += 'urdlurrdluldrruld'
            
        self.update_puzzle(move_string)
        assert self.row1_invariant(target_col-1), "row 1 invariant error"+str(target_col-1)    
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(target_col), "row 1 invariant error"       
        tile = self.current_position(1,target_col)
        
        if tile[0] == 1 and tile[1] < target_col:
            move_string = "l" * (target_col - tile[1])
            move_string += "urrdl" * (target_col - tile[1] - 1)
            move_string += "ur"
            
        elif tile[0] == 0 and tile[1] < target_col:
            move_string = "u"
            move_string += 'l' * (target_col - tile[1])
            move_string += 'drrul' * (target_col - tile[1] - 1)
            move_string += "dru"
            
        elif tile[0] == 0 and tile[1] == target_col:
            move_string = "u"
        
        self.update_puzzle(move_string)
        assert self.row0_invariant(target_col),"row0 invariant"
        return move_string

    ###########################################################
    # Phase 3 methods

    def check_2x2(self):
        """
        Helper function to check if 2x2 is solved
        """
        if self.current_position(0,0) != (0,0):
            return False
        if self.current_position(1,0) != (1,0):
            return False
        if self.current_position(0,1) != (0,1):
            return False
        if self.current_position(1,1) != (1,1):
            return False
        return True
    
    
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(1), "row1 invariant in solve2x2"
        move_string = "lu"
        self.update_puzzle('lu')
        while not self.check_2x2():
            move_string += 'rdlu'
            self.update_puzzle('rdlu')

        return move_string
                

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        zero_pos = self.current_position(0,0)
        move_string = 'd' * (self.get_height() - zero_pos[0] - 1)
        move_string += 'r' * (self.get_width() - zero_pos[1] - 1)
        self.update_puzzle(move_string)
    
        for rowiter in range(self.get_height()-1, 1, -1):
            for coliter in range(self.get_width()-1, 0, -1):
                move_string += self.solve_interior_tile(rowiter,coliter)
            move_string += self.solve_col0_tile(rowiter)

        for coliter in range(self.get_width()-1, 1, -1):
            move_string += self.solve_row1_tile(coliter)
            move_string += self.solve_row0_tile(coliter)
        
        move_string += self.solve_2x2()

        return move_string

# Start interactive simulation

#PUZ = Puzzle(4,4)
#PUZ.solve_puzzle() 
#poc_fifteen_gui.FifteenGUI(PUZ)
#PUZ = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#PUZ.solve_puzzle() 
#PUZ = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#PUZ.solve_puzzle()
#poc_fifteen_gui.FifteenGUI(PUZ)