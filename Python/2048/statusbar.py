from support import *

class StatusBar(tk.Frame):
        """
                Description:
                    Creates a statusbar class (inherits from tk.Frame) that contains and maintains information about score and remaining undos,
                    as well as a button to start a new game and a button to undo the previous move

                Example usage:
                    >>> statusbar = StatusBar(tk.tk())
        """
        def __init__(self, master: tk.Tk, **kwargs) -> None:
                """
                        Description:
                            Initialises a Frame widget with given inputs
                            The Frame contains visual information to display the current status of the game

                        Parameters:
                            master  : Pass the root tkinter intepreter and root window for the Frame 
                            **kwargs: List of additional arguments added for any named arguments supported by Frame
                            Frame is created with default dimensions and background color per gradescope requirements

                        Example usage:
                            >>> frame = StatusBar(tk)

                """
                super().__init__(master, height = BOARD_HEIGHT, width = BOARD_WIDTH, bg = "#bbada0")
                # Score
                self._scoreLabelTitle = tk.Label(self, text = "SCORE", font = ('Arial bold', 12), bg = "#bbada0", fg = "#ccc0b3")
                self._scoreLabelTitle.grid(row = 1, column = 1, columnspan = 2, padx = 50, sticky = tk.S)
                self._scoreLabelText = tk.Label(self, text = "YES", font = ('Arial bold', 12), bg = "#bbada0", fg = "#f5ebe4")
                self._scoreLabelText.grid(row = 2, column = 1, columnspan = 2, padx = 50, sticky = tk.N)
                # Undo
                self._undoLabelTitle = tk.Label(self, text = "UNDOS", font = ('Arial bold', 12), bg = "#bbada0", fg = "#ccc0b3")
                self._undoLabelTitle.grid(row = 1, column = 3, columnspan = 2, padx = 50, sticky = tk.S)
                self._undoLabelText = tk.Label(self, text = "YES", font = ('Arial bold', 12), bg = "#bbada0", fg = "#f5ebe4")
                self._undoLabelText.grid(row = 2, column = 3, columnspan = 2, padx = 50, sticky = tk.N)
                # Undo Button
                self._undoButton = tk.Button(self, text="Undo Move")
                self._undoButton.grid(row = 1, column = 5, pady = 2, padx = 20)
                # New Game
                self._newGameButton = tk.Button(self, text="New Game")
                self._newGameButton.grid(row = 2, column = 5, pady = 2, padx = 20)
        
        def redraw_infos(self, score: int, undos: int) -> None:
                """
                        Description:
                            Update the information of the Labels within the Frame

                        Parameters:
                            score: An integer value of the current score
                            undos: An integer value of the current remaining undos available

                        Returns:
                            Updates the Score and Undo Label widgets within the frame

                        Example usage:
                            >>> StatusBar(tk).redraw_infos(Model().get_score(), Model.get_undos())

                """
                self._scoreLabelText.config(text=str(score))
                self._undoLabelText.config(text=str(undos))

        def set_callbacks(self, new_game_command : callable, undo_command: callable) -> None:
                """
                        Description:
                            Update the callback of the buttons within the Frame Widget

                        Parameters:
                            new_game_command: reference to the called function
                            undo_command: reference to the called function 

                        Returns:
                            Updates the callback function of each button corresponding to the referenced function

                        Example usage:
                            >>> StatusBar(tk).set_callbacks(Game().new_game(), Game.undo())

                """
                self._undoButton.configure(command = undo_command)
                self._newGameButton.configure(command = new_game_command)