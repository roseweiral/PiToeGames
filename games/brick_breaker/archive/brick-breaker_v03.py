import pygame
import sys
import random

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
GRAY = (100, 100, 100)

# Font
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Global Settings
ball_speed_multiplier = 1  # Default speed multiplier


def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def main_menu():
    """Main menu loop."""
    while True:
        screen.fill(BLACK)
        draw_text("Brick Breaker", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)
        draw_text("1 - Simple Rainbow", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 30)
        draw_text("S - Settings", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 30)

        pygame.display.flip()

        # Event handling for menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return  # Start the game
        if keys[pygame.K_s]:
            settings_menu()


def settings_menu():
    """Settings menu loop for adjusting ball speed."""
    global ball_speed_multiplier
    while True:
        screen.fill(BLACK)
        draw_text("Settings", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)
        draw_text(f"Ball Speed: {ball_speed_multiplier}", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 30)
        draw_text("Use UP and DOWN to adjust", small_font, GRAY, screen, WIDTH // 2, HEIGHT // 2 + 30)
        draw_text("Press ESC to return to the main menu", small_font, GRAY, screen, WIDTH // 2, HEIGHT // 2 + 80)

        pygame.display.flip()

        # Event handling for settings
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and ball_speed_multiplier < 9:
            ball_speed_multiplier += 1
            pygame.time.wait(100)  # Add delay for smoother input
        if keys[pygame.K_DOWN] and ball_speed_multiplier > 1:
            ball_speed_multiplier -= 1
            pygame.time.wait(100)
        if keys[pygame.K_ESCAPE]:
            return  # Return to main menu


def game():
    """Main game loop."""
    global ball_speed_multiplier

    # Paddle settings
    PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
    paddle_speed = 7
    paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Ball settings
    BALL_SIZE = 15
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    ball_speed_x, ball_speed_y = random.choice([-2, 2]) * ball_speed_multiplier, -0.75 * ball_speed_multiplier

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

    # Score and lives
    score = 0
    lives = 3

    # Game loop
    clock = pygame.time.Clock()
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
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
            ball_speed_x = -ball_speed_x
        if ball.top <= 0:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_speed_y = -ball_speed_y

        # Ball collision with bricks
        for brick in bricks[:]:
            brick_rect, brick_color = brick
            if ball.colliderect(brick_rect):
                ball_speed_y = -ball_speed_y
                bricks.remove(brick)
                score += 10

        # Ball out of bounds
        if ball.bottom >= HEIGHT:
            lives -= 1
            ball.x, ball.y = WIDTH // 2, HEIGHT // 2
            ball_speed_x, ball_speed_y = random.choice([-4, 4]) * ball_speed_multiplier, -4 * ball_speed_multiplier
            if lives == 0:
                return  # End game

        # Drawing the game
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        for brick_rect, brick_color in bricks:
            pygame.draw.rect(screen, brick_color, brick_rect)

        # Draw score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))

        # Check win condition
        if not bricks:
            return  # End game

        # Update the display
        pygame.display.flip()
        clock.tick(60)


# Run the game
while True:
    main_menu()
    game()
