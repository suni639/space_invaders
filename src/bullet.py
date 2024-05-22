import pygame

class Bullet:
    def __init__(self):
        self.image = pygame.image.load('assets/bullet_alt.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.x = 0
        self.y = 500
        self.y_change = 10
        self.state = "ready"

    def draw(self, screen):
        if self.state == "fire":
            screen.blit(self.image, (self.x + 10, self.y + 10))

    def fire(self, x):
        self.x = x
        self.state = "fire"

    def move(self):
        if self.state == "fire":
            self.y -= self.y_change
            if self.y <= 0:
                self.state = "ready"
                self.y = 500
