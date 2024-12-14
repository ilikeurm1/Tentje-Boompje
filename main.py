"""Main file"""

# region imports
import sys
import numpy as np
import pygame as pg
import pyautogui as pag # type: ignore
from Utils.Scripts.settings import (
    lives,
    DIMENSION,
    EMPTY,
    GRASS,
    TREE,
    TENT,
    fps_max,
    DEBUG,
    )  # Game constants
from Utils.Scripts.funcs import (
    CREATE_VALID_GAME,
    get_neighbors,
    pretty_print,
    )  # Game functions

# endregion

# region pygame

# Setup
pg.init()
pg.display.set_caption("Tentje Boompje")
pg.display.set_icon(pg.image.load(r"Utils\imgs\TENT.png"))

# Set up the display (setting up with fullscreen being: 1280x720)
screen_width: int = round(
    pg.display.Info().current_w * 0.5078125
)  # Screen width is 650 for 1280x720
screen_height: int = round(
    pg.display.Info().current_h * (0.5 + 1 / 3)
)  # Screen height is 600 for 1280x720

if DEBUG:
    print(
        f"Screen width: {pg.display.Info().current_w}, Screen height: {pg.display.Info().current_h}"
    )
    print(f"Game width: {screen_width}, Game height: {screen_height}")

screen: pg.Surface = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()

# endregion

# region classes
class Tent:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.image = pg.image.load(r"Utils\imgs\TENT.png")  # Load the image
        self.image = pg.transform.scale(
            self.image, (TILESIZE, TILESIZE)
        )  # Scale the image
        self.rect = self.image.get_rect(center=pos)  # Get the rect of the image

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Tree:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.image = pg.image.load(r"Utils\imgs\TREE.png")
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Grass:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.image = pg.image.load(r"Utils\imgs\GRASS.png")
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.image, self.rect)


class Text:
    def __init__(self, text: str, pos: tuple[int, int]) -> None:
        self.font = pg.font.Font(None, 24)
        self.text: pg.Surface = self.font.render(text, True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=pos)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.text, self.textRect)


class FPSCounter:
    """fps counter class"""

    def __init__(
        self,
        surface: pg.Surface,
        font: pg.font.Font,
        clock: pg.time.Clock,
        color: tuple[int, int, int],
        pos: tuple[int, int, int, int],
    ):
        self.surface = surface
        self.font = font
        self.clock = clock
        self.color = color
        self.pos = pos

        self.fps_text = self.font.render(
            str(int(self.clock.get_fps())) + "FPS", False, self.color
        )
        self.fps_text_rect = self.fps_text.get_rect(
            center=(self.pos[0] + (self.pos[2] // 2), self.pos[1] + (self.pos[3] // 2))
        )

    def draw(self):
        # Draw the counter
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        text = f"FPS: {self.clock.get_fps():2.0f}"
        self.fps_text = self.font.render(text, True, self.color)
        self.fps_text_rect = self.fps_text.get_rect(
            center=(self.pos[0] + (self.pos[2] // 2), self.pos[1] + (self.pos[3] // 2))
        )


class LivesCounter:
    def __init__(self, lives: int, pos: tuple[int, int]) -> None:
        self.lives = lives
        self.font = pg.font.Font(None, 24)
        self.text = self.font.render(f"LIVES LEFT: {self.lives}", True, (255, 255, 255))
        self.textRect = self.text.get_rect(topright=pos)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.text, self.textRect)

    def update(self, lives: int) -> None:
        self.lives = lives
        self.text = self.font.render(f"LIVES LEFT: {self.lives}", True, (255, 255, 255))
        self.textRect = self.text.get_rect(topright=self.textRect.topright)


# endregion

# region vars

top_margin: int = int(
    screen_height * 0.05
)  # Margin = 30 pixels if the game has 600 height

# The size of the tiles which has to be the whole screen width divided by the dimension of the board
TILESIZE = round(((screen_height - top_margin) // (DIMENSION + 1)) * 0.85)
margin: int = 7

# Fps counter
fps_counter = FPSCounter(
    screen, pg.font.Font(None, 24), clock, (255, 255, 255), (5, 0, 75, 30)
)

# Lives counter
lives_counter: LivesCounter = LivesCounter(lives, (screen_width - 5, 5))

running: bool = True

# endregion

# region Events

# Clear events event
CLEAR_EVENTS = pg.USEREVENT + 1
# Clear every 5 seconds
pg.time.set_timer(CLEAR_EVENTS, 5000)

# Update board event
UPDATE_BOARD = pg.USEREVENT + 2

# endregion

# region Functions

def convert_cords(i: bool, pos: tuple[int, int]) -> tuple[int, int]:
    """Returns the pos into index cords or pixel cords.

    Args:
        i (bool): if the position given is in index cords or pixel cords.
        pos (tuple[int, int]): the position in i format.

    Returns:
        tuple[int, int]: the position in the other format.
    """
    x = pos[0]
    y = pos[1]
    
    if i:
        return (
                int((margin + TILESIZE) * x + margin + top_margin * 2),
                int((margin + TILESIZE) * y + margin + top_margin * 2),
            )
    else:
        return (
            int((x - margin - top_margin * 2) / (margin + TILESIZE)),
            int((y - margin - top_margin * 2) / (margin + TILESIZE)),
        )

def get_positions_of_all_PIECES(
    pieces: list[tuple[int, tuple[int, int], bool]]
    ) -> list[tuple[int, tuple[int, int], bool]]:
    """Get all the positions of the pieces.

    Args:
        pieces (list[tuple[int, tuple[int, int], bool]]): the pieces list with indexes instead of x and y cords.

    Returns:
        pieces (list[tuple[int, tuple[int, int], bool]]): the pieces list with x and y cords instead of indexes.
    """
    for i, piece in enumerate(pieces):
        pos = piece[1]
        x = pos[0]
        y = pos[1]
        """
        The cords are in the form of indexes, so we have to convert them to the cords.
        We put y first because in a list:
        y = rows
        x = columns
        
        so:
        [
            [(x, y), (3, 1), (1, 6)],
            [(6, 8), (1, 6), (a, b)],
            [(c, d), (3, 1), (5, 7)]
        ]
        
        (x, y) = [0][0]
        (a, b) = [1][2]
        (c, d) = [2][0]
        
        row down (y += 1) | down (y -= 1)
        column right (x += 1) | left (x -= 1)
        """
        pos = (
            int((margin + TILESIZE) * y + margin + top_margin * 2),
            int((margin + TILESIZE) * x + margin + top_margin * 2),
        )
        # Change the position to the cords
        new_piece = (piece[0], pos, piece[2])
        pieces[i] = new_piece

    return pieces

def draw_board(
    screen: pg.surface.Surface,
    board: np.ndarray,
    pieces: list[tuple[int, tuple[int, int], bool]],
    ) -> None:
    """Draws the board on the disply.

    Args:
        screen (pg.surface.Surface): The display to draw on.
        board (np.ndarray): the board list.
        pieces (list[tuple[int, tuple[int, int], bool]]): The list of pieces and their position also if to draw them or not.
    """

    for y in range(DIMENSION + 1):
        for x in range(DIMENSION + 1):
            pos = convert_cords(True, (x, y))
            
            for i, piece_pos in enumerate([piece[1] for piece in pieces]):
                if pos == piece_pos:
                    if pieces[i][2]:  # If the pieces boolean is True
                        if pieces[i][0] == TREE:
                            Tree(piece_pos).draw(screen)
                            break
                        elif pieces[i][0] == TENT:
                            Tent(piece_pos).draw(screen)
                            break

            else:
                if y == 0 or x == DIMENSION:
                    Text(str(board[y][x]), pos).draw(screen)
                else:
                    if board[y][x] == EMPTY:
                        # Grass(pos).draw(screen)
                        Text("Empty", pos).draw(screen)
                    elif board[y][x] == GRASS:
                        Grass(pos).draw(screen)

def clicked_on_tent(board: np.ndarray, pos: tuple[int, int]) -> None:
    """When the player clicks on a tent we update the board to show that the player clicked on a tent.

    Args:
        board (np.ndarray): the current board position
        pos (tuple[int, int]): position of the tent (in pixels)
    """
    
    # Convert the pixel positions to indexes
    row, col = convert_cords(False, pos)
    
    # Get all the surrounding
    neighbors = get_neighbors((row, col), 8)
    
    # set all the surrounding spaces to grass
    for n_col, n_row in neighbors:
        if board[n_row][n_col] != TREE and n_row != 0 and n_col != DIMENSION:
            board[n_row][n_col] = GRASS

    # Update the board
    board[col][DIMENSION] -= 1
    board[0][row] -= 1
    
    # if the row is empty set all the spaces to grass
    if board[0][row] <= 0:
        for x in range(1, DIMENSION + 1):
            if board[x][row] == EMPTY:
                board[x][row] = GRASS

    # if the column is empty set all the spaces to grass
    if board[col][DIMENSION] <= 0:
        for y in range(DIMENSION):
            if board[col][y] == EMPTY:
                board[col][y] = GRASS

# endregion


# Main function
def main() -> int:
    """Main function."""
    # region main
    
    global running
    global lives
    
    while running:
        # Create the game board
        board, trees_and_tents = CREATE_VALID_GAME()

        trees_and_tents = get_positions_of_all_PIECES(trees_and_tents)

        # Pretty print the board
        pretty_print(board)

        # Throw a move event to draw the game
        pg.event.post(pg.event.Event(UPDATE_BOARD))

        # Main loop
        while lives != 0: # While the player has lives
            # Play the game:
            # Clear the screen
            screen.fill((0, 0, 0))

            # Event handling
            for e in pg.event.get():
                if DEBUG:
                    if e.type not in (pg.MOUSEMOTION, pg.WINDOWENTER, pg.WINDOWLEAVE, CLEAR_EVENTS, pg.ACTIVEEVENT, pg.WINDOWEXPOSED, pg.WINDOWMOVED, pg.VIDEOEXPOSE):
                        print(f"Event: {e}")

                if e.type == pg.QUIT:
                    lives = 0 
                    running = False

                elif e.type == CLEAR_EVENTS:
                    pg.event.clear()

                # Main game event
                elif e.type == pg.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        # Update the board
                        for i, PIECE in enumerate(trees_and_tents):
                            # Piece name
                            name = PIECE[0]

                            # Piece cords
                            piece_cords = PIECE[1]
                            piece_x = piece_cords[0]
                            piece_y = piece_cords[1]

                            # If the user clicked on a piece (tree or tent)
                            if (
                                # mouse x-pos is in the range of the piece
                                (
                                    (piece_x - TILESIZE // 2)
                                    < e.pos[0]
                                    < (piece_x + TILESIZE // 2)
                                )
                            ) and (
                                # mouse y-pos is in the range of the piece
                                (
                                    piece_y - TILESIZE // 2
                                    < e.pos[1]
                                    < (piece_y + TILESIZE // 2)
                                )
                            ):
                                # If the piece is a Tent and it hasn't been placed yet
                                if name == TENT and not PIECE[2]:
                                    PIECE = (name, (piece_x, piece_y), True)
                                    trees_and_tents[i] = PIECE
                                    # Update the far right column
                                    board[0][DIMENSION] -= 1
                                    clicked_on_tent(board, piece_cords)

                                    pg.event.post(pg.event.Event(UPDATE_BOARD))

                                else:
                                    print("That's a tree... or a tent you've already clicked...")

                                break
                        else:
                            # Decrease lives when the player clicks on a wrong space
                            lives -= 1

                            pg.event.post(pg.event.Event(UPDATE_BOARD))

                # region user events

                elif e.type == UPDATE_BOARD:
                    # Draw the board
                    draw_board(
                        screen, board, trees_and_tents
                    )  # Only draw the board when asked -> fps baby!!!!

                    # Update the lives_counter
                    lives_counter.update(lives)
                    # Draw the lives counter
                    lives_counter.draw(screen)

                    # Update the ENTIRE display (doesn't matter much here wince we won't save much performance by updating only the places that changed)
                    pg.display.flip()

                # endregion

            # Update everything
            fps_counter.update()

            # Draw everything
            fps_counter.draw()

            # Define which places to update
            fps_counter_space = pg.rect.Rect(0, 0, 100, 30)
            line = pg.draw.line(
                screen, (200, 200, 200), (0, top_margin), (screen_width, top_margin)
            )

            # Update the display
            pg.display.update([fps_counter_space, line])
            clock.tick(fps_max)
            
            # Check if the player has won
            if board[0][DIMENSION] == 0:
                # Show the last tent clicked
                draw_board(screen, board, trees_and_tents)
                
                # Draw the lives counter (so it doesn't dissapear)
                lives_counter.draw(screen)
                
                # Update the display
                pg.display.flip()

                break # Break the loop if the player has won

        if lives == 0:
            pag.alert(text="You've lost", title="You lost 😥", button="OK")
        else:
            pag.alert(text="You've won", title="You won 🎉", button="OK")

        running = (
            False
            if pag.confirm(text='You want to go again?', title='Go again?', buttons=['Y', 'N']) == 'N'
            else True
        )
        if running:
            lives = 3

        # endregion

    pg.quit()
    sys.exit(0)
    return 0


# region main
if __name__ == "__main__":
    main()
    print("Program exited successfully\nexit code: 0")
    exit(0)

    # except Exception as e:
    #     print(f"An error occurred: {e}\nexit code: you choose lmao 1 ig?")
    #     exit(1)

# endregion
