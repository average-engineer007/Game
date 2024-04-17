import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Obstacle Example")

# Define colors
WHITE = (255, 255, 255)

class Ropes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Game/images/rope.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 3, self.image.get_height() // 3))
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self, scroll):
        self.rect.x += scroll[0]
        self.rect.y += scroll[1]

# Create ropes instances
ropes_group = pygame.sprite.Group()

def generate_ropes():
    for _ in range(5):  # Adjust as needed
        rope = Ropes(random.randint(0, screen_width), random.randint(0, screen_height))
        ropes_group.add(rope)

generate_ropes()

# Game variables
scroll = [0, 0]
player_x = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        scroll[0] -= 5
        player_x += 5

    # Generate new ropes as player moves forward
    if player_x % 200 == 0:  # Adjust as needed
        generate_ropes()

    # Remove ropes that go out of vision
    for rope in ropes_group.copy():
        if rope.rect.right < 0:
            ropes_group.remove(rope)

    # Update
    ropes_group.update(scroll)

    # Draw
    screen.fill((0, 0, 0))  # Clear the screen
    for rope in ropes_group:
        rope_rect = rope.rect.move(-scroll[0], -scroll[1])
        screen.blit(rope.image, rope_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
