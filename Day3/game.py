import math
import pygame
import sys
import math

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


# Colors
GREY = 0xF2F2F2
BLACK = 0x000000
WHITE = 0xFFFFFF
KEY_C = 0xF6BE37
KEY_CS = 0x8064C6
KEY_D = 0x95C631
KEY_DS = 0xED3883
KEY_E = 0x45B5A1
KEY_F = 0xF7943D
KEY_FS = 0x4E61D8
KEY_G = 0xD1C12E
KEY_GS = 0xA542B1
KEY_A = 0x4BB250
KEY_AS = 0xF75839
KEY_B = 0x4598B6
key_colors = [
    KEY_C,
    KEY_CS,
    KEY_D,
    KEY_DS,
    KEY_E,
    KEY_F,
    KEY_FS,
    KEY_G,
    KEY_GS,
    KEY_A,
    KEY_AS,
    KEY_B,
]

key_text = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]

# Button coordinates
button_centres = [
    (105, 100),
    (195, 100),
    (285, 100),
    (375, 100),
    (105, 190),
    (195, 190),
    (285, 190),
    (375, 190),
    (105, 280),
    (195, 280),
    (285, 280),
    (375, 280),
]
play_stop_centre = (240, 398)
prev_centre = (140, 398)
next_centre = (340, 398)

# State variables
shift = 0
pattern = 0
playing = True

patterns = [pattern1, pattern2, pattern3, pattern4]

frame_count = 0
key_count = 0


def dist(pointA, pointB):
    return abs(math.sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2))


def check_click(pointA, pointB, radius):
    return dist(pointA, pointB) <= radius


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

play = pygame.image.load("buttons/play.png")
pause = pygame.image.load("buttons/pause.png")
next = pygame.image.load("buttons/next.png")
prev = pygame.image.load("buttons/prev.png")

roboto_mono = pygame.font.Font("fonts/RobotoMono-Light.ttf", 32)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_point = (mouse_pos[0], mouse_pos[1])
            for i in range(len(button_centres)):
                if check_click(mouse_point, button_centres[i], 36):
                    shift = i
            if check_click(mouse_point, play_stop_centre, 48):
                playing = not playing
                frame_count = 0
                key_count = 0
            if check_click(mouse_point, prev_centre, 32):
                pattern = pattern - 1
                pattern = max(0, pattern)
                frame_count = 0
                key_count = 0
            if check_click(mouse_point, next_centre, 32):
                pattern = pattern + 1
                pattern = min(3, pattern)
                frame_count = 0
                key_count = 0

    screen.fill(GREY)

    for i in range(len(button_centres)):
        key_color = key_colors[i]
        if i == shift:
            key_color = BLACK
        pygame.draw.circle(screen, key_color, button_centres[i], 36)
        text = roboto_mono.render(key_text[i], True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = button_centres[i]
        screen.blit(text, text_rect)

    if playing:
        screen.blit(pause, (192, 350))
    else:
        screen.blit(play, (192, 350))
    screen.blit(prev, (108, 366))
    screen.blit(next, (308, 366))
    if frame_count == 120:
        key_count = 0

    frames_per_key = 120 // len(patterns[pattern])
    if playing and (frame_count % frames_per_key == 0):
        play_shifted(patterns[pattern][key_count], shift)
        key_count += 1

    frame_count = frame_count % 120
    frame_count += 1

    # Update display
    pygame.display.update()

    # Wait for FPS cap
    pygame.time.Clock().tick(FPS)
