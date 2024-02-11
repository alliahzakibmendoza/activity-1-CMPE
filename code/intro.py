import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Leonel Gods")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BG_IMAGES = [pygame.image.load(os.path.join('background', 'ezgif-frame-001.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-002.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-003.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-004.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-005.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-006.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-007.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-008.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-009.jpg')).convert(),
             pygame.image.load(os.path.join('background', 'ezgif-frame-010.jpg')).convert()]

# Define font and font size
intro_font = pygame.font.Font('assets/ngger.ttf', 17)


# Function to animate the background frames
def animate_with_text(BG_IMAGES, text, x, y, line_spacing, word_spacing, char_delay):
    frame_index = 0
    frame_count = len(BG_IMAGES)
    clock = pygame.time.Clock()

    running = True
    current_text = ''
    text_surface = None
    text_rect = None
    char_index = 0
    mouse_click_detected = False  # Flag to indicate if mouse click was detected
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click_detected = True
                running = False
                break

        if not running:
            break

        # Clear the screen
        WIN.fill(BLACK)

        # Draw the current frame onto the window
        current_frame = BG_IMAGES[frame_index]
        WIN.blit(current_frame, (0, 0))

        # Render text character by character with typewriter effect
        if char_index < len(text):
            current_text += text[char_index]
            text_surface = intro_font.render(current_text, True, WHITE)
            text_rect = text_surface.get_rect(topleft=(x, y))
            char_index += 1

        # Blit the entire text surface onto the window
        if text_surface:
            WIN.blit(text_surface, text_rect)

        # Move to the next frame
        frame_index = (frame_index + 1) % frame_count

        # Control frame rate
        clock.tick(75)

        # Update the display
        pygame.display.update()

        # Delay between each character
        pygame.time.delay(char_delay)

    return mouse_click_detected  # Return flag indicating if mouse click was detected


def intro():

    text_audio_pairs = [
        ("With a sudden  and  devastating onslaught,  monsters descended upon our world.",'vo',"audio_1.wav"),
        ("Shattering  humanity's defenses  after countless  battles. Now, a century later",'vo', "audio_2.wav"),
        ("their dark presence looms large engulfing 90 percent of our once thriving planet",'vo', "audio_3.wav"),
        ("amidst  the desolation,  scattered  bands of survivors clinging onto existence",'vo', "audio_4.wav"),
        ("in the most remote and desolate corners and in this bleak landscape of despair",'vo', "audio_5.wav"),
        ("you, our hero, have  stumbled upon a relic from a forgotten era a tome pulsating ",'vo', "audio_6.wav"),
        (" with   all  of   the  secrets   of    ancient   civilization's   technology. ",'vo', "audio_7.wav"),
        ("This discovery ignites  a spark  of  hope  amidst  the  suffocating  darkness",'vo', "audio_8.wav"),
        (" for  within  its  pages  lies  the  potential   to  reclaim  what  was lost ",'vo', "audio_9.wav"),
        ("and stand  against the monstrous  tide   threatening   to  engulf  us  all. ",'vo', "audio_10.wav")]

    for text,vo, audio_file in text_audio_pairs:
        # Load and play audio
        audio = pygame.mixer.Sound(os.path.join(vo, audio_file))
        audio.play()

        # Animate text and check if mouse click was detected
        mouse_click_detected = animate_with_text(BG_IMAGES, text, 225, 350, 30, 1, char_delay=75)

        if mouse_click_detected:
            audio.stop()  # Stop audio if mouse click was detected