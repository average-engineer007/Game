import pygame, sys
import os
import random


pygame.init()
pygame.display.set_caption('Fruit-Ninja Game in Python -- GetProjects.org')

WIDTH = 800
HEIGHT = 500
FPS = 60
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
player_lives = 3   

rope = pygame.image.load('falling/images/rope.png')
rope = pygame.transform.rotozoom(rope, 0, 2)
rope_rect = rope.get_rect(midbottom=(100, 100))

fan = pygame.image.load('falling/images/fan.png')
fan_rect = fan.get_rect(midbottom=(200, 200))

hangman = pygame.image.load('falling/images/hangman.png').convert_alpha()
hangman_rect = hangman.get_rect(midbottom=(40, 300))

# Create a blank surface for the composite image
composite_width = max(rope_rect.width, fan_rect.width, hangman_rect.width)
composite_height = rope_rect.height + fan_rect.height + hangman_rect.height
composite_surface = pygame.Surface((composite_width, composite_height), pygame.SRCALPHA)

# Blit the images onto the composite surface
composite_surface.blit(hangman, hangman_rect)
composite_surface.blit(rope, rope_rect.move(0, hangman_rect.height))
composite_surface.blit(fan, fan_rect.move(0, hangman_rect.height + rope_rect.height))




class objects(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x_pos=random.randint(200, 600)
        y_pos=-100
        self.fan = pygame.image.load('falling/images/fan.png')
        self.fan=pygame.transform.rotozoom(self.fan,0,1.4)
        self.fan_rect = self.fan.get_rect(midbottom=(x_pos,y_pos))
        self.rope = pygame.image.load('falling/images/rope.png')
        scale_factor = random.uniform(3, 7)  # Generate a random scale factor between 4 and 7
        self.rope = pygame.transform.rotozoom(self.rope, 0, 2)  # Reset the scale to 1 to maintain the width
        rope_width, rope_height = self.rope.get_size()
        self.rope = pygame.transform.scale(self.rope, (rope_width, int(rope_height * scale_factor)))  # Scale the height
        self.rope_rect = self.rope.get_rect(midtop=(x_pos, self.fan_rect.bottom-13))
        self.hangman = pygame.image.load('falling/images/hangman.png').convert_alpha()
        self.hangman_rect = self.hangman.get_rect(midtop=(x_pos, self.rope_rect.bottom-1))
        self.happy = pygame.image.load('falling/images/happy_stickman.png').convert_alpha()
        self.happy_rect = self.hangman.get_rect(midtop=(x_pos, self.rope_rect.bottom-1))
        self.skull= pygame.image.load('falling/images/game_over.png').convert_alpha()
        self.skull=pygame.transform.rotozoom(self.skull, 0, 0.3)
        self.skull_rect = self.hangman.get_rect(midtop=(x_pos, self.rope_rect.bottom-1))
        # self.rect = self.image.get_rect(bottomright=(random.randint(200, 600), -200))
        # border_color = (0, 0, 0)  # Example: white color
        # border_width = 2
        # image_width, image_height = self.image.get_size()
        # pygame.draw.rect(self.image, border_color, (0, 0, image_width, image_height), border_width)
        self.gravity=0
        self.player_index=0
        # self.x_pos=self.rect.x
        # self.y_pos=self.rect.y
        self.move_x=0
        self.move_y=0
        self.hit=False
        self.border_color = (255, 0, 0)  # Red border color
        self.border_width = 2
        self.dead = False
        self.count=0
    
    def player_movement(self):
        self.gravity+=1
        if(self.gravity>5):
            self.gravity=5

        self.fan_rect.y+=self.gravity
        self.rope_rect.y+=self.gravity
        self.hangman_rect.y+=self.gravity
        self.happy_rect.y+=self.gravity
        self.skull_rect.y+=self.gravity


    def destroy(self):
        global player_lives
        if self.rope_rect.y>600:
            if not self.hit:
                player_lives-=1
            self.kill()
        if self.count==20:
            self.kill()
    def draw(self):
        if self.hit:
            gameDisplay.blit(self.happy,self.happy_rect)
            self.count+=1
        elif self.dead:
            gameDisplay.blit(self.skull,self.skull_rect)
            self.count+=1
        # Blit the falling object onto the specified surface
        else:
            gameDisplay.blit(self.rope, self.rope_rect)
            gameDisplay.blit(self.fan, self.fan_rect)
            # pygame.draw.rect(gameDisplay, self.border_color, self.fan_rect, self.border_width)
            pygame.draw.rect(gameDisplay, self.border_color, self.rope_rect, self.border_width)
            pygame.draw.rect(gameDisplay, self.border_color, self.hangman_rect, self.border_width)
            gameDisplay.blit(self.hangman, self.hangman_rect)          

    def update(self):
        self.player_movement()
        self.destroy()
        self.draw()




score = 0                                                       #keeps track of score
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']    #entities in the game

clock = pygame.time.Clock()

# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

w=2
lines = []
last_pos = None
line_duration = 0.25
screen_color = (255,255,200)

background = pygame.image.load('falling/back.jpg')                                  #game background
font = pygame.font.Font(os.path.join(os.getcwd(), 'falling/comic.ttf'), 42)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))    #score display
lives_icon = pygame.image.load('falling/images/white_lives.png')                    #images that shows remaining lives
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1200)


# rope = pygame.image.load('falling/images/rope.png') 
rope = pygame.transform.rotozoom(rope,0,2)
rope_rect=rope.get_rect(midbottom=(100,100))
# fan=pygame.image.load('falling/images/fan.png')
# fan_rect=fan.get_rect(midbottom=(200,200))
# hangman = pygame.image.load('falling/images/hangman.png').convert_alpha()
# hangman_rect=hangman.get_rect(midbottom=(40,300))
slash=pygame.image.load('falling/images/slash.png')
slash_rect=slash.get_rect(midbottom=(250,250))
border_color = (255, 0, 0)  # Red
border_width = 2

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("falling/images/red_lives.png"), (x, y))

# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

# draw players lives
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #gets the (x,y) coordinates of the cross icons (lives on the the top rightmost side)
        img_rect.x = int(x + 35 * i)    #sets the next cross icon 35pixels awt from the previous one
        img_rect.y = y                  #takes care of how many pixels the cross icon should be positioned from top of the screen
        display.blit(img, img_rect)
def line_rect_collision(line_start, line_end, rect):
    # Unpack rectangle coordinates
    if(len(rect.clipline(start_pos,end_pos))): 
        return True
    return False

# Game Loop
object_group=pygame.sprite.Group()
first_round = True
game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
drawing = False
while True : 
    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYUP:
            if(game_over==True):
                game_over=False
                if(first_round):
                    first_round=False
                game_over=False
        if event.type == obstacle_timer and not(game_over):
            object_group.add(objects())
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                mouse_position = pygame.mouse.get_pos()
                if last_pos is not None:
                    pygame.draw.line(gameDisplay, (255,0,0), (last_pos[0], last_pos[1]), (mouse_position[0], mouse_position[1]), w)
                    lines.append((last_pos, mouse_position, current_time))
                last_pos = mouse_position
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_position = (0, 0)
            drawing = False
            last_pos = None
            last_scroll = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        current_time = pygame.time.get_ticks()
    for line in lines:
        start_pos, end_pos, timestamp= line
        if (current_time - timestamp) / 1000 >= line_duration:
            lines.remove(line)
    gameDisplay.fill(screen_color)  # Clear screen
    for line in lines:
        start_pos, end_pos, timestamp= line
        pygame.draw.line(gameDisplay, (0,0,200), (start_pos[0],start_pos[1]), (end_pos[0], end_pos[1]), 2*w)
        pygame.draw.line(gameDisplay, (255,255,255), (start_pos[0],start_pos[1]), (end_pos[0], end_pos[1]), w)
        for obj in object_group:
            playercut = False
            ropecut = False
            if(line_rect_collision(start_pos,end_pos,obj.rope_rect)):
                ropecut = True
            if((line_rect_collision(start_pos,end_pos,obj.hangman_rect))):
                if(obj.dead== False):
                    obj.dead = True
                    playercut = True
            if(not obj.dead):
                if(playercut):
                    player_lives-=1
                    print('mar gya')
                elif ropecut:
                    obj.hit = True
                    print('kat gya')
            else :
                if(playercut):
                    player_lives-=1
                    print('mar gya')
        
    # obstacle_group.draw(screen)
    if game_over :
        if first_round :
            draw_text(gameDisplay,"Score : " + str(score), 50, WIDTH / 2, HEIGHT /2)
        gameDisplay.blit(background, (0,0))
        # print("yes")
        draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
        draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
        player_lives = 3
        # draw_lives(gameDisplay, 690, 5, player_lives, 'Fruit/images/red_lives.png')
        score = 0

    else:
        
        # gameDisplay.blit(background, (0, 0))
        # gameDisplay.fill((255,255,200))
        # gameDisplay.blit(score_text, (0, 0))
        # gameDisplay.blit(rope,rope_rect)
        # gameDisplay.blit(hangman, hangman_rect)
        # gameDisplay.blit(fan,fan_rect)
        # gameDisplay.blit(slash,slash_rect)
        # gameDisplay.blit(composite_surface,(100,100))
        # print(hangman_rect.x,hangman_rect.y)
        # pygame.draw.rect(gameDisplay, border_color, rope_rect, border_width)
        # pygame.draw.rect(gameDisplay, border_color, fan_rect, border_width)
        # pygame.draw.rect(gameDisplay, border_color, hangman_rect, border_width)
        # pygame.draw.rect(gameDisplay, border_color, slash_rect, border_width)
        draw_lives(gameDisplay, 690, 5, player_lives, 'falling/images/red_lives.png')
        # object_group.draw(gameDisplay) 
        current_position = pygame.mouse.get_pos()   #gets the current coordinate (x, y) in pixels of the mouse
        object_group.update()
        if(player_lives<1):
            game_over=True

    pygame.display.update()
    clock.tick(FPS)                              