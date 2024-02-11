import pygame
import random
import subprocess

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokemon-style Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

# Define enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.defeated = False  # Flag to track if the enemy has been defeated

# Function to fade the screen to black
def fade_to_black(screen):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Collision detection
    hits = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in hits:
        if not enemy.defeated:
            # Fade to black
            fade_to_black(screen)
            # Transition to battle script
            subprocess.run(["python", "battle_script.py"])
            # Mark the enemy as defeated
            enemy.defeated = True

    # Check if there are any active enemies left
    active_enemies = any(not enemy.defeated for enemy in enemies)

    # Update
    all_sprites.update()

    # Render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Check if there are no active enemies left
    if not active_enemies:
        # Display congratulations scene
        # You can add your code here to display the congratulations scene
        font = pygame.font.Font(None, 36)
        text = font.render("Congratulations! You defeated all enemies!", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Display the message for 3 seconds

        # Exit the game loop
        running = False

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
