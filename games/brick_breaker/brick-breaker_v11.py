# main.py
import pygame
import sys
import random
import os

from event_logging import handle_fsr_data


# Add the path to the hardware folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hardware')))
# Import the FSR logic module
from hardware import fsr

#==============================================================================#
# Game Configuration and Constants
#==============================================================================#

WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_SPEED = 5

# Initialize the pygame mixer
pygame.mixer.init()

class media:
    paddle_hit_sound = pygame.mixer.Sound("sounds/ding.wav")
    wall_hit_sound = pygame.mixer.Sound("sounds/ding.wav")
    brick_hit_sound = pygame.mixer.Sound("sounds/ding.wav")
    life_lost_sound = pygame.mixer.Sound("sounds/chord.wav")
    game_over_sound = pygame.mixer.Sound("sounds/tada.wav")

#==============================================================================#
# Game Setup
#==============================================================================#

# Initialize Pygame
pygame.init()

# Create screen, clock, and fonts
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Brick Breaker')
font = pygame.font.Font(None, 36)

# Create the paddle and ball
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Initialize ball speed variables
ball_speed_x = random.choice([-4, 4])
ball_speed_y = -4

#==============================================================================#
# Main Game Loop
#==============================================================================#

# Check for /nolog parameter
nolog = '/nolog' in sys.argv

clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Escape key pressed, break to menu
                print("Escape pressed. Returning to menu...")
                main_menu()

    # Read FSR values using the fsr module
    fsr_value_left, fsr_value_right = fsr.get_fsr_values()

    # Logging FSR events
    print(f"FSR LEFT event detected: Value = {fsr_value_left}")
    handle_fsr_data(fsr_id="left", values=fsr_value_left)
    print(f"FSR RIGHT event detected: Value = {fsr_value_right}")
    handle_fsr_data(fsr_id="right", values=fsr_value_right)

    # Event handling for keyboard
    keys = pygame.key.get_pressed()  # Get the state of all keys
    if keys[pygame.K_LEFT] and paddle.left > 0:  # Left arrow key
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:  # Right arrow key
        paddle.x += PADDLE_SPEED

    # Movement control for fsr player (paddle control with FSRs)
    if fsr_value_left > fsr.FSR_THRESHOLD and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if fsr_value_right > fsr.FSR_THRESHOLD and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Handle collisions, drawing, and game logic...

    pygame.display.flip()
    clock.tick(60)  # FPS = 60
