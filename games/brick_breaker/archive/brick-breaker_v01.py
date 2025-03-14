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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle_speed = 7
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball settings
BALL_SIZE = 15
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x, ball_speed_y = random.choice([-4, 4]), -4

# Brick settings
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
bricks = []
for row in range(5):  # 5 rows of bricks
    for col in range(WIDTH // (BRICK_WIDTH + 10)):
        brick_x = col * (BRICK_WIDTH + 10) + 35
        brick_y = row * (BRICK_HEIGHT + 10) + 50
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Score and lives
score = 0
lives = 3
font = pygame.font.Font(None, 36)

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
        if ball.colliderect(brick):
            ball_speed_y = -ball_speed_y
            bricks.remove(brick)
            score += 10

    # Ball out of bounds
    if ball.bottom >= HEIGHT:
        lives -= 1
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed_x, ball_speed_y = random.choice([-4, 4]), -4
        if lives == 0:
            print("Game Over!")
            pygame.quit()
            sys.exit()

    # Drawing the game
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))

    # Check win condition
    if not bricks:
        print("You Win!")
        pygame.quit()
        sys.exit()

    # Update the display
    pygame.display.flip()
    clock.tick(60)
