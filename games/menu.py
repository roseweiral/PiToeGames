import pygame
import sys
from games.brick_breaker.brick_breaker import start_brick_breaker  # Import the correct function

#==============================================================================#
# Game Setup
#==============================================================================#

# Initialize Pygame
print("Main Menu")
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 600

# Create screen, clock, and fonts
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Toe Games')
font = pygame.font.Font(None, 36)


def main_menu():
    while True:
        screen.fill(BLACK)
        title_text = font.render("Toe Pong Games", True, WHITE)
        start_text = font.render("Press B for Brick Breaker", True, WHITE)
        settings_text = font.render("Press P for Pong", True, WHITE)
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
                if event.key == pygame.K_b:
                    print("Brick Breaker")
                    #pygame.quit()  # Close the menu before starting the game
                    start_brick_breaker()  # Start the Brick Breaker game
                    return  # Ensure the function exits after starting the game
                if event.key == pygame.K_p:
                    print("Pong")
                    # Add your Pong functionality here if needed
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Run the menu function
main_menu()
