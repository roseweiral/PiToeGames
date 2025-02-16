import pygame
import random


#==============================================================================#
# Game Setup
#==============================================================================#

def bb_game_setup():
    # Initialize Pygame
    pygame.init()

    # Create screen, clock, and fonts
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Brick Breaker')
    font = pygame.font.Font(None, 36)

    # Create the paddle and ball
    global ball, paddle, bricks, dynamic_bat, ball_speed_multiplier, ball_speed_x, ball_speed_y
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    # Initialize ball speed variables
    ball_speed_x = random.choice([-4, 4])
    ball_speed_y = -4

    # Define the number of columns and rows for the bricks
    rows = 1  # Number of rows for the rainbow effect
    cols = 2  # Number of bricks per row

    # Bricks - Create bricks in a grid with a rainbow color scheme
    bricks = [
        (pygame.Rect(100 * col, 50 + 30 * row, 80, 20), color[(row) % len(color)])
        for row in range(rows) for col in range(cols)
    ]

    # Score and lives
    global score, lives
    score = 0
    lives = 3

    # Dynamic bat toggle
    dynamic_bat = False

    # Initialize ball speed multiplier
    ball_speed_multiplier = 1


#==============================================================================#
# Configuration and Constants
#==============================================================================#
color = [
    (255, 0, 0),    # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (238, 130, 238) # Violet
]

WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_SPEED = 5

# Create screen, clock, and fonts
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Brick Breaker')

pygame.font.init()
font = pygame.font.Font(None, 36)