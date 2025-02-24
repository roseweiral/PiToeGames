import pygame
import sys
import random
from time import sleep

#from ...modules.event_logging import handle_fsr_data
from modules.event_logging import handle_fsr_data
from hardware.archive.fsr_initial_ads115 import get_fsr_values, read_adc, FSR_CHANNEL_LEFT, FSR_CHANNEL_RIGHT, FSR_THRESHOLD
from modules.bb_media import Media, play_background_music, stop_background_music



#==============================================================================#
# Global Variables  
#==============================================================================#

ball = None
ball_speed_x = None
ball_speed_y = None
bricks = None
paddle = None
score = None
lives = None
dynamic_bat = None

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
    rows = 7  # Number of rows for the rainbow effect
    cols = 5  # Number of bricks per row

    # Bricks - Create bricks in a grid with a rainbow color scheme
    bricks = [
        (pygame.Rect(100 * col, 50 + 30 * row, 80, 20), color[(row) % len(color)])
        for row in range(rows) for col in range(cols)
    ]

    # Score and lives
    global score, lives
    score = 0
    lives = 10

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
# Main Brickbreaker Menu
#==============================================================================#

def brick_breaker_menu():
    while True:
        pygame.display.flip()
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
                    ball_speed_y = -4    # Ensure ball moves upwards
                    return  # Exit the main menu to start the game
                if event.key == pygame.K_s:
                    settings_menu()
                if event.key == pygame.K_ESCAPE:
                    from games.menu import main_menu
                    main_menu()
                    return

#==============================================================================#
# Ball and Paddle Logic
#==============================================================================#

def handle_ball_paddle_collision():
    global ball_speed_x, ball_speed_y
    if ball.colliderect(paddle):
        Media.paddle_hit_sound.play()  # Play paddle hit sound
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

def enforce_minimum_speed():
    global ball_speed_x, ball_speed_y

    # Ensure the ball always has a non-zero vertical speed
    if ball_speed_y == 0:
        ball_speed_y = random.choice([-4, 4])  # Randomize vertical speed if it's zero

    # Ensure the vertical speed is always non-zero (to avoid horizontal-only movement)
    if abs(ball_speed_y) < 1:
        ball_speed_y = random.choice([-4, 4])

    # Ensure that horizontal speed also has a meaningful value
    if abs(ball_speed_x) < 1:
        ball_speed_x = random.choice([-4, 4])

#==============================================================================#
# Ball Reset
#==============================================================================#

# Ball reset function
def reset_ball():
    global ball_speed_x, ball_speed_y, ball
    # Reset ball to the middle of the paddle
    ball.x = paddle.x + paddle.width // 2 - ball.width // 2
    ball.y = paddle.y - ball.height  # Position it just above the paddle

    # Randomize ball speed at a 45-degree angle
    ball_speed_x = random.choice([-2, 2])
    ball_speed_y = -2  # Always upwards
    print(f"Ball reset: speed X={ball_speed_x}, Y={ball_speed_y}")

#==============================================================================#
# Main Game Loop
#==============================================================================#

# Check for /nolog parameter
nolog = '/nolog' in sys.argv

clock = pygame.time.Clock()
ball_speed_multiplier = 1

def start_brick_breaker():
    
    bb_game_setup()
    brick_breaker_menu()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            #    pygame.quit()
            #    sys.exit()
                print("Escape pressed. Returning to menu...")
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Escape key pressed, break to menu
                    stop_background_music()
                    print("Escape pressed. Returning to menu...")
                    start_brick_breaker()

        # Read FSR values
        fsr_value_left = read_adc(FSR_CHANNEL_LEFT)
        fsr_value_right = read_adc(FSR_CHANNEL_RIGHT)

        # Logging FSR events
        # if fsr_value_left <> FSR_THRESHOLD:
        handle_fsr_data(fsr_id="left", values=fsr_value_left)

        #if fsr_value_right <> FSR_THRESHOLD:
        handle_fsr_data(fsr_id="right", values=fsr_value_right)
        
        # Event handling for keyboard
        keys = pygame.key.get_pressed()  # Get the state of all keys
        if keys[pygame.K_LEFT] and paddle.left > 0:  # Left arrow key
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:  # Right arrow key
            paddle.x += PADDLE_SPEED

        # Movement control for fsr player (paddle control with FSRs)
        if fsr_value_left > FSR_THRESHOLD and paddle.left > 0:
            paddle.x -= PADDLE_SPEED
        if fsr_value_right > FSR_THRESHOLD and paddle.right < WIDTH:
            paddle.x += PADDLE_SPEED

        # Ball movement
        global ball_speed_x, ball_speed_y
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Enforce non-zero vertical speed
        enforce_minimum_speed()

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            Media.wall_hit_sound.play()  # Play wall hit sound
            ball_speed_x = -ball_speed_x
        if ball.top <= 0:
            Media.wall_hit_sound.play()
            ball_speed_y = -ball_speed_y

        # Ball collision with paddle
        handle_ball_paddle_collision()

        # Ball collision with bricks
        global score
        for brick, brick_color in bricks:
            if ball.colliderect(brick):
                Media.brick_hit_sound.play()  # Play brick hit sound
                ball_speed_y = -ball_speed_y
                bricks.remove((brick, brick_color))  # Remove the brick from the list
                score += 10

        # Ball out of bounds
        global lives
        if ball.bottom >= HEIGHT:
            Media.life_lost_sound.play()  # Play life lost sound
            lives -= 1
            if lives == 0:
                stop_background_music
                Media.game_over_sound.play()  # Play game over sound
                start_brick_breaker()  # Quit game and Return to the main menu
            else:
                reset_ball()  # Only reset if the game continues

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        # Draw bricks with their assigned colors
        for brick, brick_color in bricks:
            pygame.draw.rect(screen, brick_color, brick)

        # Start Background Music
        play_background_music()

        # Display score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

        # Display the number of bricks remaining at the top center
        bricks_remaining = len(bricks)
        text = font.render(f"Bricks Remaining: {bricks_remaining}", True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(WIDTH // 2, 30))  # Centered at the top
        screen.blit(text, text_rect)
        if bricks_remaining == 0:
            # All bricks have been destroyed
            stop_background_music()  # Stop the background music
            text = font.render("Congratulations! You won!", True, (255, 255, 255))  # White text
            Media.winner_sound.play()  # Play the winner sound
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            sleep(5)  # Wait for 5 seconds before returning to the main menu
            start_brick_breaker()

        pygame.display.flip()

        clock.tick(60)  # FPS = 60


# If the script is run directly (not imported), start the game
if __name__ == "__main__":
    start_brick_breaker()
