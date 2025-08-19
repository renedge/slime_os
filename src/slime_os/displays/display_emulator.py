import pygame, sys


class Display:
    def __init__(self, sos):
        pygame.init()
        self.width = 400
        self.height = 240
        self.pens = []
        self.pen = None

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Slime OS")

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def get_bounds(self, *args, **kwargs):
        return (self.width, self.height)

    def update(self):
        pygame.display.flip()

    def line(self, x1, y1, x2, y2, thickness):
        pygame.draw.line(self.surface, self.pen, (x1, y1), (x2, y2), thickness)

    def text(self, text, x, y, scale, angle):
        # return self.display.line(*args, **kwargs)
        print(text, x, y)

    def pixel(self, x, y):
        pygame.draw.set_at(self.surface, (x, y), self.pen)

    def rectangle(self, x, y, w, h):
        pygame.draw.rect(self.surface, self.pen, pygame.Rect(x, y, w, h))

    def create_pen(self, r,g,b):
        self.pens.append((r,g,b))
        return len(self.pens) - 1

    def set_pen(self, pen_id):
        self.pen = self.pens[pen_id]
