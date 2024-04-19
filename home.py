import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Never Give Up")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

background_image = pygame.image.load("Game/images/home_page.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Fonts
title_font = pygame.font.SysFont(None, 64)
button_font = pygame.font.SysFont(None, 36)

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Main menu function
def main_menu():
    while True:
        screen.fill(WHITE)
        screen.blit(background_image,(0,0))
        draw_text("Never Give Up", title_font, (255,255,255), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        
        # Play Button
        play_button = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(screen, RED, play_button)
        draw_text("Play", button_font, WHITE, screen, play_button.centerx, play_button.centery)

        # Quit Button
        # quit_button = pygame.Rect(300, 400, 200, 50)
        # pygame.draw.rect(screen, RED, quit_button)
        # draw_text("Quit", button_font, WHITE, screen, quit_button.centerx, quit_button.centery)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    # Call your play function here
                    pass  # Placeholder for play function
                # elif quit_button.collidepoint(mouse_pos):
                #     pygame.quit()
                #     sys.exit()

        pygame.display.update()

# Run the main menu
if __name__ == "__main__":
    main_menu()
