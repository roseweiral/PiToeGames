import pygame
import sys
import random
import spidev

#==============================================================================#
# Configuration and Constants
#==============================================================================#

WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_SPEED = 5

#==============================================================================#
# Media Assets
#==============================================================================#

# Dummy media module functions to simulate sound playing (replace with your actual sound file calls)
class media:
    @staticmethod
    def paddle_hit_sound():
        print("Paddle hit sound")

    @staticmethod
    def wall_hit_sound():
        print("Wall hit sound")

    @staticmethod
    def brick_hit_sound():
        print("Brick hit sound")

    @staticmethod
    def life_lost_sound():
        print("Life lost sound")

    @staticmethod
    def game_over_sound():
        print("Game over sound")

#==============================================================================#
# FSR Logic
#==============================================================================#

# Define the channels and threshold for FSR readings
FSR_CHANNEL_LEFT = 0  # FSR connected to CH0 for left movement
FSR_CHANNEL_RIGHT = 1  # FSR connected to CH1 for right movement
FSR_THRESHOLD = 100  # Sensitivity threshold for FSRs

# Set up SPI for MCP3008 (used for reading FSRs)
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

# Bricks (for simplicity, we're defining just a few bricks here)
bricks = [pygame.Rect(100 * i, 50, 80, 20) for i in range(5)]

# Score and lives
score = 0
lives = 3

# Dynamic bat toggle
dynamic_bat = False

#==============================================================================#
# Settings Menu
#==============================================================================#

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

#==============================================================================#
# Main Menu
#==============================================================================#

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

#==============================================================================#
# Ball and Paddle Logic
#==============================================================================#

def handle_ball_paddle_collision():
    global ball_speed_x, ball_speed_y
    if ball.colliderect(paddle):
        media.paddle_hit_sound()  # Play paddle hit sound
        if dynamic_bat:
            zone_width = PADDLE_WIDTH / 10
            impact_zone = int((ball.x - paddle.x) // zone_width) + 1

            if impact_zone == 1:
                ball_speed_x = -abs(ball_speed_x)
                ball_speed_y = -abs(ball_speed_y)
            elif 2 <= impact_zone <= 4 or 7 <= impact_zone <= 9:
                ball_speed_y = -abs(ball_speed_y)
            elif 5 <= impact_zone <= 6:
                ball_speed_x = 0
                ball_speed_y = -abs(ball_speed_y)
            elif impact_zone == 10:
                ball_speed_x = abs(ball_speed_x)
                ball_speed_y = -abs(ball_speed_y)
        else:
            ball_speed_y = -abs(ball_speed_y)

#==============================================================================#
# Main Game Loop
#==============================================================================#

clock = pygame.time.Clock()
ball_speed_multiplier = 1

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
    if fsr_value_left > FSR_THRESHOLD:
        print(f"FSR LEFT event detected: Value = {fsr_value_left}")
    if fsr_value_right > FSR_THRESHOLD:
        print(f"FSR RIGHT event detected: Value = {fsr_value_right}")

    # Movement control for fsr player (paddle control with FSRs)
    if fsr_value_left > FSR_THRESHOLD and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
        print("Paddle moves left (FSR LEFT detected)")
    if fsr_value_right > FSR_THRESHOLD and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED
        print("Paddle moves right (FSR RIGHT detected)")

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        media.wall_hit_sound()  # Play wall hit sound
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        media.wall_hit_sound()
        ball_speed_y = -ball_speed_y

    # Ball collision with paddle
    handle_ball_paddle_collision()

    # Ball collision with bricks
    for brick in bricks[:]:
        brick_rect = brick
        if ball.colliderect(brick_rect):
            media.brick_hit_sound()  # Play brick hit sound
            ball_speed_y = -ball_speed_y
            bricks.remove(brick)
            score += 10

    # Ball out of bounds
    if ball.bottom >= HEIGHT:
        media.life_lost_sound()  # Play life lost sound
        lives -= 1
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed_x, ball_speed_y = random.choice([-2, 2]) * ball_speed_multiplier, -0.5 * ball_speed_multiplier
        if lives == 0:
            media.game_over_sound()  # Play game over sound

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 150, 10))

    pygame.display.flip()

    clock.tick(60)  # Maintain 60 FPS
