import RPi.GPIO as GPIO
import spidev  # Library for SPI communication with MCP3008
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
FSR_CHANNEL = 0  # MCP3008 channel for FSR
fsr_threshold = 500  # Configurable threshold for FSR sensitivity (0-1023)

# Initialize SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 1350000

# Initialize positions
player1 = pygame.Rect(50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

# Scores
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)

# Game loop
clock = pygame.time.Clock()

def reset_ball():
    """Reset the ball to the center and reverse the X direction"""
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2
    return -ball_speed_x, ball_speed_y  # reverse X direction for new round

def read_mcp3008(channel):
    """Read analog value from MCP3008"""
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spi.close()
            pygame.quit()
            sys.exit()

    # Read FSR value
    fsr_value = read_mcp3008(FSR_CHANNEL)

    # Logging FSR event
    if fsr_value > fsr_threshold:
        print(f"FSR event detected: Value {fsr_value} exceeded threshold {fsr_threshold}")

    # Movement control for player 1 (paddle control with W & S keys and FSR)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= paddle_speed
        print("Player 1 moves up (W key pressed)")
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += paddle_speed
        print("Player 1 moves down (S key pressed)")

    # If FSR is pressed (threshold-based, simulate paddle movement)
    if fsr_value > fsr_threshold:
        if player1.top > 0:  # Move paddle up if not at the top
            player1.y -= paddle_speed
            print("Player 1 moves up (FSR event detected)")

    # Movement control for player 2 (paddle control with arrow keys)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= paddle_speed
        print("Player 2 moves up (Up arrow key pressed)")
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += paddle_speed
        print("Player 2 moves down (Down arrow key pressed)")

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
        print("Player 2 scores!")
    if ball.right >= WIDTH:  # Player 1 scores
        player1_score += 1
        ball_speed_x, ball_speed_y = reset_ball()  # reset ball
        pygame.time.delay(500)  # Short delay before next round
        print("Player 1 scores!")

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
