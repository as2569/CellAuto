import pygame

blank = 0, 0, 0, 0
green = 0, 255, 0, 255
black = 0, 0, 0, 255
white = 255, 255, 255, 255
yellow = 0, 128, 0, 255
brown = 80, 41, 28, 255
red = 255, 0, 0, 255
orange = 255, 165, 0, 210
teal = 100, 100, 255, 255
blue = 0, 0, 255, 255
purple = 138, 43, 226, 210

class CellType(enumerate):
    EMPTY = 0
    SEA = 1
    PLAINS = 2
    COAST = 3
    HILL = 4
    MOUNTAIN = 5
    CIV1 = 6
    CIV2 = 7

class Cell:
    def __init__(self, x, y, size):
        self.state = 0
        self.posX = x * size
        self.posY = y * size
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        #self.image = pygame.image.load('square.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * size, y * size)
        return

    def get_state(self):
        return self.state

    def set_state(self, cell_type):
        self.state = cell_type

    def update(self):
        if self.state == 0:
            self.image.fill(blank)
        elif self.state == 1:
            self.image.fill(blue)
        elif self.state == 2:
            self.image.fill(green)
        elif self.state == 3:
            self.image.fill(teal)
        elif self.state == 4:
            self.image.fill(brown)
        elif self.state == 5:
            self.image.fill(white)
        elif self.state == 6:
            self.image.fill(orange)
        elif self.state == 7:
            self.image.fill(purple)
        else:
            print("invalid cell")
            self.image.fill(blank)
