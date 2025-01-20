import RPi.GPIO as GPIO
import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tennis Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
paddle_speed = 5

# Ball settings
BALL_SIZE = 20
ball_speed_x, ball_speed_y = 4, 4

# FSR settings
FSR_PIN = 4  # GPIO Pin for FSR
fsr_threshold = 500  # Adjust this value to your FSR's sensitivity

# Initialize positions
player1 = pygame.Rect(50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

# Scores
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)

# Set up GPIO for FSR input
GPIO.setmode(GPIO.BCM)
GPIO.setup(FSR_PIN, GPIO.IN)

# Game loop
clock = pygame.time.Clock()

def reset_ball():
    """Reset the ball to the center and reverse the X direction"""
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2
    return -ball_speed_x, ball_speed_y  # reverse X direction for new round

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Read FSR value (you will need to change this if you are using an analog-to-digital converter)
    fsr_value = GPIO.input(FSR_PIN)

    # If FSR is pressed (threshold-based, simulate pressing the "up arrow" key)
    if fsr_value > fsr_threshold:  # Adjust threshold based on your sensor's response
        if player1.top > 0:  # Move paddle up if not at the top
            player1.y -= paddle_speed

    # Movement control for player 2 (paddle control with arrow keys)
    keys = pygame.key.get_pressed()
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
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x = -ball_speed_x

    # Ball out of bounds (scoring)
    if ball.left <= 0:  # Player 2 scores
        player2_score += 1
        ball_speed_x, ball_speed_y = reset_ball()  # reset ball
        pygame.time.delay(500)  # Short delay before next round
    if ball.right >= WIDTH:  # Player 1 scores
        player1_score += 1
        ball_speed_x, ball_speed_y = reset_ball()  # reset ball
        pygame.time.delay(500)  # Short delay before next round

    # Drawing the game
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw scores
    player1_text = font.render(str(player1_score), True, WHITE)
    player2_text = font.render(str(player2_score), True, WHITE)
    screen.blit(player1_text, (WIDTH // 4, 20))
    screen.blit(player2_text, (WIDTH * 3 // 4, 20))

    # Update the display
    pygame.display.flip()
    clock.tick(60)
