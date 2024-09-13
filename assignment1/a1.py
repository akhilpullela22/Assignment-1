# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys
import random

class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "game" : self.game,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner
        }
        self.grid = None
        self.current_player = None
        self.width = 0
        self.height = 0

    # Convert a raw string to a command and a list of arguments
    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Uknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

    def game(self, args):
        """This command creates a new game on an empty rectangular grid of width n and height m 
        (both in the range from 1 and 20). It only requires the command status as output."""
        try:
            # Initialize the grid size
            self.width = int(args[0])
            self.height = int(args[1])
            
            # Ensure that the width and height are within valid range
            if not (1 <= self.width <= 20 and 1 <= self.height <= 20):
                raise ValueError("Invalid grid dimensions.")
            
            # Create an empty grid and initialize game state
            self.grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
            self.current_player = 1  # Player 1 starts
        except:
            print("= -1")
            return False
        return True

    
    def show(self, args):
        """This command shows the current state of the grid, one line per row, followed by the command status."""
        if self.grid is None:  # Ensure that the grid exists before printing.
            print("? No game in progress. Start a new game first.", file=sys.stderr)
            print("= -1")
            return False
        
        # Print the grid row by row
        for row in self.grid:
            print(''.join(row))
        
        return True
    
    def play(self, args):
        if len(args) != 3:
            print(f"= illegal move: {' '.join(args)} wrong number of arguments")
            return -1
        
        try:
            x = int(args[0])
            y = int(args[1])
            digit = int(args[2])
        except ValueError:
            print(f"= illegal move: {' '.join(args)} wrong coordinate or number")
            return -1
        
        if (x > self.n or y > self.m or x < 0 or y < 0):
            print(f"= illegal move: {' '.join(args)} wrong coordinate")
            return -1
        
        if digit != 1 or digit != 0:
            print(f"= illegal move: {' '.join(args)} wrong number")
            return -1
        
        if self.grid[y][x] != '.':
            print(f"= illegal move: {' '.join(args)} occupied")
            return -1
        
        # triples constraint
        if self.check_triple(x, y, digit, args) == -1:
            print(f"= illegal move: {' '.join(args)} three in a row")
            return -1
        
        # balance constraint
        if self.check_balance(x, y, digit, args) == -1:
            print(f"= illegal move: {' '.join(args)} too many {digit}")
            return -1
        # make the move
        self.grid[y][x] = str(digit)
        self.row_count[y][digit] += 1
        self.col_count[x][digit] += 1
        print("= 1")
        return 1
    

    def legal(self, args):

        if len(args) != 3:
            print("no")
            return -1
        
        try:
            x = int(args[0])
            y = int(args[1])
            digit = int(args[2])
        except ValueError:
            print("no")
            return -1
        
        if (x > self.n or y > self.m or x < 0 or y < 0):
            print("no")
            return -1
        
        if digit != 1 or digit != 0:
            print("no")
            return -1
        
        if self.grid[y][x] != '.':
            print("no")
            return -1
        
        # triples constraint
        if self.check_triple(x, y, digit, args) == -1:
            print("no")
            return -1
        
        # balance constraint
        if self.check_balance(x, y, digit, args) == -1:
            print("no")
            return -1
        
        print("yes")
        return 1
    
    def check_triple(self, x, y, digit, args):
        row = self.grid[y][:]
        row[x] = str(digit)
        if '000' in ''.join(row) or '111' in ''.join(row):
            return -1
        col = [self.grid[i][x] for i in range(self.m)]
        col[y] = str(digit)
        if '000' in ''.join(col) or '111' in ''.join(col):
            return -1
    def check_balance(self, x, y, digit, args):
        row_count = sum(1 for cell in self.grid[y] if cell == str(digit))
        if row_count + 1 > (self.n + 1) // 2:
            return -1
        
        col_count = sum(1 for i in range(self.m) if self.grid[i][x] == str(digit))
        if col_count + 1 > (self.m + 1) // 2:
            return -1
    
    def genmove(self, args):
        #This command generates and plays a random move and gives the move as its response. 
        # The move format is the same as for play: x y digit. 
        # If there is no legal move, output resign. The command status is = 1. 
        if self.grid is None:
            print("No game has been started yet.", file=sys.stderr)
            print("= -1\n")
            return False
        empty_cells = [(x, y) for x in range(self.width) for y in range(self.height) if self.grid[y][x] == '.']
        if not empty_cells:
            print("resign")
            return True
        x, y = random.choice(empty_cells)
        digit = random.choice([0, 1])
        self.grid[y][x] = str(digit)
        print(f"{x},{y}, {digit}")
        return True
    
    
    def winner(self, args):
        """  #This command checks if the game is over and outputs one of the following game results:
       1
       2
       unfinished
       Output unfinished if the game is not over yet - the next player still has a move. The command status is = 1
       The player who makes the last move wins. 
       In other words, a player who does not have any legal move loses. 
       This will happen sooner or later as the grid fills.


       """
        if self.grid is None:
            print("No game has been started yet.", file=sys.stderr)
            print("= -1\n")
            return
        # Check if the game is over
        empty_cells = [(x, y) for x in range(self.width) for y in range(self.height) if self.grid[y][x] == '.']
        if not empty_cells:
            print("1")
            return True
        # Check if the next player has a move
        next_player = 1 if self.current_player == 0 else 0
        for x, y in empty_cells:
            if self.is_legal(x, y, next_player):
                print("unfinished")
                return True
        print(str(self.current_player))
        return True
    
    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()