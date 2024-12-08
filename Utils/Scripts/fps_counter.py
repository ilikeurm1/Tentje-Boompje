import pygame as pg

class FPSCounter:
    """fps counter class"""

    def __init__(self, surface: pg.Surface, font: pg.font.Font, clock: pg.time.Clock, color: tuple[int, int, int], pos: tuple[int, int, int, int]):
        self.surface = surface
        self.font = font
        self.clock = clock
        self.color = color
        self.pos = pos

        self.fps_text = self.font.render(
            str(int(self.clock.get_fps())) + "FPS", False, self.color
        )
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0] + (self.pos[2] // 2), self.pos[1] + (self.pos[3] // 2)))

    def draw(self):
        # Draw the counter
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        text = f"FPS: {self.clock.get_fps():2.0f}"
        self.fps_text = self.font.render(text, True, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0] + (self.pos[2] // 2), self.pos[1] + (self.pos[3] // 2)))
