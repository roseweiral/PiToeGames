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

