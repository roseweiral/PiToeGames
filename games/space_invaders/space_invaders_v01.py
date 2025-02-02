import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Enemy
enemy_size = 50
enemy_speed = .5
enemies = []

# Bullet
bullet_size = 5
bullet_speed = 10
bullets = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Create enemies
def create_enemies():
    for i in range(5):
        for j in range(3):
            enemy_x = i * (enemy_size + 20) + 100
            enemy_y = j * (enemy_size + 20) + 50
            enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size))

# Main game loop
def game_loop():
    global player_x, player_y, score
    clock = pygame.time.Clock()
    create_enemies()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player_x + player_size // 2 - bullet_size // 2, player_y, bullet_size, bullet_size))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                pygame.quit()
                sys.exit()

        # Check for collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop() 