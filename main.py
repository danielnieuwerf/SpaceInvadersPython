import pygame
import random
from pygame import mixer

# initialise pygame
pygame.init()

# set screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('rocket.jpg')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

# Background music
mixer.music.load('backgroundmusic.mp3')
mixer.music.play(-1)
# Player
playerImage = pygame.image.load('spaceship.jpg')
playerX = 370
playerY = 480
playerXdelta = 0

def player(x, y):
    screen.blit(playerImage, (x, y))

# Enemy
enemyImage = pygame.image.load('enemy.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyXdelta = 3

def enemy(x, y):
    screen.blit(enemyImage, (x, y))

# Bullet
bulletImage = pygame.image.load('bullet.png')
bulletX = 370
bulletY = 480
bulletXdelta = 0
bulletYdelta = 10
bulletState = "Ready"

def bullet(x, y):
    global bulletState
    bulletState = "Fired"
    screen.blit(bulletImage, (x+16, y+10))

# Collision detection
def isCollision(bulletX, bulletY, enemyX, enemyY):
    distanceSquared= pow(bulletX - enemyX, 2) + pow(bulletY - enemyY, 2)
    if distanceSquared < 700:
        return True
    else:
        return False

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
def showScore(x, y):
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))

# Game Over
overfont = pygame.font.Font('freesansbold.ttf', 64)
def gameoverPrint():
    text2 = overfont.render("GAMEOVER!", True, (255, 255, 255))
    screen.blit(text2, (200, 250))

# Game loop
running = True

while running:
    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXdelta = -6
            if event.key == pygame.K_RIGHT:
                playerXdelta = 6
            if event.key == pygame.K_SPACE:
                if bulletState == "Ready":
                    bulletX = playerX
                    bullet(bulletX, bulletY)
                    bulletXdelta = playerXdelta
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXdelta = 0

    # Update player position
    playerX += playerXdelta
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # Update enemy position
    enemyX += enemyXdelta
    if enemyX < 0:
        enemyX = 0
        enemyY += 50
        enemyXdelta = 3
    elif enemyX > 736:
        enemyX = 736
        enemyY += 50
        enemyXdelta = -3

    # Update bullet position amd state
    if bulletY < 0:
        bulletState = "Ready"
        bulletY = 480
    elif bulletX < 0 or bulletX > 800:
        bulletState = "Ready"
        bulletY = 480

    if bulletState == "Fired":
        bulletY -= bulletYdelta
        bulletX += bulletXdelta

    # Check for collisions
    if isCollision(bulletX, bulletY, enemyX, enemyY):
        bulletState = "Ready"
        bulletY = 480
        score += 1
        enemyY = random.randint(50, 150)

    # Display images
    showScore(10, 10)
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    if bulletState == "Fired":
        bullet(bulletX, bulletY)
    pygame.display.update()

    # Check for gameover
    if enemyY > 440:
        gameoverPrint()
        enemyY = 666
        pygame.display.update()
