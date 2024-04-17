from typing import Any
import pygame
from sys import exit
import random

# from pygame.sprite import _Group


#
pygame.init()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global scroll_x
        global scroll_y
        self.image=pygame.image.load('Game/images/Layer 1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200,300))
        border_color = (0, 0, 0)  # Example: white color
        border_width = 2
        image_width, image_height = self.image.get_size()
        pygame.draw.rect(self.image, border_color, (0, 0, image_width, image_height), border_width)
        self.gravity=0
        self.player_index=0
        self.x_pos=self.rect.x
        self.y_pos=self.rect.y
  
    def player_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] :
            self.rect.y-=5
        if keys[pygame.K_DOWN] :
            self.rect.y+=5
        if keys[pygame.K_RIGHT] :
            self.rect.x+=5
        if keys[pygame.K_LEFT] :
            self.rect.x-=5
    # def apply_gravity(self):
    #     self.gravity+=1
    #     self.rect.y += self.gravity
    #     if self.rect.bottom >=300:
    #         self.rect.bottom=300
    # def animate(self):
    #     # global player_surface,player_index
    #     if self.rect.bottom <300:
    #         self.image=self.player_jump
    #     else:
    #         self.player_index+=0.2
    #         if self.player_index<=1 :
    #             # player_index=0
    #             self.image=self.player_walk1
    #         elif self.player_index<=2:
    #             self.image=self.player_walk2
    #         else:
    #             self.player_index=0

    def update(self):
        
        # self.rect.x=self.x_pos -scroll_x
        # self.rect.y=self.y_pos  - scroll_y
        self.player_input()
        # if(self.rect.x>1000):
        #     self.rect.x-=1000
        #     true_scroll[0]-=1000

        # self.x_pos=self.rect.x+scroll_x
        # self.y_pos=self.rect.y+scroll_y
        
        # self.apply_gravity()
        # self.animate()

# class ropes(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         global scroll_x
#         global scroll_y
#         self.image=pygame.image.load('Game/images/rope.png').convert_alpha()
#         self.image = pygame.transform.scale(self.image, (self.image.get_width() // 3, self.image.get_height() // 3))
#         self.rect = self.image.get_rect(midbottom = (100+scroll_x,300+scroll_y))
#         border_color = (0, 0, 0)  # Example: white color
#         border_width = 2
#         image_width, image_height = self.image.get_size()
#         pygame.draw.rect(self.image, border_color, (0, 0, image_width, image_height), border_width)


class Ropes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Game/images/rope.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 3, self.image.get_height() // 3))
        self.rect = self.image.get_rect(midbottom=(random.randint(0, screen_width), random.randint(0, screen_height)))

    # def update(self, scroll_x, scroll_y):
    #     self.rect.x += scroll_x
    #     self.rect.y += scroll_y

class platforms(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global scroll_x
        global scroll_y
        # test_surface.fill('REd')
        self.image=pygame.Surface((300,50))
        self.image.fill('RED')
        self.rect = self.image.get_rect(midbottom = (300+scroll_x,500+scroll_y))
        border_color = (0, 0, 0)  # Example: white color
        border_width = 2
        image_width, image_height = self.image.get_size()
        pygame.draw.rect(self.image, border_color, (0, 0, image_width, image_height), border_width)
    def update(self):
        self.rect.x=300 +10
        self.rect.y+=500+10

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        # obstacle_group.empty()
        print("mar gaya")
    if pygame.sprite.spritecollide(player.sprite,platform_group,False):
        print("surface collision")



def shift_back():
    if (player.rect.x>1000):
        player.rect.x-=1000
        true_scroll[0]-=1000
        for rope in ropes_group:
            rope.rect.x-=1000




screen = pygame.display.set_mode((1000,800))
screen_width=1000
screen_height=800
clock = pygame.time.Clock()
# test_font = pygame.font.Font('Game/font/Pixeltype.ttf',50)
game_active=True
# font type and font size
scroll_x=0
scroll_y=0
test_surface= pygame.Surface((300,50))
test_surface.fill('REd')
start_time=0
rope=pygame.image.load('Game/images/rope.png')
rope = pygame.transform.scale(rope, (rope.get_width() // 3, rope.get_height() // 3))
player_sp=pygame.sprite.GroupSingle()
player = Player()
player_sp.add(Player())
obstacle_group=pygame.sprite.Group()
# obstacle_group.add(ropes())
platform_group=pygame.sprite.Group()
platform_group.add(platforms())
true_scroll=[0,0]
ropes_group = pygame.sprite.Group()
num_ropes = 5  # Adjust as needed
for _ in range(num_ropes):
    rope = Ropes()
    ropes_group.add(rope)

while True: 
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((255,255,255))
    obstacle_group.draw(screen)
    true_scroll[0] += (player.rect.x-true_scroll[0]-400)/20
    true_scroll[1] += (player.rect.y-true_scroll[1]-300)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    print(scroll[0],end=" ")
    print(player.rect.x,end=" ")
    print(player.rect.x-scroll[0])

    # print(scroll_y)
    # print(scroll_x)
    # screen.blit(rope,(100,300))
    # ropes_group.update(-scroll[0], -scroll[1])
    # ropes_group.draw(screen)
    # screen.blit(test_surface,(300,500)) 
    # shift_back()
    platform_group.draw(screen)
    # platform_group.update()
    obstacle_group.update()
    # collision_sprite()
    player_rect = player.rect.move(-scroll[0], -scroll[1])
    screen.blit(player.image, player_rect)
    for rope in ropes_group:
            rope_rect = rope.rect.move(-scroll[0], -scroll[1])
            screen.blit(rope.image, rope_rect)
    player.update()
    pygame.display.update() 
    clock.tick(60)      



    #player
    


    # set the max frame rate to 60 fps

