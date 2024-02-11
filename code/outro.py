import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Leonel ECE Journey")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BG_IMAGES = [pygame.image.load(os.path.join('outro_background', 'outro_1.jpg')).convert(),
             pygame.image.load(os.path.join('outro_background', 'outro_2.jpg')).convert(),
             pygame.image.load(os.path.join('outro_background', 'outro_3.jpg')).convert(),
             pygame.image.load(os.path.join('outro_background', 'outro_4.jpg')).convert(),
             pygame.image.load(os.path.join('outro_background', 'outro_5.jpg')).convert(),]


# Define font and font size
intro_font = pygame.font.Font('assets/ngger.ttf', 17)

character = pygame.image.load("assets/down_idle.png")
# Function to animate the background frames
WIN.blit(character, (WIDTH / 2 - character.get_width() / 2, HEIGHT / 2 - character.get_height() / 2))
pygame.display.flip()



def outro_animate_with_text(BG_IMAGES, text, x, y, line_spacing, word_spacing, char_delay):
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
        WIN.blit(current_frame, (-100, -100))

        # Render text character by character with typewriter effect
        if char_index < len(text):
            current_text += text[char_index]
            text_surface = intro_font.render(current_text, True, WHITE)
            text_rect = text_surface.get_rect(topleft=(x, y))
            char_index += 1

        # Blit the entire text surface onto the window
        if text_surface:
            WIN.blit(text_surface, text_rect)

        # Blit the character onto the screen
        WIN.blit(character,(WIDTH / 2 - character.get_width() / 2, HEIGHT / 2 - character.get_height() / 2))

        # Update the display
        pygame.display.update()

        # Move to the next frame
        frame_index = (frame_index + 1) % frame_count

        # Control frame rate
        clock.tick(75)

        # Delay between each character
        pygame.time.delay(char_delay)



def main():

    for text, outro_vo, audio_file in [
        ("Congratulations on completing your journey.", 'outro_vo', "audio_out_1.mp3"),
        ("Your perseverance and skill have paid off.", 'outro_vo', "audio_out_2.mp3"),
        ("Thank you for playing! Until next time.", 'outro_vo', "audio_out_3.mp3")
    ]:
        # Load and play audio
        audio = pygame.mixer.Sound(os.path.join(outro_vo, audio_file))
        audio.play()



        # Animate text and check if mouse click was detected
        mouse_click_detected = outro_animate_with_text(BG_IMAGES, text, 425, 400, 30, 1, char_delay=75)

        if mouse_click_detected:
            audio.stop()


if __name__ == "__main__":
    main()