import pygame

def battle_voltmeter():
    # Initialize Pygame
    pygame.init()

    # Set up the window
    WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Leonel Gods")
    clock = pygame.time.Clock()

    # Load and scale background image
    background_image = pygame.image.load("assets/sprites/background.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


    # Load and scale heart image
    heart_image = pygame.image.load("assets/sprites/heart.png").convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (40, 40))  # Adjust size as needed

    # Load and scale sprite images
    new_cursor = pygame.image.load("assets/sprites/01.png").convert_alpha()
    pygame.mouse.set_visible(False)
    dialogue_image = pygame.image.load("assets/sprites/dialogue.png").convert_alpha()
    dialogue_image = pygame.transform.scale(dialogue_image, (1475, 280))

    # Load and scale sprite images
    player_sprite = pygame.image.load("assets/sprites/player_sprite.png").convert_alpha()
    enemy_sprite = pygame.image.load("assets/sprites/enemy_sprite_fire.png").convert_alpha()

    # Scale sprite images
    sprite_width, sprite_height = 250, 250
    player_sprite = pygame.transform.scale(player_sprite, (sprite_width, sprite_height))
    # = pygame.transform.scale(enemy_sprite, (sprite_width + 50, sprite_height + 50))
    # Load and play music
    pygame.mixer.music.load("assets/music/background_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)   # Play in a loop

    # Load sound effects
    button_click_sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")
    attack_sound = pygame.mixer.Sound("assets/sounds/attack.mp3")
    damage_sound = pygame.mixer.Sound("assets/sounds/damage.mp3")
    notif_sound = pygame.mixer.Sound("assets/sounds/notification.wav")
    over_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")
    click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
    pygame.mixer.Sound.set_volume(click_sound, 0.5)
    pygame.mixer.Sound.set_volume(damage_sound, 0.5)
    pygame.mixer.Sound.set_volume(attack_sound, 5)
    # Reward Sprite
    reward = pygame.image.load('assets/sprites/voltmeter.png')

    # Define colors and fonts
    colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (200, 200, 200),
              'red': (255, 0, 0), 'green': '#228b22', 'blue': (0, 0, 255), 'orange': '#fe6f5e'}
    font = pygame.font.Font('assets/ngger.ttf', 28)


    # Game variables
    player_hp, enemy_hp = 3, 3
    dialogues = ["A wild monster appeared!", "The monster has seized the voltmeter! ", "Beware, for it now wields the power of volts against you."]
    current_dialogue = 0
    question_answered = False
    game_ended = False
    game_lost = False  # New variable to track if the game is lost

    # Define paths for button images
    button_image_normal_path = "assets/sprites/Button_Blue_3Slides.png"
    button_image_pressed_path = "assets/sprites/Button_Blue_3Slides_Pressed.png"

    # Load button images
    button_image_normal = pygame.image.load(button_image_normal_path).convert_alpha()
    button_image_pressed = pygame.image.load(button_image_pressed_path).convert_alpha()

    # Scale button images
    button_width, button_height = 200, 80
    button_x, button_y, button_spacing = 100, 180, 40
    button_image_normal = pygame.transform.scale(button_image_normal, (button_width, button_height))
    button_image_pressed = pygame.transform.scale(button_image_pressed, (button_width, button_height))

    questions = [
        {
            "question": "What electrical quantity does a voltmeter measure?",
            "choices": ["Voltage", "Ohms", "Ampere"],
            "correct_answer": "Voltage"
        },
        {
            "question": "What are the typical units used to express voltmeter readings?",
            "choices": ['Ampere', 'Ohms', 'Volts'],
            "correct_answer": "Volts"
        },
        {
            "question": "What type of circuit element are most voltmeters?",
            "choices": ["Active", "Dynamic", "Passive"],
            "correct_answer": "Passive"
        },
        {
            "question": "What type of current do most voltmeters measure?",
            "choices": ["DC only", "AC only", "DC and AC"],
            "correct_answer": "DC and AC"
        },
        {
            "question": "What is the typical connection method for a voltmeter in a circuit?",
            "choices": ["Series", "Parallel", "Horizontal"],
            "correct_answer": "Parallel"
        }
    ]

    current_question_index = 0



    class Enemy(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__()
            self.attack_animation = False
            self.sprites = []
            sprite_paths = ['assets/sprites/fire_1.png', 'assets/sprites/fire_2.png', 'assets/sprites/fire_3.png', 'assets/sprites/fire_4.png']
            for path in sprite_paths:
                sprite = pygame.image.load(path)
                scaled_sprite = pygame.transform.scale(sprite, (320, 320))  # Resize each frame of the sprite animation
                self.sprites.append(scaled_sprite)

            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
            self.animation_timer = pygame.time.get_ticks()  # Timer for animation

        def update(self):
            # Set animation speed (milliseconds per frame)
            animation_speed = 200  # Adjust as needed for desired animation speed
            # Check if it's time to update the sprite image
            if pygame.time.get_ticks() - self.animation_timer >= animation_speed:
                self.animation_timer = pygame.time.get_ticks()  # Reset timer
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites)  # Loop through sprite list
                self.image = self.sprites[self.current_sprite]


    moving_sprites = pygame.sprite.Group()
    enemy = Enemy(550, 205)
    moving_sprites.add(enemy)



    class Button:
        def __init__(self, text, x, y, width, height, image_normal, image_pressed, font, font_size,
                     clickable=True):  # Add font properties
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.image_normal = image_normal
            self.image_pressed = image_pressed
            self.font = pygame.font.Font(font, font_size)  # Load font
            self.text_y = y + height // 2.4  # Adjust the vertical position of the text
            self.clickable = clickable  # Store clickable state

        def draw(self, surface):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if self.rect.collidepoint(mouse):
                surface.blit(self.image_pressed, self.rect)
                if click[0] == 1 and self.clickable:  # Check if clickable
                    return True, self.text
            else:
                surface.blit(self.image_normal, self.rect)

            text_surface = self.font.render(self.text, True, colors['black'])  # Use custom font
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.text_y))
            surface.blit(text_surface, text_rect)

            return False, None

    def display_text(text, x, y, color='black'):
        text_surface = font.render(text, True, colors[color])
        text_rect = text_surface.get_rect(center=(x, y))
        window.blit(text_surface, text_rect)


    # Initialize variables to track sound playing
    notification_sound_played = False
    over_sound_played = False

    running = True
    while running:
        window.blit(background_image, (0, 0))
        window.blit(player_sprite,(250,350))

        enemy.update()  # Update enemy animation continuously
        moving_sprites.draw(window)
        moving_sprites.update()
        # pygame.display.flip()
        # clock.tick(60)

        if current_dialogue < len(dialogues) and not game_ended and not game_lost:
            # Display dialogues
            box_height = 175
            box_y = WINDOW_HEIGHT - box_height
            pygame.draw.rect(window, colors['gray'], (0, box_y, WINDOW_WIDTH, box_height))
            window.blit(dialogue_image, (-100, WINDOW_HEIGHT - box_height - 55))
            display_text(dialogues[current_dialogue], WINDOW_WIDTH // 2, WINDOW_HEIGHT - box_height // 2, 'black')

            if pygame.mouse.get_pressed()[0]:
                click_sound.play(0)
                current_dialogue += 1
                pygame.time.wait(300)
        elif current_question_index < len(questions) and not question_answered and not game_ended and not game_lost:
            # Display questions and choices
            question = questions[current_question_index]
            box_height = 175
            box_y = WINDOW_HEIGHT - box_height
            pygame.draw.rect(window, colors['gray'], (0, box_y, WINDOW_WIDTH, box_height))
            window.blit(dialogue_image, (-100, WINDOW_HEIGHT - box_height - 55))
            display_text(question["question"], WINDOW_WIDTH // 2, WINDOW_HEIGHT - box_height // 2, 'black')

            # Create buttons for choices
            buttons = []
            for i, choice in enumerate(question["choices"]):
                button = Button(choice, button_x, button_y + i * (button_height + button_spacing),
                                button_width, button_height, button_image_normal, button_image_pressed,
                                'assets/ngger.ttf', 28)  # Use font properties directly
                buttons.append(button)

            # Check for button clicks
            for button in buttons:
                clicked, choice = button.draw(window)
                if clicked:
                    button_click_sound.play()
                    pygame.time.wait(300)
                    question_answered = True
                    if choice == question["correct_answer"]:
                        enemy_hp -= 1
                        attack_sound.play(0)

                    else:
                        player_hp -= 1
                        damage_sound.play(0)

                    pygame.time.wait(300)

        elif question_answered and not game_ended and not game_lost:
            current_question_index += 1
            question_answered = False

            if current_question_index >= len(questions) or player_hp <= 0 or enemy_hp <= 0:
                # All questions answered or game ended
                if enemy_hp <= 0:
                    dialogues.append("You win! Congratulations.")
                    game_ended = True
                elif player_hp <= 0:
                    dialogues.append("You lose ! Game over.")
                    game_lost = True  # Set game_lost to True if player loses
                    game_ended = True
                else:
                    dialogues.append("Game over.")
                    game_ended = True

        elif game_ended:
            # Display the last dialogue
            if current_dialogue < len(dialogues):
                box_height = 175
                box_y = WINDOW_HEIGHT - box_height
                pygame.draw.rect(window, colors['gray'], (0, box_y, WINDOW_WIDTH, box_height))
                window.blit(dialogue_image, (-100, WINDOW_HEIGHT - box_height - 55))
                display_text(dialogues[current_dialogue], WINDOW_WIDTH // 2, WINDOW_HEIGHT - box_height // 2, 'black')

                if pygame.mouse.get_pressed()[0]:
                    if not game_lost:
                        if not notification_sound_played:
                            notif_sound.play(0)
                            notification_sound_played = True
                    else:
                        if not over_sound_played:
                            over_sound.play(0)
                            over_sound_played = True
                    current_dialogue += 1
                    pygame.time.wait(300)
            else:
                # Display the reward sprite and wait for user to exit (if game is won)
                if not game_lost:
                    window.blit(reward, (525, 200))
                    window.blit(dialogue_image, (-100, WINDOW_HEIGHT - box_height - 55))
                    display_text(f"Behold your triumph: a Voltmeter, now yours!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.15,
                                 'green')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        running = False

        pos = pygame.mouse.get_pos()
        window.blit(new_cursor, pos)

        # Display HP
        for i in range(player_hp):
            window.blit(heart_image, (100 + i * 50, 50))

        for i in range(enemy_hp):
            window.blit(heart_image, (WINDOW_WIDTH - (150 + i * 50), 50))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        pygame.display.update()
    pygame.quit()
