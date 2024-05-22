import pygame
from player import Player
from enemy import Enemy
from bullet import Bullet
import math

# Initialize the pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 2
BULLET_SPEED = 10
ENEMY_SPEED = 0.5
ENEMY_DROP = 20
NUM_ENEMIES = 20

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and resize the background
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('assets/spaceship.png')
pygame.display.set_icon(icon)

# Initialize game objects
player = Player()
bullet = Bullet()
enemies = [Enemy((i % 10) * 70 + 50, (i // 10) * 70 + 50) for i in range(NUM_ENEMIES)]

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
completion_font = pygame.font.Font('freesansbold.ttf', 64)
game_over = False
game_complete = False

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def game_complete_text():
    complete_text = completion_font.render("YOU WIN!", True, (255, 255, 255))
    screen.blit(complete_text, (250, 250))

def reset_game():
    global score_value, game_over, game_complete
    player.x = 370
    player.y = 500
    bullet.y = 500
    bullet.state = "ready"
    score_value = 0
    game_over = False
    game_complete = False
    for i, enemy in enumerate(enemies):
        enemy.x = (i % 10) * 70 + 50
        enemy.y = (i // 10) * 70 + 50
        enemy.active = True

def is_collision(enemy, bullet):
    distance = math.sqrt(math.pow(enemy.x - bullet.x, 2) + math.pow(enemy.y - bullet.y, 2))
    return distance < 27

# Game Loop
running = True
while running:

    # Fill screen with black color (RGB)
    screen.fill((0, 0, 0))
    # Draw background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the game loop

        # If keystroke is pressed, check whether it is right, left, or space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -PLAYER_SPEED  # Move player left
            if event.key == pygame.K_RIGHT:
                player.x_change = PLAYER_SPEED  # Move player right
            if event.key == pygame.K_SPACE:
                if bullet.state == "ready":
                    bullet.fire(player.x)
            if event.key == pygame.K_r and (game_over or game_complete):
                reset_game()  # Restart the game if "R" key is pressed and game is over or complete

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0  # Stop player movement when key is released

    if not game_over and not game_complete:
        player.move()
        bullet.move()
        for enemy in enemies:
            enemy.move()
            if enemy.active:
                if is_collision(enemy, bullet):
                    bullet.y = 500
                    bullet.state = "ready"
                    score_value += 1
                    enemy.active = False
                if enemy.y > 475:
                    game_over = True
                enemy.draw()

        bullet.draw()
        player.draw()
        show_score(textX, textY)

        if all(not enemy.active for enemy in enemies):
            game_complete = True

    elif game_over:
        game_over_text()  # Display game over text
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (250, 320))  # Display restart instruction
    elif game_complete:
        game_complete_text()  # Display game complete text
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (250, 320))  # Display restart instruction

    pygame.display.update()  # Update the display
