"""Main file"""

# imports
import numpy as np
import pygame as pg
from Utils.Scripts.fps_counter import FPSCounter # FPS counter
from Utils.Scripts.settings import DIMENSION, EMPTY, GRASS, TREE, TENT, fps_max, DEBUG # Game constants
from Utils.Scripts.funcs import CREATE_VALID_GAME, pretty_print # Game functions

# Main function
def main() -> int:
    """Main function."""
    # region pygame

    # Pygame setup
    pg.init()
    pg.display.set_caption("Tentje Boompje")

    Resolution = (pg.display.Info().current_w, pg.display.Info().current_h)

    # Set up the display (setting up with fullscreen being: 1280x720)
    screen_width = round(Resolution[0] * 0.5078125) # Screen width is 650 for 1280x720
    screen_height = round(Resolution[1] * (0.5 + 1/3)) # Screen height is 600 for 1280x720

    if DEBUG:
        print(f"Screen width: {Resolution[0]}, Screen height: {Resolution[1]}")
        print(f"Game width: {screen_width}, Game height: {screen_height}")

    top_margin = screen_height * 0.05 # Margin = 30 pixels if the game has 600 height

    screen: pg.Surface = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()

    # Fps counter
    fps_counter = FPSCounter(
        screen, pg.font.Font(None, 24), clock, (255, 255, 255), (40, 15)
    )
    
    # Vars
    running: bool = True
    

    # region classes
    class Board:
        def __init__(self):
            pass

    class Tent:
        def __init__(self, pos: tuple[int, int], dims: tuple[int, int]) -> None:
            """Tent class

            Args:
                pos (tuple[int, int]): The x, y position of the tent on the board.
                dims (tuple[int, int]): The dimensions of the tent picture.
            """

            self.image = pg.image.load(r"Utils\imgs\TENT.png") # Load the image
            self.image = pg.transform.scale(self.image, dims) # Scale the image
            self.rect = self.image.get_rect(center=pos) # Get the rect of the image
        
        def draw(self, screen: pg.Surface) -> None:
            screen.blit(self.image, self.rect)


    class Tree:
        def __init__(self, pos: tuple[int, int], dims: tuple[int, int]) -> None:
            self.image = pg.image.load(r"Utils\imgs\TREE.png")
            self.image = pg.transform.scale(self.image, dims)
            self.rect = self.image.get_rect(center=pos)
        
        def draw(self, screen: pg.Surface) -> None:
            screen.blit(self.image, self.rect)

    class Grass:
        def __init__(self, pos: tuple[int, int], dims: tuple[int, int]) -> None:
            self.image = pg.image.load(r"Utils\imgs\GRASS.png")
            self.image = pg.transform.scale(self.image, dims)
            self.rect = self.image.get_rect(center=pos)
        
        def draw(self, screen: pg.Surface) -> None:
            screen.blit(self.image, self.rect)
    # endregion

    # region Events
    # Clear events event
    CLEAR_EVENTS = pg.USEREVENT + 1
    # Clear every 10 seconds 
    pg.time.set_timer(CLEAR_EVENTS, 10000)



    # endregion

    # endregion

    # region main
    
    # Create the game board
    board = CREATE_VALID_GAME()
    
    # Pretty print the board
    pretty_print(board)

    # Main loop
    while running:
        screen.fill((0, 0, 0))
        pg.draw.line(screen, (200,200,200), (0, top_margin), (screen_width, top_margin), 2)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            elif e.type == CLEAR_EVENTS:
                pg.event.clear()
                print("Cleared events")

        # Update everything
        fps_counter.update()


        # Draw everything
        for y in range(DIMENSION):
            for x in range(DIMENSION):
                if board[y][x] == Tree:
                    ...
                elif board[y][x] == Tent:
                    ...

        fps_counter.draw()

        pg.display.flip()
        clock.tick(fps_max)
    # endregion
    
    pg.quit()
    return 0

if __name__ == "__main__":
    exit_code = main()

    if exit_code != 0:
        print(f"""An error occurred.
exit code: {exit_code}
""")

    else:
        print(f"""Program exited successfully.
exit code {exit_code}
""")

