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
        #This command creates a new game on an empty rectangular grid of width n and height m (both in the range from 1 and 20). 
        # It only requires the command status as output.
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def show(self, args):
        """ This command shows the current state of the grid, one line per row, followed by the command status. Example:
        show
        ..0
        1..
        = 1 """
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def play(self, args):
        """Place the digit (0 or 1) at the given (x,y) coordinate. 
        x increases from left to right, starting at 0. y increases from top to bottom, starting at 0. 
        So the top left corner has coordinates 0 0, and the bottom right is at n-1 m-1. 
        You need to implement basic error handling and return the proper command status. Example:
        play 1 2 0
        = 1"""
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def legal(self, args):
        """ Check if this move (in the same format as in play) is legal. 
        Answer yes or no. 
        The command status is = 1.
        Usage example (on empty 3x3 board):
        game 3 3
        = 1
        legal 0 0 0
        yes
        = 1 """
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
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