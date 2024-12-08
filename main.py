"""Main file"""

# imports
import numpy as np
import pygame as pg
from Utils.Scripts.fps_counter import FPSCounter  # FPS counter
from Utils.Scripts.settings import (
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
    pretty_print
    )  # Game functions

# Main function
def main() -> int:
    """Main function."""
    # region pygame

    # Pygame setup
    pg.init()
    pg.display.set_caption("Tentje Boompje")

    Resolution = (pg.display.Info().current_w, pg.display.Info().current_h)

    # Set up the display (setting up with fullscreen being: 1280x720)
    screen_width: int = round(
        Resolution[0] * 0.5078125
    )  # Screen width is 650 for 1280x720
    screen_height: int = round(
        Resolution[1] * (0.5 + 1 / 3)
    )  # Screen height is 600 for 1280x720

    if DEBUG:
        print(f"Screen width: {Resolution[0]}, Screen height: {Resolution[1]}")
        print(f"Game width: {screen_width}, Game height: {screen_height}")

    top_margin = screen_height * 0.05  # Margin = 30 pixels if the game has 600 height

    # The size of the tiles which has to be the whole screen width divided by the dimension of the board
    TILESIZE = round(((screen_height - top_margin) // (DIMENSION + 1)) * .85)
    margin = 7

    screen: pg.Surface = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()

    # Fps counter
    fps_counter = FPSCounter(
        screen, pg.font.Font(None, 24), clock, (255, 255, 255), (5, 0, 75, 30)
    )

    # Vars
    running: bool = True

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

    # endregion

    # region Events
    # Clear events event
    CLEAR_EVENTS = pg.USEREVENT + 1
    # Clear every 5 seconds
    pg.time.set_timer(CLEAR_EVENTS, 5000)

    # Update board event
    UPDATE_BOARD = pg.USEREVENT + 2

    # Move event
    MOVE_EVENT = pg.USEREVENT + 3

    # endregion

    # endregion

    # funcions
    
    # Drawing functions
    def get_positions_of_all_PIECES(pieces: list[tuple[int, tuple[int, int], bool]]) -> list[tuple[int, tuple[int, int], bool]]:
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

    def draw_board(screen: pg.surface.Surface, board: np.ndarray, pieces: list[tuple[int, tuple[int, int], bool]]):
        """Draws the board on the disply.

        Args:
            screen (pg.surface.Surface): The display to draw on.
            board (np.ndarray): the board list.
            pieces (list[tuple[int, tuple[int, int], bool]]): The list of pieces and their position also if to draw them or not.
        """
        if pieces:
            piece_positions = [piece[1] for piece in pieces]
        
        for y in range(DIMENSION + 1):
            for x in range(DIMENSION + 1):
                pos = (
                    int((margin + TILESIZE) * x + margin + top_margin * 2),
                    int((margin + TILESIZE) * y + margin + top_margin * 2),
                )
                
                for i, piece_pos in enumerate(piece_positions):
                    if pos == piece_pos:
                        if pieces[i][2]: # If the pieces boolean is True
                            if board[y][x] == TREE:
                                Tree(piece_pos).draw(screen)
                            elif board[y][x] == TENT:
                                Tent(piece_pos).draw(screen)                        

                else:
                    if y == 0 or x == DIMENSION:
                        Text(str(board[y][x]), pos).draw(screen)
                    else:
                        if board[y][x] == EMPTY:
                            # Grass(pos).draw(screen)
                            Text("Empty", pos).draw(screen)
                        elif board[y][x] == GRASS:
                            Grass(pos).draw(screen)

    # region main

    # Create the game board
    board, game_board_positions = CREATE_VALID_GAME()
    
    game_board_positions = get_positions_of_all_PIECES(game_board_positions)

    # Pretty print the board
    pretty_print(board)
    
    # Throw a move event to draw the game
    pg.event.post(pg.event.Event(UPDATE_BOARD))

    # Main loop
    while running:
        screen.fill((0, 0, 0))

        # Event handling
        for e in pg.event.get():
            if DEBUG:
                if e.type != pg.MOUSEMOTION:
                    print(f"Event: {e}")

            if e.type == pg.QUIT:
                running = False
                
            elif e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    print(f"Mouse pos: {e.pos}")
                    for i, PIECE in enumerate(game_board_positions):
                        # Piece name
                        name = PIECE[0]
                        
                        # Piece cords
                        piece_cords = PIECE[1]
                        piece_x = piece_cords[0]
                        piece_y = piece_cords[1]
                        
                        if  (
                                # mouse x-pos is in the range of the piece
                                ((piece_x - TILESIZE // 2) < e.pos[0] < (piece_x + TILESIZE // 2))
                            ) and (
                                # mouse y-pos is in the range of the piece
                                (piece_y - TILESIZE // 2 < e.pos[1] < (piece_y + TILESIZE // 2))
                            ):
                            
                            print(f"Clicked on {name}")
                            break
                    else:
                        print("Clicked on nothing") 


            # region user events
             
            elif e.type == CLEAR_EVENTS:
                pg.event.clear()
            
            elif e.type == MOVE_EVENT:
                # Do move logic

                # Draw the board
                pg.event.post(pg.event.Event(UPDATE_BOARD))
            
            elif e.type == UPDATE_BOARD:
                draw_board(screen, board, game_board_positions) # Only draw the board when asked -> fps baby!!!!
                
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
        pg.display.update(
            [
                fps_counter_space, 
                line
            ]
        )
        clock.tick(fps_max)

    # endregion

    pg.quit()
    return 0



# region main

if __name__ == "__main__":
    # try:
    main()
    print("Program exited successfully\nexit code: 0")
    exit(0)

    # except Exception as e:
    #     print(f"An error occurred: {e}\nexit code: you choose lmao 1 ig?")
    #     exit(1)

# endregion

