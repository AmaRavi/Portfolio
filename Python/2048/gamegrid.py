from support import *

class GameGrid(tk.Canvas):
        """
                Description:
                    Creates a view class (inherits from tk.Canvas) that displays the state of the game

                Example usage:
                    >>> grid = GameGrid(tk.tk())
        """
        def __init__(self, master: tk.Tk, **kwargs) -> None:
                """
                        Description:
                            Initialises a Canvas with given inputs

                        Parameters:
                            master  : Pass the root tkinter intepreter and root window for the Canvas 
                            **kwargs: List of additional arguments added for any named arguments supported by Canvas
                            Canvas is created with default dimensions and background color provided

                        Example usage:
                            >>> canvas = GameGrid(tk)

                """
                super().__init__(master, height = BOARD_HEIGHT, width = BOARD_WIDTH, bg = BACKGROUND_COLOUR)
                

        def _get_bbox(self, position: tuple[int, int]) -> tuple[int, int, int, int]:
                """
                        Description:
                            Return the bounding box for the (row, column) position

                        Parameters:
                            position: tuple[int, int] Position of tile within the grid

                        Returns:
                            tuple[int, int, int, int]: Location of two points (x1, y1, x2, y2) where (x1, y1) corresponds
                            to top left corner of a box and (x2, y2) corresponds to the bottom right corner of a box.
                            With 10 pixels of padding added and subtraced respectively

                        Example usage:
                            >>> box = GameGrid(tk)._get_bbox((0,1))
                            >>> box
                            >>> (105, 10, 195, 90)

                """
                xmin = 0
                ymin = 0
                xmax = 0
                ymax = 0
                row, colomn = position

                xmin = (row * (BOARD_WIDTH/NUM_COLS))+BUFFER/2
                xmax = (BOARD_WIDTH - ((BOARD_WIDTH - ((BOARD_WIDTH/NUM_COLS)*(row+1))))) - BUFFER/2
                ymin = (colomn * (BOARD_HEIGHT/NUM_ROWS))+BUFFER/2
                ymax = (BOARD_HEIGHT - ((BOARD_HEIGHT - ((BOARD_HEIGHT/NUM_ROWS)*(colomn+1))))) - BUFFER/2
                
                return (xmin, ymin, xmax, ymax)
        
        def _get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
                """
                        Description:
                            Return the centre point for the tile of (row, column) position

                        Parameters:
                            position: tuple[int, int] Position of tile within the grid

                        Returns:
                            tuple[int, int, int, int]: Location of midpoint of the tile location on the grid

                        Example usage:
                            >>> box = GameGrid(tk)._get_midpoint((0,3))
                            >>> box
                            >>> (350.0, 50.0)

                """
                xmin, ymin, xmax, ymax = self._get_bbox(position)
                xmid = (xmax + xmin)/2
                ymid = (ymax + ymin)/2
                return (xmid, ymid)

        def clear(self) -> None:
                """
                        Description:
                            Clears the elements on the Canvas

                        Parameters:
                            None: No additional inputs required

                        Returns:
                            Deletes all active drawings on the grid

                        Example usage:
                            >>> GameGrid(tk).clear()

                """
                self.delete(tk.ALL)
                
        def redraw(self, tiles: list[list[Optional[int]]]) -> None:
                """
                        Description:
                            Draw the view of the game on the Canvas

                        Parameters:
                            tiles: list[list[int] List of tiles of the current game grid

                        Returns:
                            Draws rectangle and colours corresponding to each value within the grid and draw the value of the tile
                            at the midpoint of each tile

                        Example usage:
                            >>> GameGrid(tk).redraw(Model().get_tiles())

                """
                self.clear()
                for x in range(NUM_ROWS):
                        for y in range(NUM_COLS):
                                self.create_rectangle(self._get_bbox((y,x)), fill = COLOURS[tiles[x][y]], outline = COLOURS[tiles[x][y]])
                                if tiles[x][y] is not None:
                                        self.create_text(self._get_midpoint((y,x)), text=tiles[x][y], font = TILE_FONT, fill = FG_COLOURS[tiles[x][y]])

