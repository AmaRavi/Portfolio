import numpy as np
from support import *

def generate_tile(current_tiles: list[list[Optional[int]]]) -> tuple[tuple[int, int], int]:
    """ Generates a random position for a new tile, and the number (either 2 or
    4) to display on that tile.

    Parameters:
        current_tiles: The tiles currently on the grid. This is a list of rows
                       in the grid (i.e. each internal list represents one
                       row), where each element is the number on the tile (or
                       None if no tile exists) at the corresponding row in the
                       column.

    Returns:
        A tuple containing ((row, column), value), where (row, column) is the
        position for the new tile, and value is the value for that tile (either
        2 or 4.)
    """
    candidate_positions = []
    for i, row in enumerate(current_tiles):
        for j, tile in enumerate(row):
            if tile is None:
                candidate_positions.append((i, j))
    return random.choice(candidate_positions), random.choice([2] * 5 + [4])

def stack_left(tiles: list[list[Optional[int]]]) -> list[list[Optional[int]]]:
    """ Moves all tiles as far as possible to the left without merging.

    Parameters:
        tiles: The tiles currently on the grid, where each internal list
               represents a row in the grid.

    Returns:
        A copy of the tiles list, in which all the tiles have stacked to the left.
    """
    stacked_tiles = [[None for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for i in range(NUM_ROWS):
        to_fill = 0
        for j in range(NUM_COLS):
            if tiles[i][j] is not None:
                stacked_tiles[i][to_fill] = tiles[i][j]
                to_fill += 1
    return stacked_tiles

def combine_left(tiles: list[list[Optional[int]]]) -> list[list[Optional[int]]]:
    """ Merges tiles to the left (i.e. if two 8's are next to each other
    horizontally, this method will merge them together into a single 16 tile,
    which sits as far left as possible.)

    Parameters:
        tiles: The tiles currently on the grid, where each internal list
               represents a row in the grid.

    Returns:
        A copy of the tiles list, in which merges have been made to the left.
    """
    combined_tiles = [row[:] for row in tiles]
    score_added = 0
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS - 1):
            if combined_tiles[i][j] is not None and combined_tiles[i][j] == combined_tiles[i][j + 1]:
                combined_tiles[i][j] *= 2
                combined_tiles[i][j + 1] = None
                score_added += combined_tiles[i][j]
    return combined_tiles, score_added

def reverse(tiles: list[list[Optional[int]]]) -> list[list[Optional[int]]]:
    """ Flips the grid of tiles horizontally.

    Parameters:
        tiles: The tiles currently on the grid, where each internal list
               represents a row in the grid.

    Returns:
        A copy of the tiles list, which has been flipped horizontally.
    """
    reversed_tiles = []
    for i in range(NUM_ROWS):
        reversed_tiles.append([])
        for j in range(NUM_COLS):
            reversed_tiles[i].append(tiles[i][3-j])
    return reversed_tiles

def transpose(tiles: list[list[Optional[int]]]) -> list[list[Optional[int]]]:
    """ Transposes the grid of tiles.

    Parameters:
        tiles: The tiles currently on the grid, where each internal list
               represents a row in the grid.

    Returns:
        A copy of the tiles, transposed.
    """
    transposed_tiles = [[None for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            transposed_tiles[i][j] = tiles[j][i]
    return transposed_tiles

class Model:
        """
                Description:
                    Creates a model class that contains and maintains the state of the game

                Example usage:
                    >>> model = Model()
        """
        def __init__(self) -> None:
                """
                        Description:
                            Create a new game upon initialisation of model class

                        Parameters:
                            None: No additional information required

                        Returns:
                            A single class model for a new game
                """
                self.new_game()

        def new_game(self) -> None:
                """
                        Description:
                            Create a new game by reseting all game relevant variables (such as Tiles, score, memory of previous tiles for undo, etc.). Once reset, add two new tiles to start the game

                        Parameters:
                            None: No additional information required

                        Returns:
                            Resets all current game state information for a new game

                        Example usage:
                            >>> model = Model().new_game()
                """
                self._tiles = self.create_list()
                self._score = 0
                self._undo = 3
                self.add_tile()
                self.add_tile()
                self._previousTiles = self._tiles
                self._storeTiles = self._tiles
                self._storeTiles2 = self._tiles
                self._storeTiles3 = self._tiles
                self._previousScore = 0
                self._storeScore = 0
                self._storeScore2 = 0
                self._storeScore3 = 0
                        
        def get_tiles(self) -> list[list[Optional[int]]]:
                """
                        Description:
                            Retrieve the current set of tiles

                        Parameters:
                            None: No additional information required

                        Returns:
                            A list of each row (also a list) within the tile grid of the game

                        Example usage:
                            >>> tiles = Model().get_tiles()
                """
                return self._tiles
        
        def get_oldTiles(self) -> list[list[Optional[int]]]:
                """
                        Description:
                            Retrieve the set of tiles (before the current set of tiles) that were changed

                        Parameters:
                            None: No additional information required

                        Returns:
                            A list of each row (also a list) within the tile grid of the game

                        Example usage:
                            >>> tiles = Model().get_oldTiles()
                """
                return self._previousTiles

        def get_oldTiles2(self) -> list[list[Optional[int]]]:
                """
                        Description:
                            Retrieve the set of tiles (2 moves before the current set of tiles) that were changed

                        Parameters:
                            None: No additional information required

                        Returns:
                            A list of each row (also a list) within the tile grid of the game

                        Example usage:
                            >>> tiles = Model().get_oldTiles2()
                """
                return self._storeTiles

        def get_oldTiles3(self) -> list[list[Optional[int]]]:
                """
                        Description:
                            Retrieve the set of tiles (3 moves before the current set of tiles) that were changed

                        Parameters:
                            None: No additional information required

                        Returns:
                            A list of each row (also a list) within the tile grid of the game

                        Example usage:
                            >>> tiles = Model().get_oldTiles3()
                """
                return self._storeTiles2

        def create_list(self) -> list[list[Optional[int]]]:
                """
                        Description:
                            Create an empty game grid (4x4) containing a list of Rows, with each row a list of none values

                        Parameters:
                            None: No additional information required

                        Returns:
                            A list of each row (also a list containing None values) within the tile grid of the game

                        Example usage:
                            >>> model = Model().create_list()
                            or
                            >>> model = Model()
                            >>> model.create_list() 
                """
                temp_Tilelist = [None] * NUM_ROWS
                for index in range(NUM_ROWS):
                        temp_Tilelist[index] = [None] * NUM_COLS
                return temp_Tilelist
        
        def add_tile(self) -> None:
                """
                        Description:
                            Add a new random value (2/4) to an available tile within an available space on the grid (replace an existing None value)

                        Example usage:
                            >>> model = Model().add_tile()
                            or
                            >>> model = Model()
                            >>> model.add_tile()
                """
                tileLocation, tileValue = generate_tile(self._tiles)
                self._tiles[tileLocation[0]][tileLocation[1]] = tileValue

        def move_left(self) -> None:
                """
                        Description:
                            Modiy the current list of the game grid to reflect a move change towards the left of the grid. This is achieved by
                            stacking all available tiles to the left, merging any two tiles with the same value to the left (prioritising the left tiles first)
                            and stacking all available tiles to the left.

                        Parameters:
                            None: No additional information required

                        Returns:
                            None: Function returns nothing
                            But modifys the stored tiles within the class with a new list of the game grid reflecting the change of tiles to the left of the grid

                        Example usage:
                            >>> model = Model()
                            >>> model.move_left()
                """
                temp_tiles, points = combine_left(stack_left(self._tiles))
                self._tiles = stack_left(temp_tiles)
                self._score += points

        def move_right(self) -> None:
                """
                        Description:
                            Modiy the current list of the game grid to reflect a move change towards the right of the grid. This is achieved by
                            reversing the current state of the grid, performing a left move (to stack and merge all tiles to the left) then
                            reverse the new state of the grid to return back to original orientation of the state.

                        Parameters:
                            None: No additional information required

                        Returns:
                            None: Function returns nothing
                            But modifys the stored tiles within the class with a new list of the game grid reflecting the change of tiles to the right of the grid

                        Example usage:
                            >>> model = Model()
                            >>> model.move_right()
                """
                temp_tiles, points = combine_left(stack_left(reverse(self._tiles)))
                self._tiles = reverse(stack_left(temp_tiles))
                self._score += points

        def move_up(self) -> None:
                """
                        Description:
                            Modiy the current list of the game grid to reflect a move change towards the top of the grid. This is achieved by
                            transposing the current state of the grid, performing a left move (to stack and merge all tiles to the left) then
                            transposing the new state of the grid to return back to original orientation of the state.

                        Parameters:
                            None: No additional information required

                        Returns:
                            None: Function returns nothing
                            But modifys the stored tiles within the class with a new list of the game grid reflecting the change of tiles to the top of the grid

                        Example usage:
                            >>> model = Model()
                            >>> model.move_up()
                """
                temp_tiles, points = combine_left(stack_left(transpose(self._tiles)))
                self._tiles = transpose(stack_left(temp_tiles))
                self._score += points

        def move_down(self) -> None:
                """
                        Description:
                            Modiy the current list of the game grid to reflect a move change towards the bottom of the grid. This is achieved by
                            transposing and reversing the current state of the grid, performing a left move (to stack and merge all tiles to the left) then
                            reverse and transpose the new state of the grid to return back to original orientation of the state.

                        Parameters:
                            None: No additional information required

                        Returns:
                            None: Function returns nothing
                            But modifys the stored tiles within the class with a new list of the game grid reflecting the change of tiles to the bottom of the grid

                        Example usage:
                            >>> model = Model()
                            >>> model.move_down()
                """
                self._tiles = transpose(self._tiles)
                self.move_right()
                self._tiles = transpose(self._tiles)

        def attempt_move(self, move: str) -> bool:
                """
                        Description:
                            Attempts to perform a move. If a move changes the state of the grid, the move is applied and all game state information is updated to reflect the change

                        Parameters:
                            move: A string value containing a character corresponding to the list of possible moves applicable (i.e. w, a, s, d)

                        Returns:
                            bool: A boolean as a result of a change within the grid, returns False if unchanged.

                        Example usage:
                            >>> change = Model().attempt_move('w')
                            or
                            >>> model = Model()
                            >>> change = model.attempt_move('w')
                """
                # Update game state information before applying move (store values for undo moves)
                old_tiles = self._tiles
                self._storeTiles3 = self._storeTiles2
                self._storeTiles2 = self._storeTiles
                self._storeTiles = self._previousTiles
                self._previousTiles = self._tiles
                self._storeScore3 = self._storeScore2
                self._storeScore2 = self._storeScore
                self._storeScore = self._previousScore
                self._previousScore = self._score
                # Apply the move
                if move == 'w' or move == 'W':
                        self.move_up()
                elif move == 's' or move == 'S':
                        self.move_down()
                elif move == 'a' or move == 'A':
                        self.move_left()
                elif move == 'd' or move == 'D':
                        self.move_right()
                else:
                        print('no move')
                # Check if the state of the grid has been changed as a result of the move
                count = 0
                for indexRow in range(NUM_ROWS):
                        for indexCol in range(NUM_COLS):
                                if old_tiles[indexRow][indexCol] == self._tiles[indexRow][indexCol]:
                                        count += 1
                # Return the grid back to the previous state of the grid before the move is applied if no change has occured
                if count == 16:
                        self._tiles = old_tiles
                        self._previousTiles = self._storeTiles
                        self._storeTiles = self._storeTiles2
                        self._storeTiles2 = self._storeTiles3
                        self._score = self._previousScore
                        self._previousScore = self._storeScore
                        self._storeScore = self._storeScore2
                        self._storeScore2 = self._storeScore3
                        return False
                else:
                        return True

        def has_won(self) -> bool:
                """
                        Description:
                            Checks state of grid for a win condition
                            Win Condition: if grid contains a tile value of 2048

                        Parameters:
                            None: No additional information required

                        Returns:
                            bool: A boolean as a result of the win condition

                        Example usage:
                            >>> win = Model().has_won()
                            or
                            >>> model = Model()
                            >>> win = model.has_won()
                """
                for row in self._tiles:
                        for col in row:
                                if col == 2048:
                                        return True
                return False

        def has_lost(self) -> bool:
                """
                        Description:
                            Checks state of grid for a loss condition
                            Loss Condition: if grid does not contain a None value AND has no change state to the grid when all possible moves are applied

                        Parameters:
                            None: No additional information required

                        Returns:
                            bool: A boolean as a result of the loss condition

                        Example usage:
                            >>> loss = Model().has_loss()
                            or
                            >>> model = Model()
                            >>> loss = model.has_loss()
                """
                # Check if any None exists in current Tile list
                for row in self._tiles:
                        for col in row:
                                if col == None:
                                        return False
                # Store tiles
                temp_tiles = self._tiles
                # Apply all possible moves and change tiles back to its original tiles (this is because the grid is changed if a move is possible)
                if not self.attempt_move('w'):
                        if not self.attempt_move('s'):
                                if not self.attempt_move('a'):
                                        if not self.attempt_move('d'):
                                                self._tiles = temp_tiles
                                                return True
                                        else:
                                                self._tiles = temp_tiles
                                                #print('Passed Right')
                                                return False
                                else:
                                        self._tiles = temp_tiles
                                        #print('Passed Left')
                                        return False
                        else:
                                self._tiles = temp_tiles
                                #print('Passed Down')
                                return False
                else:
                        self._tiles = temp_tiles
                        #print('Passed Up')
                        return False
        
        def get_score(self) -> int:
                """
                        Description:
                            Returns the current score based on the moves applied

                        Parameters:
                            None: No additional information required

                        Returns:
                            int: An integer value of the score

                        Example usage:
                            >>> score = Model().get_score()
                            or
                            >>> model = Model()
                            >>> score = model.get_score()
                """
                return self._score

        def get_previousScore(self) -> int:
                """
                        Description:
                            Returns the previous score from the grid state before 1 move

                        Parameters:
                            None: No additional information required

                        Returns:
                            int: An integer value of the score

                        Example usage:
                            >>> score = Model().get_previousScore()
                            or
                            >>> model = Model()
                            >>> score = model.get_previousScore()
                """
                return self._previousScore

        def get_storeScore(self) -> str:
                """
                        Description:
                            An additional implemented function to handle string handling of the scores for game data saving/loading

                        Parameters:
                            None: No additional information required

                        Returns:
                            str: A string value containing the scores on each line

                        Example usage:
                            >>> scoreString = Model().get_storeScore()
                            or
                            >>> model = Model()
                            >>> scoreString = model.get_storeScore()
                """
                score1 = str(self._storeScore) + '\n'
                score2 = str(self._storeScore2) + '\n'
                score3 = str(self._storeScore3) + '\n'
                return score1 + score2 + score3

        def get_undos_remaining(self) -> int:
                """
                        Description:
                            Returns the number of undos remaining in the current state of the game

                        Parameters:
                            None: No additional information required

                        Returns:
                            int: A integer value containing the scores on each line

                        Example usage:
                            >>> undos = Model().get_undos_remaining()
                            or
                            >>> model = Model()
                            >>> undos = model.get_undos_remaining()
                """
                return self._undo

        def use_undo(self) -> None:
                """
                        Description:
                            Reverts the game state and grid to the state before 1 move was applied. This change only occurs if there is an undo available

                        Parameters:
                            None: No additional information required


                        Example usage:
                            >>> undos = Model().use_undo()
                            or
                            >>> model = Model()
                            >>> model.use_undo()
                """
                if self._undo > 0:
                        self._undo = self._undo - 1
                        self._tiles = self._previousTiles
                        self._previousTiles = self._storeTiles
                        self._storeTiles = self._storeTiles2
                        self._score = self._previousScore
                        self._previousScore = self._storeScore
                        self._storeScore = self._storeScore2
                        self._storeScore2 = self._storeScore3

        def load_model(self, score: int, undo: int, oldScore: int, storeScore: int, storeScore2: int, storeScore3: int, tiles: list[list[Optional[int]]], oldtiles: list[list[Optional[int]]], oldtiles2: list[list[Optional[int]]], oldtiles3: list[list[Optional[int]]]) -> None:
                """
                        Description:
                            An additional function used to change the game state to play a saved game

                        Parameters:
                            All values correspond to the saved game state
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
                            None:
                            But changes the current model state into the loaded game save

                        Example usage:
                            >>> Model().load_model(12, 3, 64, 32, 16, 8, [4x4], [4x4], [4x4])
                            or
                            >>> model = Model()
                            >>> model.load_model(12, 3, 64, 32, 16, 8, [4x4], [4x4], [4x4])
                """
                self._tiles = tiles
                self._score = score
                self._undo = undo
                self._previousTiles = oldtiles
                self._previousScore = oldScore
                self._storeTiles = oldtiles2
                self._storeTiles2 = oldtiles3
                self._storeScore = storeScore
                self._storeScore2 = storeScore2
                self._storeScore3 = storeScore3
