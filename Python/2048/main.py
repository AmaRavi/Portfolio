from support import *
from game import *

def play_game(root):
	# Add a docstring and type hints to this function
	# Then write your code here
        """
                Description:
                    Function called to start an instance of the game

                Parameters:
                    root: Master window and tkinter intepreter

                Returns:
                    Creates necessary classes to begin functionality of the game

                Example usage:
                    >>> play_game(tk.Tk())

        """
        currentGame = Game(root)

if __name__ == '__main__':
	root = tk.Tk()
	play_game(root)
	root.mainloop()
