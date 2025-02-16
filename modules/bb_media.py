# modules/bb_media.py
import pygame

# Initialize the pygame mixer
pygame.mixer.init()

class Media:
    # Load the sound files
    paddle_hit_sound = pygame.mixer.Sound("sounds/ding.wav")
    wall_hit_sound = pygame.mixer.Sound("sounds/ding.wav")
    brick_hit_sound = pygame.mixer.Sound("sounds/brickbreak.wav")
    life_lost_sound = pygame.mixer.Sound("sounds/critical.wav")
    game_over_sound = pygame.mixer.Sound("sounds/gameover.wav")
    winner_sound = pygame.mixer.Sound("sounds/winner.wav")

music_playing = False

def play_background_music():
    global music_playing
    if not music_playing:  # Check if music is not already playing
        """Loads and plays the background music in a loop."""
        pygame.mixer.music.load("sounds/background.wav")  # Load the music file
        pygame.mixer.music.play(-1)  # Loop indefinitely (-1 means infinite loop)
        pygame.mixer.music.set_volume(0.1)  # Set volume (adjust as needed)
        music_playing = True
    
def stop_background_music():
    global music_playing
    """Stops the background music."""
    pygame.mixer.music.stop()
    music_playing = False
