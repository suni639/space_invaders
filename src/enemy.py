import pygame

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/enemy.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.x = x
        self.y = y
        self.x_change = 0.5
        self.y_change = 20
        self.active = True

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0 or self.x >= 770:
            self.x_change *= -1
            self.y += self.y_change

    def reset(self, index):
        self.x = (index % 10) * 70 + 50
        self.y = (index // 10) * 70 + 50
