import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tennis Game with Sounds")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
paddle_speed = 5

# Ball settings
BALL_SIZE = 20
ball_speed_x, ball_speed_y = 4, 4

# Initialize positions
player1 = pygame.Rect(50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

# Scores
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)

# Load sounds
player1_beep = pygame.mixer.Sound("chord.wav")
player2_beep = pygame.mixer.Sound("ding.wav")
win_fanfare = pygame.mixer.Sound("tada.wav")

# Game loop
clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= paddle_speed
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += paddle_speed
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= paddle_speed
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += paddle_speed

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddles
    if ball.colliderect(player1):
        ball_speed_x = -ball_speed_x
        player1_beep.play()  # Play Player 1's beep
    if ball.colliderect(player2):
        ball_speed_x = -ball_speed_x
        player2_beep.play()  # Play Player 2's beep

    # Ball out of bounds
    if ball.left <= 0:
        player2_score += 1
