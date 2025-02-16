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