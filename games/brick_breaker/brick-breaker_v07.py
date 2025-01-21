import pygame
import sys
import random
import spidev


# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
COLORS = [
    (255, 0, 0),    # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 127, 255),  # Cyan
    (0, 0, 255),    # Blue
    (139, 0, 255)   # Violet
]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle_speed = 7
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball settings
BALL_SIZE = 15
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
ball_speed_multiplier = 1
ball_speed_x, ball_speed_y = random.choice([-2, 2]) * ball_speed_multiplier, -0.5 * ball_speed_multiplier

# Brick settings
BRICK_WIDTH, BRICK_HEIGHT = 50, 20
rows = 7
columns = WIDTH // (BRICK_WIDTH + 5)
bricks = []
for row in range(rows):
    for col in range(columns):
        brick_x = col * (BRICK_WIDTH + 5) + 20
        brick_y = row * (BRICK_HEIGHT + 5) + 50
        bricks.append((pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT), COLORS[row]))

# MCP3008 settings
FSR_CHANNEL_LEFT = 0  # FSR connected to CH0 for upward movement
FSR_CHANNEL_RIGHT = 1  # FSR connected to CH1 for downward movement
fsr_threshold = 100  # Configurable threshold for FSR sensitivity


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

# Score and lives
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Sounds
paddle_hit_sound = pygame.mixer.Sound("sounds/ding.wav")
brick_hit_sound = pygame.mixer.Sound("sounds/ding.wav")
wall_hit_sound = pygame.mixer.Sound("sounds/ding.wav")
life_lost_sound = pygame.mixer.Sound("sounds/tada.wav")
game_over_sound = pygame.mixer.Sound("sounds/tada.wav")
win_sound = pygame.mixer.Sound("sounds/chord.wav")

# Dynamic bat toggle
dynamic_bat = False

# Settings menu
def settings_menu():
    global ball_speed_multiplier, dynamic_bat
    while True:
        screen.fill(BLACK)
        title_text = font.render("Settings", True, WHITE)
        speed_text = font.render(f"Ball Speed (1-9): {ball_speed_multiplier}", True, WHITE)
        dynamic_bat_text = font.render(f"Dynamic Bat (B): {'On' if dynamic_bat else 'Off'}", True, WHITE)
        exit_text = font.render("Press ESC to return to the main menu", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, 150))
        screen.blit(dynamic_bat_text, (WIDTH // 2 - dynamic_bat_text.get_width() // 2, 250))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_UP:
                    ball_speed_multiplier = min(9, ball_speed_multiplier + 1)
                if event.key == pygame.K_DOWN:
                    ball_speed_multiplier = max(1, ball_speed_multiplier - 1)
                if event.key == pygame.K_b:
                    dynamic_bat = not dynamic_bat

# Handle ball and paddle collision
def handle_ball_paddle_collision():
    global ball_speed_x, ball_speed_y
    if ball.colliderect(paddle):
        paddle_hit_sound.play()  # Play paddle hit sound
        if dynamic_bat:
            zone_width = PADDLE_WIDTH / 10
            impact_zone = int((ball.x - paddle.x) // zone_width) + 1

            if impact_zone == 1:
                ball_speed_x = -abs(ball_speed_multiplier)
                ball_speed_y = -abs(ball_speed_multiplier)
            elif 2 <= impact_zone <= 4 or 7 <= impact_zone <= 9:
                ball_speed_y = -abs(ball_speed_multiplier)
            elif 5 <= impact_zone <= 6:
                ball_speed_x = 0
                ball_speed_y = -abs(ball_speed_multiplier)
            elif impact_zone == 10:
                ball_speed_x = abs(ball_speed_multiplier)
                ball_speed_y = -abs(ball_speed_multiplier)
        else:
            ball_speed_y = -abs(ball_speed_y)

# Main menu
def main_menu():
    while True:
        screen.fill(BLACK)
        title_text = font.render("Brick Breaker", True, WHITE)
        start_text = font.render("Press 1 to Start Game", True, WHITE)
        settings_text = font.render("Press S for Settings", True, WHITE)
        exit_text = font.render("Press ESC to Quit", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 150))
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, 250))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Initialize ball speed and position
                    global ball_speed_x, ball_speed_y, ball
                    ball.x, ball.y = WIDTH // 2, HEIGHT // 2  # Reset ball position
                    ball_speed_x = random.choice([-4, 4])     # Randomize x direction
                    ball_speed_y = random.choice([-4, -3])    # Ensure ball moves upward
                    return  # Exit the main menu to start the game
                if event.key == pygame.K_s:
                    settings_menu()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Game loop
clock = pygame.time.Clock()

main_menu()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Read FSR values
    fsr_value_left = read_adc(FSR_CHANNEL_LEFT)
    fsr_value_right = read_adc(FSR_CHANNEL_RIGHT)

    # Logging FSR events
    if fsr_value_left > fsr_threshold:
        print(f"FSR LEFT event detected: Value = {fsr_value_left}")
    if fsr_value_right > fsr_threshold:
        print(f"FSR RIGHT event detected: Value = {fsr_value_right}")

    # Movement control for fsr player (paddle control with FSRs)
    if fsr_value_left > fsr_threshold and paddle.top > 0:
        paddle.y -= paddle_speed
        print("Paddle moves up (FSR LEFT detected)")
    if fsr_value_right > fsr_threshold and paddle.bottom < HEIGHT:
        paddle.y += paddle_speed
        print("Paddle moves down (FSR RIGHT detected)")

    # Paddle movement (keyboard control, can be removed if only FSR is used)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        wall_hit_sound.play()  # Play wall hit sound
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        wall_hit_sound.play()
        ball_speed_y = -ball_speed_y

    # Ball collision with paddle
    handle_ball_paddle_collision()

    # Ball collision with bricks
    for brick in bricks[:]:
        brick_rect, brick_color = brick
        if ball.colliderect(brick_rect):
            brick_hit_sound.play()  # Play brick hit sound
            ball_speed_y = -ball_speed_y
            bricks.remove(brick)
            score += 10

    # Ball out of bounds
    if ball.bottom >= HEIGHT:
        life_lost_sound.play()  # Play life lost sound
        lives -= 1
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed_x, ball_speed_y = random.choice([-2, 2]) * ball_speed_multiplier, -0.5 * ball_speed_multiplier
        if lives == 0:
            game_over_sound.play()  # Play game over sound
