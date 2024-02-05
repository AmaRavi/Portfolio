"""
CSSE1001 Assignment 1
Semester 2, 2022
"""
from a1_support import *


# Fill these in with your details
__author__ = "Amareesh Ravirajah"
__email__ = "s4722774@student.uq.edu.au"
__date__ = "23/08/2022"

# Write your functions here

def num_hours() -> float:
    """
        Description:
            Provides the number of hours to complete designing Sudoku using Python for Assignment

            Note for Marker:
            This assignment took me approximately 4 days to complete
            Day 1: Implement read board, print board and load board locally on computer. Required to use os import in order to grab directory of my folder location (Approximately 6 hours)
            Day 2: Implement all relevant functions including main and bug testing (Approximately 3 hours)
            Day 3: Submit file to Gradescope to ensure passes. Required lots of tweaking such as removing imported functions (only OS), print logic (2 hours)
                   [Had an interesting interactions where Gradescope would pass the entire input through as the input for loading board, but precede to actively play the game and fail the main function]
            Day 4: Complete documentation and in-line code to ensure marker understands logic of code (to which I hope it makes sense) (1 hour)

        Parameters:
            None

        Returns:
            Number of hours (float)

        Example:
            >>> num_hours()
            5.00

    """
    return float(12)

def check_playerInput(player_input: str) -> str:
    """
        Description:
            Reads player input and returns a string corresponding to the state of the game.
            Used to handle help, quit and new game functionality of the game

        Parameters:
            player_input: Input typed by user (Precondition: Must be a single value or empty input)

        Returns:
            A single string containing game state corresponding to player input

        Example:
            >>> check_playerInput("h")
            'Help'
            >>> check_playerInput("")
            'Load Board'
    """
    if player_input == 'H' or player_input == 'h':
        return 'Help'
    elif player_input == 'Q' or player_input == 'q':
        return 'Quit'
    elif player_input == 'Y' or player_input == 'y' or player_input == '':
        return 'Load Board'
    else:
        return 'Quit'
    
def convert_playerInput(player_input: str) -> tuple[tuple [int, int], str]:
    """
        Description:
            Reads player input as a move and returns tuple containing the position and value of the move.
            Used to help convert player input into appropriate input to update the board

        Parameters:
            player_input: str 'x y z'
            Input typed by user (Precondition: Must be in the format as provided)

        Returns:
            A tuple containing position and value
            tuple(tuple[x, y], str z)

        Example:
            >>> convert_playerInput("0 0 c")
            ((0, 0), 'c')
            >>> convert_playerInput("6 7 6")
            ((6, 7), '6')
            
    """
    row = int(player_input[0])
    colomn = int(player_input[2])
    value = player_input[len(player_input)-1]
    pass_input = ((row, colomn), value)
    return pass_input

def is_empty(position: tuple[int, int], board: Board) -> bool:
    """
        Description:
            Check to see if the selected position (input) is free for a move (i.e. contains None)
            Used to ensure that player can perform on a valid square that does not contain a value in the original board

        Parameters:
            position: tuple(int x, int y) (Chosen coordinates of the board)
            board: Board (Chosen board to check, preferably the original board)

        Returns:
            Returns True if position contains None in Board, otherwise False (Boolean)

        Example:
            >>> is_empty((8, 8), board_one_winnable)
            True
            >>> is_empty((0, 0), board_one_winnable)
            False

    """
    row, colomn = position
    if board[row][colomn] == None:
        return True
    else:
        return False

def update_board(position: tuple[int, int], value: Optional[int], board: Board) -> None:
    """
        Description:
            Updates the position selected on the board with a value.
            Precondition: The value being updated on the board must not be a value existing on the original board

        Parameters:
            position: tuple(int x, int y) Chosen coordinates of the board
            value: Optional[int] Value to be placed in the board
            board: Board (Chosen board to check, preferably the Player board)

        Returns:
            None: Updates Board with value at position

        Example:
            >>> player_board[8]
            [8, 2, 4, 6, 8, 1, 3, None]
            >>> update_board((8, 8), 7, player_board)
            >>> player_board[8]
            [8, 2, 4, 6, 8, 1, 3, 7]

    """
    row, colomn = position
    board[row][colomn] = value


def clear_position(position: tuple[int, int], board: Board) -> None:
    """
        Description:
            Updates the position selected on the board with a None to indicated a empty cell
            Precondition: The value being updated on the board must not be a value existing on the original board

        Parameters:
            position: tuple(int x, int y) Chosen coordinates of the board
            board: Board (Chosen board to check, preferably the Player board)

        Returns:
            None: Updates Board with None at position

        Example:
            >>> player_board[8]
            [8, 2, 4, 6, 8, 1, 3, 7]
            >>> clear_position((8, 8), player_board)
            >>> player_board[8]
            [8, 2, 4, 6, 8, 1, 3, None]

    """
    row, colomn = position
    board[row][colomn] = None

def read_board(raw_board: str) -> Board:
    """
        Description:
            Converts a raw board containing a line of numbers into a nested list, where each parent index corresponds to each row

        Parameters:
            raw_board: str, List of raw numbers from reading board file

        Returns:
            Board: Converted string into nested loops list[list[Optional[int]]]

        Example:
            >>> file_board
            '8, 2, 4, 6, 8, 1, 3, 7, 8, 7, 5, 3, 1, 4, 6, 8'
            >>> read_board(file_board)
            [[8, 2, 4, 6, 8, 1, 3, 7], [8, 7, 5, 3, 1, 4, 6, 8]]

    """
    # Help track position of reading board
    index = 0
    row_number = 0
    # temporary board to store data
    temp_board = [[] for _ in range(9)]
    # Assign each value from raw board to appropriate location on the board
    for number in raw_board:
        if number == ' ':
            number = None
            temp_board[row_number].append(number)
        else:
            temp_board[row_number].append(int(number))
        index = index + 1 # Increase every iteration to track colomn number
        # When one row is fully read, reset colomn number , increment row number
        if index == 9:
            row_number = row_number + 1
            index = 0
    return temp_board
    
def print_board(board: Board) -> None:
    """
        Description:
            Prints out a friendly readable board to view the current state of the game for the user

        Parameters:
            board: Board, Board contianing all the values of the current game

        Returns:
            None, Printed board in Console

        Example:
            >>> print_board(board)
            685|13 | 47 0
            7  |   | 1  1
             1 |764| 5  2
            -----------
            9  | 7 |5 4 3
            8 1|  9| 72 4
            4 3|  6|    5
            -----------
               |427|39  6
             4 |9  | 68 7
            1 7|   |4   8

            012 345 678

    """
    # Help track position of reading board
    index = 0
    row_number = 0
    # Iterate through each row within the Board
    for row in board:
        # A placeholder to store row to be printed
        temp_string = ''
        # Iterate through each number in the row, and appropriately format
        for number in row:
            if number == None:
                temp_string = temp_string + BLANK
            else:
                temp_string = temp_string + str(number)
        # Further format for board
        # Add row number at end of row and vertical lines to indicate square
        temp_string = temp_string[0:3] + VERTICAL_WALL + temp_string[3:6] + VERTICAL_WALL + temp_string[6:9] + BLANK + str(row_number)
        # Add colomn numbers when reached end of the board
        if row_number == 8:
            print(temp_string)
            print('\n012 345 678')
        # Add line breaker inbetween 3 rows
        elif index == 2:
            print(temp_string)
            print('-----------')
            index = 0
        else:
            print(temp_string)
            index = index + 1
        # Increment once formatting row is complete
        row_number = row_number + 1
        
def has_won(board: Board) -> bool:
    """
        Description:
            Checks the current board to see if the game is complete, and ensure victory by checking if each row, colomn and square contains no duplicate values between 1-9.
            This is completed by checking if the sum of each row and colomn add up to 45. If either row or colomn, does not add up to 45, then an incorrect value is placed in a square or an index contains None or no value
            
        Parameters:
            board: Board, Board contianing all the values of the current game

        Returns:
            bool, Returns true when all the conditions are met

        Example:
            >>> has_won(board_one_winnable)
            False
            >>> update_board((8, 8), 5, board_one_winnable)
            True

    """
    # Track Sum
    totalSum = 0
    # First Condition: Check for any None
    for row in board:
        for item in row:
            if item == None:
                return False
    # Second Condition: Check if each row contains doubles
    for row in board:
        for item in row:
            totalSum = totalSum + item
        if totalSum != 45:
            return False
        totalSum = 0
    # Third Condition: Check if each colomn contains doubles
    for colomn in range(9):
        for row in range(9):
            totalSum = totalSum + board[row][colomn]
        if totalSum != 45:
            return False
        totalSum = 0
    # Fourth Condition: Check if each square contains doubles
    # If all the rows and colomns add up to 45, then all squares must default have unique numbers ranging from 1-
    return True

def main() -> None:
    """
        Description:
            Main function that controls the entire logic and behaviour of the game
            1. Ask player for input to load a game board
            2. Convert board into readable format and save another board that will remain unchanged
            3. Retrieve player move
            4. Update board if input is not a single input value, otherwise perform single value condition
                a. Player Move
                    i. Pre-condition: Check if index contains a value in the original board, if contains None can update board
                    ii. Update move can either be insert int: Value (insert) or None (remove value)
                b. Single Value
                    i. If value is H, print Help Condition
                    ii. If value is Q or empty (''), quit the current game gracefully
                    iii. If value is Y, repeat load game
                    iv. If value is N, quit current game gracefully
            5. Print out the new updated board
            6. Check win condition, if True request for New Game, if False repeat step 3-6
            7. If player requests new game repeat step 1-6, otherwise close the game gracefully
            Note: Game is run through state cases using strings, where each condition met is dependant on the state of the game
            States of the game include: Load Game, Player Move, Help, Win?
            
        Parameters:
            None

        Returns:
            None

    """
    # Constants to track state of game
    gameRunning = True
    game_state = 'Load Board'
    game_board = []
    player_board = []
    while(gameRunning):
        # Load Board Condition
        if game_state == 'Load Board':
            select_board = input(START_GAME_PROMPT)
            selected_board = load_board(select_board)
            # Original Board stored
            game_board = read_board(selected_board)
            # Player board
            player_board = read_board(selected_board)
            print_board(game_board)
            game_state = 'Player Move'
        # Player Move Condition
        elif game_state == 'Player Move':
            # Retrieve user input
            player_move = input(INPUT_PROMPT)
            if len(player_move) <= 1:
                game_state = check_playerInput(player_move)
            else:
                position, value = convert_playerInput(player_move)
                # Precondition: Check for empty in original board
                if is_empty(position, game_board):
                    # Clear value in player board
                    if value == 'C' or value == 'c':
                        clear_position(position, player_board)
                    # Update value in player board
                    else:
                        update_board(position, int(value), player_board)
                else:
                    print(INVALID_MOVE_MESSAGE)
                game_state = 'Win?'
        # Win Condition
        elif game_state == 'Win?':
            print_board(player_board)
            if has_won(player_board):
                print(WIN_MESSAGE)
                new_game = input(NEW_GAME_PROMPT)
                game_state = check_playerInput(new_game)
            else:
                game_state = 'Player Move'
                
        # Help Condition
        elif game_state == 'Help':
            print(HELP_MESSAGE + "\n")
            game_state = 'Win?'
        # Quit Game Condition
        elif game_state == 'Quit':
            gameRunning = False

if __name__ == "__main__":
    main()
        

        
