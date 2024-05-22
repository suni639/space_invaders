import pygame

class Player:
    def __init__(self):
        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.x = 370
        self.y = 500
        self.x_change = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 770:
            self.x = 770
