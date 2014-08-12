"""
Clone of 2048 game.

Author: John Liu
Date: 2014-14-Jun
"""

import poc_2048_gui        
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
          
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = []
    for item in range(len(line)):
        if line[item]<>0:
            result.append(line[item])
            
    while(len(result)<len(line)):
        result.append(0)        

    if len(result) == 1:
        return result
    
    if result[0] == result[1]:
        result[0] += result[1]
        result.remove(result[1])
    
    item = 1
    while item < len(result)-1:
        if (result[item] == result[item+1]) and (result[item] > 0):
            result[item] += result[item+1]
            result.pop(item+1)
        item += 1
            
    while(len(result)<len(line)):
        result.append(0)            
        
    return result


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.reset()
        self.limit = {UP: grid_height,
                      DOWN: grid_height,
                      LEFT: grid_width,
                      RIGHT: grid_width}
        self.edges = {UP: [[0,i] for i in range(self.width)],
                      DOWN: [[self.height-1,i] for i in range(self.width)],
                      LEFT: [[i,0] for i in range(self.height)],
                      RIGHT: [[i,self.width-1] for i in range(self.height)]}
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = []
        while len(self.grid) < self.height * self.width:
            self.grid.append(0)
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        disp = ""
        for row in range(self.height):
            for col in range(self.width):
                disp += str(self.grid[row*self.width+col]) + " "
            disp += "\n"
        return disp
        
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        front = self.edges[direction]
        offset = OFFSETS[direction]
        moved_boolean = False
        
        for index in front:
            init_list = tmp_list = []
            for item in range(self.limit[direction]):
                init_list.append(self.get_tile(index[0]+item*offset[0],
                                              index[1]+item*offset[1]))
            tmp_list = merge(init_list)
            
            for item in range(self.limit[direction]):
                moved_boolean = moved_boolean or (tmp_list[item] != init_list[item])
                self.set_tile(index[0]+item*offset[0],
                              index[1]+item*offset[1],tmp_list[item])
        if moved_boolean:
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        index = random.randint(0,self.height*self.width-1)
        while self.grid[index] != 0:
            index = random.randint(0,self.height*self.width-1)
        
        self.grid[index] = random.choice([2,2,2,2,2,2,2,2,2,4])
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.grid[row*self.width + col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.grid[row*self.width + col]
    
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
