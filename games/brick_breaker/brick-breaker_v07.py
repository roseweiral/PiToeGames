import pygame
import sys
import random
import spidev

#==============================================================================#
# Modules in other files
#==============================================================================#

import config
import fsr_logic
import media

#==============================================================================#

# Initialize Pygame
pygame.init()

# Score and lives
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Dynamic bat toggle
dynamic_bat = False

# Settings menu
def settings_menu():
    global ball_speed_multiplier, dynamic_bat
    while True:
        config.screen.fill(config.BLACK)
        title_text = font.render("Settings", True, config.WHITE)
        speed_text = font.render(f"Ball Speed (1-9): {ball_speed_multiplier}", True, config.WHITE)
        dynamic_bat_text = font.render(f"Dynamic Bat (B): {'On' if dynamic_bat else 'Off'}", True, config.WHITE)
        exit_text = font.render("Press ESC to return to the main menu", True, config.WHITE)

        config.screen.blit(title_text, (config.WIDTH // 2 - title_text.get_width() // 2, 50))
        config.screen.blit(speed_text, (config.WIDTH // 2 - speed_text.get_width() // 2, 150))
        config.screen.blit(dynamic_bat_text, (config.WIDTH // 2 - dynamic_bat_text.get_width() // 2, 250))
        config.screen.blit(exit_text, (config.WIDTH // 2 - exit_text.get_width() // 2, 350))

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
    if config.ball.colliderect(config.paddle):
        media.paddle_hit_sound.play()  # Play paddle hit sound
        if dynamic_bat:
            zone_width = config.PADDLE_WIDTH / 10
            impact_zone = int((ball.x - config.paddle.x) // zone_width) + 1

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
        config.screen.fill(config.BLACK)
        title_text = font.render("Brick Breaker", True, config.WHITE)
        start_text = font.render("Press 1 to Start Game", True, config.WHITE)
        settings_text = font.render("Press S for Settings", True, config.WHITE)
        exit_text = font.render("Press ESC to Quit", True, config.WHITE)

        config.screen.blit(title_text, (config.WIDTH // 2 - title_text.get_width() // 2, 50))
        config.screen.blit(start_text, (config.WIDTH // 2 - start_text.get_width() // 2, 150))
        config.screen.blit(settings_text, (config.WIDTH // 2 - settings_text.get_width() // 2, 250))
        config.screen.blit(exit_text, (config.WIDTH // 2 - exit_text.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Initialize ball speed and position
                    global ball_speed_x, ball_speed_y, ball
                    ball.x, ball.y = config.WIDTH // 2, config.HEIGHT // 2  # Reset ball position
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
    fsr_value_left = fsr_logic.read_adc(fsr_logic.FSR_CHANNEL_LEFT)
    fsr_value_right = fsr_logic.read_adc(fsr_logic.FSR_CHANNEL_RIGHT)

    # Logging FSR events
    if fsr_value_left > fsr_logic.fsr_threshold:
        print(f"FSR LEFT event detected: Value = {fsr_value_left}")
    if fsr_value_right > fsr_logic.fsr_threshold:
        print(f"FSR RIGHT event detected: Value = {fsr_value_right}")

    # Movement control for fsr player (paddle control with FSRs)
    if fsr_value_left > fsr_logic.fsr_threshold and config.paddle.left > 0:
        config.paddle.x -= config.paddle_speed
        print("Paddle moves left (FSR LEFT detected)")
    if fsr_value_right > fsr_logic.fsr_threshold and config.paddle.right < config.WIDTH:
        config.paddle.x += config.paddle_speed
        print("Paddle moves right (FSR RIGHT detected)")

    # Ball movement
    config.ball.x += ball_speed_x
    config.ball.y += ball_speed_y

    # Ball collision with walls
    if config.ball.left <= 0 or config.ball.right >= config.WIDTH:
        media.wall_hit_sound.play()  # Play wall hit sound
        ball_speed_x = -ball_speed_x
    if config.ball.top <= 0:
        media.wall_hit_sound.play()
        ball_speed_y = -ball_speed_y

    # Ball collision with paddle
    handle_ball_paddle_collision()

    # Ball collision with bricks
    for brick in config.bricks[:]:
        brick_rect, brick_color = brick
        if config.ball.colliderect(brick_rect):
            media.brick_hit_sound.play()  # Play brick hit sound
            ball_speed_y = -ball_speed_y
            config.bricks.remove(brick)
            score += 10

    # Ball out of bounds
    if config.ball.bottom >= config.HEIGHT:
        media.life_lost_sound.play()  # Play life lost sound
        lives -= 1
        config.ball.x, config.ball.y = config.WIDTH // 2, config.HEIGHT // 2
        ball_speed_x, ball_speed_y = random.choice([-2, 2]) * ball_speed_multiplier, -0.5 * ball_speed_multiplier
        if lives == 0:
            media.game_over_sound.play()  # Play game over sound
