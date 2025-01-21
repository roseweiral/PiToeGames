import spidev
import pygame
import sys

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

# MCP3008 settings
FSR_CHANNEL_UP = 0  # FSR connected to CH0 for upward movement
FSR_CHANNEL_DOWN = 1  # FSR connected to CH1 for downward movement
fsr_threshold = 500  # Configurable threshold for FSR sensitivity

# Initialize positions
player1 = pygame.Rect(50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

# Scores
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)

# Set up SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    """Read data from the specified ADC channel."""
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def reset_ball():
    """Reset the ball to the center and reverse the X direction."""
    ball.x, ball.y = WIDTH // 2, HEIGHT // 2
    return -ball_speed_x, ball_speed_y  # reverse X direction for new round

# Game loop
clock = pygame.time.Clock()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Read FSR values
    fsr_value_up = read_adc(FSR_CHANNEL_UP)
    fsr_value_down = read_adc(FSR_CHANNEL_DOWN)

    # Logging FSR events
    if fsr_value_up > fsr_threshold:
        print(f"FSR UP event detected: Value = {fsr_value_up}")
    if fsr_value_down > fsr_threshold:
        print(f"FSR DOWN event detected: Value = {fsr_value_down}")

    # Movement control for player 1 (paddle control with FSRs)
    if fsr_value_up > fsr_threshold and player1.top > 0:
        player1.y -= paddle_speed
        print("Player 1 moves up (FSR UP detected)")
    if fsr_value_down > fsr_threshold and player1.bottom < HEIGHT:
        player1.y += paddle_speed
        print("Player 1 moves down (FSR DOWN detected)")

    # Movement control for player 2 (paddle control with arrow keys)
    keys = pygame.key.get_pressed()
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
