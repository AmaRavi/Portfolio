from support import *
from model import *
from gamegrid import *
from statusbar import *

class Game:
        """
                Description:
                    Creates a controller class that facilitates the communication between the view, model and status bar classes.
                    Also, responsible for maintaining the classes and binding some event handlers

                Example usage:
                    >>> statusbar = StatusBar(tk.tk())
        """
        def __init__(self, master: tk.Tk) -> None:
                """
                        Description:
                            Initialises all the necessary widget and classes. This includes initialising a model to track
                            current game state, a view class to display the current game state, a status bar class to for
                            user to use to monitor the game states. In addition, a file menu is initialised to allow
                            for loading and saving of the game

                        Parameters:
                            master  : Pass the root tkinter intepreter and root window 

                        Example usage:
                            >>> game = Game(tk)

                """
                # Create master and add title, game title
                self._master = master
                master.title('CSSE1001/7030 2022 Semester 2 A3')
                label = tk.Label(master, text = "2048", font = TITLE_FONT, bg = "#fad74d")
                label.pack(side=tk.TOP, fill = tk.BOTH)
                # Store fileName
                self._filename = None
                # Create a model class to track game state
                self._model = Model()
                # Create view class
                self._grid = GameGrid(self._master)
                self._grid.pack(side=tk.TOP)
                # Create a status bar
                self._statusBar = StatusBar(self._master)
                self._statusBar.set_callbacks(self.start_new_game, self.undo_previous_move)
                self._statusBar.pack()
                # Create a menu bar
                self._menubar = tk.Menu(self._master)
                self._master.config(menu = self._menubar)
                # Create file within menubar
                self._filemenu = tk.Menu(self._menubar)
                self._menubar.add_cascade(label="File", menu=self._filemenu)
                # Create the Menubar options within File
                self._filemenu.add_command(label="Save Game", command=self.save_game)
                self._filemenu.add_command(label="Load Game", command=self.load_game)
                self._filemenu.add_command(label="New Game", command=self.start_new_game)
                self._filemenu.add_command(label="Quit", command=self.quit)
                # Communicate Model and view class
                self.draw()
                # Bind keyboard presses
                master.bind("<Key>", lambda i: self.attempt_move(i))
                
        def draw(self) -> None:
                """
                        Description:
                            Update the information of the GUI by passing the game state from the Model class to the
                            view class

                        Parameters:
                            None: No additional input required

                        Returns:
                            Updates the widgets within the root window with the updated game state

                        Example usage:
                            >>> Game(tk).draw()

                """
                self._grid.redraw(self._model.get_tiles())
                self._statusBar.redraw_infos(self._model.get_score(), self._model.get_undos_remaining())
        
        def attempt_move(self, event: tk.Event) -> None:
                """
                        Description:
                            Updates the game state based on the user input event (i.e. any button press that causes a tkinter event)
                            Note: Only valid events are 'w', 'a', 's', 'd'. Any other events are considered invalid

                            This function dictates the win condition behaviour of the game

                        Parameters:
                            event: tkinter event corresponding to a key press

                        Returns:
                            Updates the game state by applying the move played by the User

                """
                validPress = ['w', 'W', 'a', 'A', 'd', 'D', 's', 'S']
                # Check move
                if event.char in validPress:
                        # Display the updated game state
                        if self._model.attempt_move(event.char):
                                self.draw()
                                # Check win condition: Restart or Quit respectively on User decision
                                if self._model.has_won():
                                        response = messagebox.askyesno("Game won",WIN_MESSAGE)
                                        if response:
                                                self.start_new_game()
                                        else:
                                                self._master.destroy()
                                else:
                                        self._master.after(150, self.new_tile)
                        else:
                                print('Nothing Happened')
                else:
                        print('Invalid Move')
                
        def new_tile(self) -> None:
                """
                        Description:
                            Update the information of the game state once a move is complete.
                            Note: A random tile is added only if a tile space is availble to do so

                            This function dictates the loss condition behaviour of the game

                        Parameters:
                            None: No additional input required

                        Returns:
                            Updates the game state by adding a random tile if available and checking loss condition

                        Example usage:
                            >>> Game(tk).new_tile()

                """
                # Add new tile
                try:
                        self._model.add_tile()
                except:
                        print('No Tile Available')
                self.draw()
                # Check loss condition
                if self._model.has_lost():
                        response = messagebox.askyesno("Game lost",LOSS_MESSAGE)
                        if response:
                                self.start_new_game()
                        else:
                                self._master.destroy()
                else:
                        print('Game Continues')

        def undo_previous_move(self) -> None:
                """
                        Description:
                            Update the information of the game state to the previous state before the last move from the user

                        Parameters:
                            None: No additional input required

                        Returns:
                            Updates the game state by updating the tiles and score stored within the Model class

                        Example usage:
                            >>> Game(tk).undo_previous_move()

                """
                self._model.use_undo()
                self.draw()
                
        def start_new_game(self) -> None:
                """
                        Description:
                            Update the information of the game state to a new game state

                        Parameters:
                            None: No additional input required

                        Returns:
                            Updates the game state by updating the tiles and score stored of a new game and resetting the file name of the game

                        Example usage:
                            >>> Game(tk).start_new_game()

                """
                self._filename = None
                self._model.new_game()
                self.draw()
                
        def save_data(self) -> str:
                """
                        Description:
                            Convert game state data into a string

                        Parameters:
                            None: No additional input required

                        Returns:
                            string: Contains current game state data

                        Example usage:
                            >>> data = Game(tk).save_data()

                """
                score = str(self._model.get_score()) + '\n'
                undo = str(self._model.get_undos_remaining()) + '\n'
                previousScore = str(self._model.get_previousScore()) + '\n'
                storeScore = self._model.get_storeScore()
                text = score + undo + previousScore + storeScore
                return text

        def save_game(self) -> None:
                """
                        Description:
                            Saves the game state data into a text file.

                            Data Contains:
                            Current Game grid including grid states up to 3 previous moves
                            Current Score including score values up to 3 previous moves
                            Current number of undos available
                            A security code to validate file

                        Parameters:
                            None: No additional input required

                        Returns:
                            Creates a text file (.txt) containing data of the game state under a user inputed name and file location

                        Example usage:
                            >>> Game(tk).save_game()

                """
                # Retrieve file name and location and open file for writing
                files_extensions = [('Text Document', '*.txt')]
                fileSave = filedialog.asksaveasfile(filetypes = files_extensions, defaultextension = files_extensions)
                if fileSave is not None:
                        fileSave.write("2048 by s4722774\n")
                        fileSave.write(self.save_data())
                        # Write each value within the grid on each new line and repeat for saved grid states
                        for row in self._model.get_tiles():
                                fileSave.write("\n".join(str(item) for item in row))
                                fileSave.write("\n")
                        for row in self._model.get_oldTiles():
                                fileSave.write("\n".join(str(item) for item in row))
                                fileSave.write("\n")
                        for row in self._model.get_oldTiles2():
                                fileSave.write("\n".join(str(item) for item in row))
                                fileSave.write("\n")
                        for row in self._model.get_oldTiles3():
                                fileSave.write("\n".join(str(item) for item in row))
                                fileSave.write("\n")
                        # Close file
                        fileSave.close()

        def load_game(self) -> None:
                """
                        Description:
                            Load the game state data within the selected text file.

                            Data Should contains:
                            Current Game grid including grid states up to 3 previous moves
                            Current Score including score values up to 3 previous moves
                            Current number of undos available
                            A security code to validate file

                            If security code is invalid, a warning message will be displayed
                            NOTE: Only Txt file extensions are allowed

                        Parameters:
                            None: No additional input required

                        Returns:
                            Load the game data stored within the selected file

                        Example usage:
                            >>> Game(tk).save_game()

                """
                # Variables to store the read data
                temp_currentTiles = [None] * 4
                temp_oldTiles = [None] * 4
                temp_oldTiles2 = [None] * 4
                temp_oldTiles3 = [None] * 4
                temp_score = 0
                temp_undo = 0
                temp_oldScore = 0
                temp_storeScore = 0
                temp_storeScore2 = 0
                temp_storeScore3 = 0
                temp_read = []
                files_extensions = [('Text Document', '*.txt')]
                # Request File
                fileLoad = filedialog.askopenfile(mode = 'r', filetypes = files_extensions)
                if fileLoad is not None:
                        for line in fileLoad:
                                # Remove linebreak
                                value = line[:-1]
                                # Add value to the list
                                temp_read.append(value)
                        # Check first line for security check
                        if temp_read[0] == "2048 by s4722774": 
                                # Store score and undo data
                                temp_score = int(temp_read[1])
                                temp_undo = int(temp_read[2])
                                temp_oldScore = int(temp_read[3])
                                temp_storeScore = int(temp_read[4])
                                temp_storeScore2 = int(temp_read[5])
                                temp_storeScore3 = int(temp_read[6])
                                # Retrieve tile data
                                temp_read = temp_read[7:]
                                index = 0
                                print(temp_read)
                                for row in range(4):
                                        temp_list = [None]*4
                                        temp_list2 = [None]*4
                                        temp_list3 = [None]*4
                                        temp_list4 = [None]*4
                                        for col in range(4):
                                                try:
                                                        temp_list[col] = int(temp_read[index])
                                                except ValueError:
                                                        temp_list[col] = None
                                                try:
                                                        temp_list2[col] = int(temp_read[index+16])
                                                except ValueError:
                                                        temp_list2[col] = None
                                                try:
                                                        temp_list3[col] = int(temp_read[index+32])
                                                except ValueError:
                                                        temp_list3[col] = None
                                                try:
                                                        temp_list4[col] = int(temp_read[index+48])
                                                except ValueError:
                                                        temp_list4[col] = None
                                                index = index + 1
                                        temp_currentTiles[row] = temp_list
                                        temp_oldTiles[row] = temp_list2
                                        temp_oldTiles2[row] = temp_list3
                                        temp_oldTiles3[row] = temp_list4
                                print(temp_currentTiles)
                                # Update current game state with data
                                self.load_data(temp_score, temp_undo, temp_oldScore, temp_storeScore, temp_storeScore2, temp_storeScore3, temp_currentTiles, temp_oldTiles, temp_oldTiles2, temp_oldTiles3)
                        else:
                                messagebox.showerror('File Load Error', 'Error: The game you tried to load is not compatible!')
                        
        def load_data(self, score: int, undo: int, oldScore: int, storeScore: int, storeScore2: int, storeScore3: int, tiles: list[list[Optional[int]]], oldtiles: list[list[Optional[int]]], oldtiles2: list[list[Optional[int]]], oldtiles3: list[list[Optional[int]]]) -> None:
                """
                        Description:
                            Load the game state data into the game

                        Parameters:
                            score      : integer of the current score of the game
                            undo       : integer of the remaining number of undos
                            oldScore   : integer of the score one move before the current score
                            storeScore : integer of the score two move before the current score
                            storeScore2: integer of the score three move before the current score
                            storeScore3: integer of the score four move before the current score
                            tiles      : List[List[int]] of the current grid
                            oldTiles   : List[List[int]] of the tiles one move before the current grid
                            oldTiles2  : List[List[int]] of the tiles two move before the current grid
                            oldTiles3  : List[List[int]] of the tiles three move before the current grid

                        Returns:
                            Pass the loaded game data into the model class to update the game state

                """
                self._model.load_model(score, undo, oldScore, storeScore, storeScore2, storeScore3, tiles, oldtiles, oldtiles2, oldtiles3)
                self.draw()
                

        def quit(self) -> None:
                """
                        Description:
                            Quit game upon user request

                        Parameters:
                            None: No additional input required

                        Returns:
                            Closes the root window and tk intepreter

                        Example usage:
                            >>> Game(tk).quit()

                """
                response = messagebox.askyesno("Quit Game", "Are you sure you want to quit?")
                if response:
                        self._master.destroy()