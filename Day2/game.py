import pygame

# Setup window vars
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480
FPS = 60

# Music patterns
pattern1 = [0, 4, 7, 12, 16, 12, 7, 4]
pattern2 = [14, 19, 17, 19, 14, 19, 17, 19]
pattern3 = [0, 2, 4, 7]
pattern4 = [
    (0, 7),
    (4, 11),
    (7, 14),
    (12, 19),
    (7, 14),
    (4, 19),
    (0, 24),
    (4, 19),
    (7, 24),
    (12, 28),
    (7, 24),
    (4, 19),
]

# State variables
shift = 0
pattern = 0

patterns = [pattern1, pattern2, pattern3, pattern4]

frame_count = 0
key_count = 0


def play_shifted(key, shift):
    if type(key) == tuple:
        for actual_key in key:
            keysound = pygame.mixer.Sound(f"soundbank/{actual_key + shift}.wav")
            pygame.mixer.Channel(actual_key).play(keysound)
    else:
        keysound = pygame.mixer.Sound(f"soundbank/{key + shift}.wav")
        pygame.mixer.Channel(key).play(keysound)


# Initialize pygame
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(36)


size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Arpeggio")

while True:
    if frame_count == 120:
        key_count = 0

    frames_per_key = 120 // len(patterns[pattern])
    if frame_count % frames_per_key == 0:
        play_shifted(patterns[pattern][key_count], shift)
        key_count += 1

    frame_count = frame_count % 120
    frame_count += 1

    # Update display
    pygame.display.update()

    # Wait for FPS cap
    pygame.time.Clock().tick(FPS)
