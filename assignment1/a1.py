# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys
import random

class CommandInterface:
    def __init__(self):
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

    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    def game(self, args):
        """
        Starts a new game by initializing a grid of specified dimensions (width x height).
        Verifies that the grid dimensions are within acceptable bounds (1-20 for both width and height).
        Initializes player turn and count trackers for rows and columns.
        """
        try:
            self.width = int(args[0])
            self.height = int(args[1])
            if not (1 <= self.width <= 20 and 1 <= self.height <= 20):
                raise ValueError("Invalid grid dimensions.")
            self.grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
            self.current_player = 1  # Player 1 starts
        except:
            print("= -1")
            return False
        self.row_count = [[0, 0] for _ in range(self.height)]
        self.col_count = [[0, 0] for _ in range(self.width)]
        return True

    def show(self, args):
        """
        Displays the current state of the game grid. If no game is in progress, prints an error message.
        """
        if self.grid is None:
            print("? No game in progress. Start a new game first.", file=sys.stderr)
            print("= -1")
            return False
        for row in self.grid:
            print(''.join(row))
        return True

    def play(self, args):
        """
        Executes a player's move by placing a digit (0 or 1) at a specific coordinate (x, y).
        Validates the move for proper argument count, valid coordinates, and digit.
        Ensures the move adheres to the "no three consecutive" and "balance" constraints.
        If the move is valid, it updates the grid and switches turns between players.
        """
        if len(args) != 3:
            print(f"= illegal move: {' '.join(args)} wrong number of arguments")
            return False

        try:
            x = int(args[0])
            y = int(args[1])
        except ValueError:
            print(f"= illegal move: {' '.join(args)} wrong coordinate")
            return False

        if (x >= self.width or y >= self.height or x < 0 or y < 0):
            print(f"= illegal move: {' '.join(args)} wrong coordinate")
            return False

        try:
            digit = int(args[2])
        except ValueError:
            print(f"= illegal move: {' '.join(args)} wrong number")
            return False

        if digit not in [0, 1]:
            print(f"= illegal move: {' '.join(args)} wrong number")
            return False

        if self.grid[y][x] != '.':
            print(f"= illegal move: {' '.join(args)} occupied")
            return False

        # triples constraint
        if self.check_triple(x, y, digit) == -1:
            print(f"= illegal move: {' '.join(args)} three in a row")
            return False

        # balance constraint
        if self.check_balance(x, y, digit) == -1:
            print(f"= illegal move: {' '.join(args)} too many {digit}")
            return False

        # make the move
        self.grid[y][x] = str(digit)
        self.row_count[y][digit] += 1
        self.col_count[x][digit] += 1
        self.current_player = 2 if self.current_player == 1 else 1  # Switch turns
        return True

    def legal(self, args):
        """
        Checks if a move is legal by validating the coordinates, digit, and enforcing game rules.
        If the move is legal, it prints "yes", otherwise it prints "no".
        """
        if len(args) != 3:
            print("no")
            return True
        
        try:
            x = int(args[0])
            y = int(args[1])
            digit = int(args[2])
        except ValueError:
            print("no")
            return True
        
        if (x >= self.width or y >= self.height or x < 0 or y < 0):
            print("no")
            return True
        
        if digit not in [0, 1]:
            print("no")
            return True
        
        if self.grid[y][x] != '.':
            print("no")
            return True
        
        if self.check_triple(x, y, digit) == -1:
            print("no")
            return True
        
        if self.check_balance(x, y, digit) == -1:
            print("no")
            return True
        
        print("yes")
        return True

    def check_triple(self, x, y, digit):
        """
        Checks if placing the specified digit (0 or 1) at the position (x, y) would create three consecutive
        digits of the same type either in the row or the column. Returns -1 if this move would break the rule, 1 otherwise.
        """
        row = self.grid[y][:]
        row[x] = str(digit)
        if '000' in ''.join(row) or '111' in ''.join(row):
            return -1
        col = [self.grid[i][x] for i in range(self.height)]
        col[y] = str(digit)
        if '000' in ''.join(col) or '111' in ''.join(col):
            return -1
        return 1
    
    def check_balance(self, x, y, digit):
        """
        Ensures the balance constraint is respected, i.e., no more than half of the digits in a row or column can
        be of the same type (0 or 1). Returns -1 if the move violates the balance constraint, 1 otherwise.
        """
        row_count = sum(1 for cell in self.grid[y] if cell == str(digit))
        if row_count + 1 > (self.width + 1) // 2:
            return -1
        col_count = sum(1 for i in range(self.height) if self.grid[i][x] == str(digit))
        if col_count + 1 > (self.height + 1) // 2:
            return -1
        return 1

    def genmove(self, args):
        """
        Generates and plays a legal move for the current player, if possible. Searches for an empty cell where placing
        a digit would not violate any game rules. If no move is possible, the player resigns.
        """
        if self.grid is None:
            print("No game in progress.")
            print("= -1")
            return False

        empty_cells = [(x, y) for x in range(self.width) for y in range(self.height) if self.grid[y][x] == '.']
        if not empty_cells:
            print("resign")
            return True

        for x, y in empty_cells:
            for digit in [0, 1]:
                if self.check_triple(x, y, digit) != -1 and self.check_balance(x, y, digit) != -1:
                    self.grid[y][x] = str(digit)
                    print(f"{x} {y} {digit}")
                    self.current_player = 2 if self.current_player == 1 else 1
                    return True

        print("resign")
        return True


    def winner(self, args):
        """
        Determines if the game has been won by checking for any empty cells. If no cells are left, the last player
        to move is declared the winner. Otherwise, the game is still unfinished.
        """
        if self.grid is None:
            print("No game in progress.")
            print("= -1")
            return False

        empty_cells = [(x, y) for x in range(self.width) for y in range(self.height) if self.grid[y][x] == '.']
        if not empty_cells:
            print(str(2 if self.current_player == 1 else 1))  # The previous player wins
            return True

        print("unfinished")
        return True

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()