class FPSCounter:
    """fps counter class"""

    def __init__(self, surface, font, clock, color, pos):
        self.surface = surface
        self.font = font
        self.clock = clock
        self.pos = pos
        self.color = color

        self.fps_text = self.font.render(
            str(int(self.clock.get_fps())) + "FPS", False, self.color
        )
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

    def draw(self):
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        text = f"FPS: {self.clock.get_fps():2.0f}"
        self.fps_text = self.font.render(text, False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))
