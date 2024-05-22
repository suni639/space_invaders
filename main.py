import pygame
import math

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Load and resize the background
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (30, 30))  # Resize player image
playerX = 370  # Initial horizontal position of the player
playerY = 500  # Initial vertical position of the player
playerX_change = 0  # Change in horizontal position of the player

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = 0.5  # Horizontal speed of enemy
enemyY_change = 5  # Vertical speed of enemy
num_of_enemies = 20  # number of enemy
enemies_active = [True] * num_of_enemies  # Track active status of each enemy

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyImg[i] = pygame.transform.scale(enemyImg[i], (30, 30))  # Resize enemy image
    x = (i % 10) * 70 + 50  # Position enemies in 10 columns
    y = (i // 10) * 70 + 50  # Position enemies in 2 rows
    enemyX.append(x)
    enemyY.append(y)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (10, 10))  # Resize bullet image
bulletX = 0  # Initial horizontal position of the bullet
bulletY = 500  # Initial vertical position of the bullet
bulletX_change = 0  # Change in horizontal position of the bullet
bulletY_change = 10  # Change in vertical position of the bullet
bullet_state = "ready"  # Bullet state - "ready" means you can't see the bullet on the screen

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # Font for score display
textX = 10  # Horizontal position of the score text
textY = 10  # Vertical position of the score text

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)  # Font for game over text
completion_font = pygame.font.Font('freesansbold.ttf', 64)  # Font for game completion text

# Game over flag
game_over = False  # Flag to check if the game is over
game_complete = False  # Flag to check if the game is complete

# Function to display the score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Function to display game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Function to display game completion text
def game_complete_text():
    complete_text = completion_font.render("YOU WIN!", True, (255, 255, 255))
    screen.blit(complete_text, (250, 250))

# Function to draw the player on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))

# Function to draw an enemy on the screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Function to fire the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # Change bullet state to "fire"
    screen.blit(bulletImg, (x + 10, y + 10))

# Function to check for collision between bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Function to reset the game state
def reset_game():
    global playerX, playerY, playerX_change, bulletX, bulletY, bullet_state, score_value, enemies_active, game_over, game_complete
    playerX = 370  # Reset player position
    playerY = 500  # Reset player position
    playerX_change = 0  # Reset player movement
    bulletX = 0  # Reset bullet position
    bulletY = 500  # Reset bullet position
    bullet_state = "ready"  # Reset bullet state
    score_value = 0  # Reset score
    enemies_active = [True] * num_of_enemies  # Reset all enemies to active
    game_over = False  # Reset game over flag
    game_complete = False  # Reset game complete flag
    for i in range(num_of_enemies):
        enemyX[i] = (i % 10) * 70 + 50  # Reset enemy horizontal position
        enemyY[i] = (i // 10) * 70 + 50  # Reset enemy vertical position

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
                playerX_change = -2  # Move player left with smaller step
            if event.key == pygame.K_RIGHT:
                playerX_change = 2  # Move player right with smaller step
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX  # Set bullet position to player position
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_r:
                if game_over or game_complete:
                    reset_game()  # Restart the game if "R" key is pressed and game is over or complete

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # Stop player movement when key is released

    if not game_over and not game_complete:
        # Update player position
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 770:
            playerX = 770

        # Move all enemies in unison
        move_down = False
        for i in range(num_of_enemies):
            if enemies_active[i]:
                enemyX[i] += enemyX_change
                if enemyX[i] <= 0 or enemyX[i] >= 770:
                    enemyX_change = -enemyX_change  # Change direction
                    move_down = True

        if move_down:
            for i in range(num_of_enemies):
                enemyY[i] += enemyY_change  # Move enemies down

        # Check for collision
        all_enemies_destroyed = True
        for i in range(num_of_enemies):
            if enemies_active[i]:
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    bulletY = 500  # Reset bullet position
                    bullet_state = "ready"  # Reset bullet state
                    score_value += 1  # Increase score
                    enemies_active[i] = False  # Mark enemy as destroyed
                if enemyY[i] > 475:
                    game_over = True
                if enemies_active[i]:
                    all_enemies_destroyed = False
                enemy(enemyX[i], enemyY[i], i)

        # Check if all enemies are destroyed
        if all_enemies_destroyed:
            game_complete = True

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 500
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)  # Draw player
        show_score(textX, textY)  # Show score
    elif game_over:
        game_over_text()  # Display game over text
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (250, 320))  # Display restart instruction
    elif game_complete:
        game_complete_text()  # Display game complete text
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (250, 320))  # Display restart instruction

    pygame.display.update()  # Update the display
