import pygame
import math
from sys import exit
import random
# from stickman_gen import stickmanRight

pygame.init()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global scroll_x
        global scroll_y
        self.image=pygame.image.load('images/Layer 1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200,300))

        # self.stickman = stickmanRight(screen, 0,0)
        border_color = (0, 0, 0)  # Example: white color
        border_width = 2
        image_width, image_height = self.image.get_size()
        # pygame.draw.rect(self.image, border_color, (0, 0, image_width, image_height), border_width)
        self.frames = []  # List to store animation frames
        self.frame_index = 0  # Current frame index
        self.load_frames()  # Load animation frames
        self.image = self.frames[self.frame_index]  # Set initial image
        # self.rect = self.image.get_rect(midbottom=(200, 300))  # Set initial position
        self.animation_speed = 0.04  # Animation speed in seconds
        self.animation_timer = pygame.time.get_ticks()  # Timer to control animation speed

        
        
        self.gravity=0
        self.player_index=0
        self.x_pos=self.rect.x
        self.y_pos=self.rect.y
        self.move_x=5
        self.move_y=0
        self.line_collision = False
        self.fall_damage=0
        self.speed = 5
        self.dead = False
    
    def load_frames(self):
    # Load animation frames from individual images
        for i in range(1, 13):
            frame = pygame.image.load(f'images/Layer {i}.png').convert_alpha()
            self.frames.append(frame)

    def update_animation(self):
        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_speed * 1000:
            self.animation_timer = current_time
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def above(self,start_point, end_point):
        v1 = (end_point[0]- start_point[0], end_point[1] - start_point[1])
        v2 = (self.rect.x+self.rect.width/2- start_point[0], self.rect.y+self.rect.height - start_point[1])
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]
        above = True
        if(cross_product < 0):
            above = True
        if(end_point[0] < start_point[0]):
            above = not above
        return above 
    
    def calculate_tangent_vector(self,start_pos, end_pos):
        # Calculate the slope of the line
        mag = math.sqrt((start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2)
        if(mag == 0):
            return 0,0
        tangent_x = (start_pos[0]-end_pos[0])/mag
        tangent_y = (start_pos[1]-end_pos[1])/mag
        return abs(tangent_x), abs(tangent_y)


    def player_movement(self):
        # print(self.move_y, self.gravity)
        # print(self.fall_damage)
        # terminal velocity
        if(self.gravity>0.16):
            self.gravity=0.16
        keys=pygame.key.get_pressed()

        if keys[pygame.K_UP] and keys[pygame.K_LSHIFT]:
            self.move_y=-5
            self.gravity=-0.2
        elif keys[pygame.K_DOWN]and keys[pygame.K_LSHIFT] :
            self.move_y=5
        # else:
        #     self.move_y=0
        # Apply horizontal movement
        if self.line_collision == False or self.above == False: 
            self.move_y+=self.gravity
        
        self.rect.y+=self.move_y
        bottom_platform =False
        top_platform = False
        hit_list = pygame.sprite.spritecollide(self,platform_group,False)
        for tile in hit_list:
            if self.move_y > 0:
                self.rect.bottom = tile.rect.top
                self.move_y = 0
                top_platform=True

            elif self.move_y < 0:
                self.rect.top = tile.rect.bottom+1
                self.move_y = 0
                bottom_platform=True

        # collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        if keys[pygame.K_RIGHT] and keys[pygame.K_LSHIFT]:
            self.move_x=5
        elif keys[pygame.K_LEFT] and keys[pygame.K_LSHIFT]:
            self.move_x=-5
        self.rect.x+=self.move_x

        right_wall=False
        left_Wall = False
        line = True
        hit_list = pygame.sprite.spritecollide(player,platform_group,False)
        for tile in hit_list:
            # print(type(tile.rect))
            if self.move_x > 0:
                self.rect.right = tile.rect.left
                right_wall = True
                # self.gravity=-15
                # self.move_y = -5
                # collision_types['right'] = True
            elif self.move_x < 0:
                self.rect.left = tile.rect.right
                # self.gravity =-15
                # self.move_y = -5
                left_Wall = True
                # collision_types['left'] = True
        self.gravity+=0.03
        # self.stickman.draw()
        line_collide_hitlist= []
        for line in lines:
            start_pos, end_pos, timestamp, old_scroll , last_old_scroll= line
            # print(start_pos, self.rect.x, self.rect.y)
            start_pos = (start_pos[0]+last_old_scroll[0], start_pos[1]+last_old_scroll[1])
            end_pos = (end_pos[0]+old_scroll[0], end_pos[1]+old_scroll[1])
            if len(self.rect.clipline(start_pos,end_pos)):
                # print("Collision detected with line!", self.rect.x, self.rect.y)
                line_collide_hitlist.append(line)
        self.line_collision = False

        hung = pygame.sprite.spritecollide(player,ropes_group,False)
        if(len (hung)>0):
            self.dead = True
            # print('Dead')
        
                
        if len(line_collide_hitlist) > 0:
            self.line_collision = True
            avg_start_pos = None
            avg_end_pos = None
            for line in line_collide_hitlist:
                start_pos, end_pos, timestamp, old_scroll, last_old_scroll = line
                start_pos = (start_pos[0]+last_old_scroll[0], start_pos[1]+last_old_scroll[1])
                end_pos = (end_pos[0]+old_scroll[0], end_pos[1]+old_scroll[1])
                if avg_start_pos != None:
                    avg_start_pos = (avg_start_pos[0] + start_pos[0], avg_start_pos[1] + start_pos[1])
                    avg_end_pos = (avg_end_pos[0] + end_pos[0], avg_end_pos[1] + end_pos[1])
                else:
                    avg_end_pos = end_pos
                    avg_start_pos = start_pos
            avg_start_pos= (avg_start_pos[0]/len(line_collide_hitlist),avg_start_pos[1]/len(line_collide_hitlist) )
            avg_end_pos= (avg_end_pos[0]/len(line_collide_hitlist),avg_end_pos[1]/len(line_collide_hitlist) )
                

                

            
            above_line = self.above(avg_start_pos,avg_end_pos)
        if (not self.line_collision):
            if(right_wall):
                self.gravity= -0.2
                self.move_y = -5
            if(left_Wall):
                self.gravity = -0.2
                self.move_y = -5
        else:
            if(above_line):
                
                tangent_x, tangent_y = self.calculate_tangent_vector(avg_start_pos, avg_end_pos)
                
                if(self.move_y > self.speed):
                    self.fall_damage+=2**(self.move_y/5)
                self.move_x = tangent_x * self.speed
                self.move_y = -tangent_y * self.speed
            else:                
                tangent_x, tangent_y = self.calculate_tangent_vector(avg_start_pos, avg_end_pos)
               
                self.move_x = tangent_x * self.speed
                self.move_y = tangent_y * self.speed
            

        
    def update(self):
        self.player_movement()
        self.update_animation()
        self.speed +=0.0001
        self.animation_speed -= 0.000001


class enemies(pygame.sprite.Sprite):
    def __init__(self,x,y,l,r):
        super().__init__()
        self.image=pygame.image.load('images/NightBorne.png').convert_alpha()
        self.image=pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(midbottom = (x,y))
        border_color = (0, 0, 0)  # Example: white color
        border_width = 2
        image_width, image_height = self.image.get_size()
        # pygame.draw.rect(self.image, border_color, (0, 0, image_width, image_height), border_width)
        self.gravity=0
        self.player_index=0
        self.x_pos=self.rect.x
        self.y_pos=self.rect.y
        self.move_x=0
        self.move_y=0
        self.right_limit=r
        self.left_limit=l
    def calculate_distance(self):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance
        
    def player_movement(self):
        d=self.calculate_distance()
        if(d<500):
            if(player.rect.x<self.rect.x):
                self.move_x=-2
            elif player.rect.x>self.rect.x:
                self.move_x=2


        # self.move_y+=self.gravity
        # self.rect.y+=self.move_y
        # # bottom_platform =False
        # # top_platform = False
        # hit_list = pygame.sprite.spritecollide(self,platform_group,False)
        # for tile in hit_list:

        #     if self.rect.midbottom[0] <= tile.rect.topleft[0]:
        #         self.rect.bottomleft = (tile.rect.topleft[0], self.rect.topleft[1])

        #     # Update the position of the bottom right corner
        #     if self.rect.midbottom[0] >= tile.rect.topright[0]:
        #         self.rect.bottomright = (tile.rect.topright[0], self.rect.topright[1])

        #     if self.move_y > 0:
        #         self.rect.bottom = tile.rect.top
        #         self.move_y = 0
        #         top_platform=True

        #     elif self.move_y < 0:
        #         self.rect.top = tile.rect.bottom
        #         self.move_y = 0
        #         bottom_platform=True

        # collision_types = {'top':False,'bottom':False,'right':False,'left':False}


        self.rect.x+=self.move_x
        hit_list = pygame.sprite.spritecollide(player,platform_group,False)
        if (self.rect.x>self.right_limit):
            self.rect.x=self.right_limit
        if (self.rect.x<self.left_limit):
            self.rect.x=self.left_limit
        # for tile in hit_list:
        #     # print(type(tile.rect))
        #     if self.move_x > 0:
        #         self.rect.right = tile.rect.left
        #         right_wall = True
        #         # self.gravity=-15
        #         # self.move_y = -5
        #         # collision_types['right'] = True
        #     elif self.move_x < 0:
        #         self.rect.left = tile.rect.right



        self.gravity+=0.53
    def destroy(self):
        self.kill()
    
    def update(self):
        self.player_movement()


class ScoreBoard:
    def __init__(self, x, y, font_size=24):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont(None, font_size)
        self.score = 0

    def draw(self, screen):
        text_surface = self.font.render(f"Score: {int(self.score)}", True, (0, 0, 0))
        screen.blit(text_surface, (self.x, self.y))

    def update_score(self, points):
        self.score += points

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.health_color = (0, 255, 0)  # Green color for full health
        self.damage_color = (255, 0, 0)  # Red color for damaged health

    def draw(self, screen):
        # Calculate width of health bar based on current health
        health_width = (self.current_health / self.max_health) * self.width

        # Draw health bar background
        pygame.draw.rect(screen, (128, 128, 128), (self.x, self.y, self.width, self.height))
        
        # Draw health bar
        pygame.draw.rect(screen, self.health_color, (self.x, self.y, health_width, self.height))

    def update_health(self, health):
        # Update current health
        self.current_health = health

        # Change color based on health
        if self.current_health <= 0:
            self.health_color = (0, 0, 0)  # Black color for empty health
        elif self.current_health <= self.max_health / 2:
            self.health_color = self.damage_color

class Ropes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/rope.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 3, self.image.get_height() // 3))
        self.rect = self.image.get_rect(midbottom=(random.randint(0, screen_width), random.randint(0, screen_height)))
    def destroy(self):
        self.kill()
    # def update(self, scroll_x, scroll_y):
    #     self.rect.x += scroll_x
    #     self.rect.y += scroll_y

class platforms(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global scroll_x
        global scroll_y
        # test_surface.fill('REd')
        self.image=pygame.Surface((random.randint(200,300),random.randint(25,100)))
        self.image.fill('#303F9E')
        self.rect = self.image.get_rect(midbottom=(random.randint(0, screen_width), random.randint(0, screen_height)))
        border_color = (0, 0, 0)  # Example: white color
        border_width = 2
        image_width, image_height = self.image.get_size()
        # pygame.draw.rect(self.image, border_color, (0, 0, image_width, image_height), border_width)
    def update(self):
        self.rect.x=300 +10
        self.rect.y+=500+10
    def destroy(self):
        self.kill()

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
rope=pygame.image.load('images/rope.png')
rope = pygame.transform.scale(rope, (rope.get_width() // 3, rope.get_height() // 3))
player_sp=pygame.sprite.GroupSingle()
player = Player()
player_sp.add(Player())
obstacle_group=pygame.sprite.Group()
# obstacle_group.add(ropes())
platform_group=pygame.sprite.Group()
platform_group.add(platforms())
enemy_group=pygame.sprite.Group()
# platform_group.add(platforms())
true_scroll=[0,0]
ropes_group = pygame.sprite.Group()
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
num_ropes = 5  # Adjust as needed
num_platform = 3
drawing = False
last_pos = None
last_scroll = None
lines = []  # Store tuples (start_pos, end_pos, timestamp)
w=2
line_duration = 1  # Duration in seconds before lines disappear
line_clear_interval = 1  # Check every second
screen_color = (255,55,100)
current_time = pygame.time.get_ticks()
for _ in range(num_platform):
    platform = platforms()
    platform_group.add(platform)
for _ in range(num_ropes):
    rope = Ropes()
    ropes_group.add(rope)

background_image = pygame.image.load("images/back.png")
background_image = pygame.transform.scale(background_image, (1000,800))


def check_overlap(new_platform, group):
    hit_list = pygame.sprite.spritecollide(new_platform,group,False)
    if(len(hit_list)>0):
        return True
    return False

def infinite_generation():
    for rope in ropes_group:
        if(rope.rect.x-scroll[0]<-100) or (rope.rect.y - scroll[1]<-100):
            rope.destroy()
            ropes_group.remove(rope)
            
    for platform in platform_group:
        if(platform.rect.x - scroll[0] < -300) or (platform.rect.y - scroll[1]<-300):
            platform.destroy()
            platform_group.remove(platform)
    for enemy in enemy_group:
        if(enemy.rect.x - scroll[0] < -300) or (enemy.rect.y - scroll[1]<-300):
            enemy.destroy()
            enemy_group.remove(enemy)

    # if(len(ropes_group)<5):
    #     rope = Ropes()
    #     rope.rect.x+=true_scroll[0]+1000
    #     rope.rect.y += true_scroll[1] 
    #     ropes_group.add(rope)

    # if(len(platform_group)<num_platform):
    #     platform = platforms()
    #     platform.rect.x+=true_scroll[0]+1000
    #     platform.rect.y += true_scroll[1] 
    #     enem=enemies(platform.rect.x,platform.rect.top)
    #     enemy_group.add(enem)
    #     platform_group.add(platform)


    if len(platform_group) < num_platform:
        new_platform = platforms()
        new_platform.rect.x += true_scroll[0] + 1000
        new_platform.rect.y += true_scroll[1] +100
        # Check for overlap with existing platforms
        while check_overlap(new_platform, platform_group)or check_overlap(new_platform,ropes_group):
            new_platform.rect.x += 100
            new_platform.rect.y += 100
        platform_group.add(new_platform)
        if random.randint(0,3)==1:
            enem=enemies(new_platform.rect.x,new_platform.rect.top,new_platform.rect.topleft[0],new_platform.rect.topright[0])
            enemy_group.add(enem)
            platform_group.add(platform)
    if len(ropes_group) < 5:
        new_rope = Ropes()
        new_rope.rect.x +=true_scroll[0] + 1000
        new_rope.rect.y += true_scroll[1] 
        # Check for overlap with existing ropes
        while (check_overlap(new_rope, ropes_group) or check_overlap(new_rope,platform_group)):
            new_rope.rect.x += 10
            new_rope.rect.y += 10

        ropes_group.add(new_rope)

def enemy_check():
    hit_list = pygame.sprite.spritecollide(player,enemy_group,False)
    l=len(hit_list)
    if(l>0):
        # print("YES")
        player.fall_damage+=(0.1*l)


def move(rect,movement):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = pygame.sprite.spritecollide(player,platform_group,False)
    for tile in hit_list:
        # print(type(tile.rect))
        if movement[0] > 0:
            rect.right = tile.rectleft
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = pygame.sprite.spritecollide(player,ropes_group,False)
    for tile in hit_list:
        if movement[1] > 0:
            print("yes")
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

health_bar = HealthBar(50, 50, 200, 20, 100)
score_board = ScoreBoard(900, 50)

while True: 
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()
    # screen.fill(screen_color)
    screen.blit(background_image,(0,0))
    
    if event.type == pygame.MOUSEMOTION:
        if drawing:
            mouse_position = pygame.mouse.get_pos()
            if last_pos is not None:
                lines.append((last_pos, mouse_position, current_time, scroll, last_scroll))
            last_pos = mouse_position
            last_scroll = scroll
    elif event.type == pygame.MOUSEBUTTONUP:
        mouse_position = (0, 0)
        drawing = False
        last_pos = None
        last_scroll = None
    elif event.type == pygame.MOUSEBUTTONDOWN:
        drawing = True
    current_time = pygame.time.get_ticks()
    for line in lines:
        start_pos, end_pos, timestamp,old_scroll , last_old_scroll= line
        if (current_time - timestamp) / 1000 >= line_duration:
            lines.remove(line)
    # screen.fill(screen_color)  # Clear screen
    for line in lines:
        start_pos, end_pos, timestamp, old_scroll , last_old_scroll= line
        pygame.draw.line(screen, (255,255,255), (start_pos[0]+last_old_scroll[0]-scroll[0], start_pos[1]+last_old_scroll[1]-scroll[1]), (end_pos[0]+old_scroll[0]-scroll[0], end_pos[1]+old_scroll[1]-scroll[1]), w)
    # obstacle_group.draw(screen)
    true_scroll[0] += (player.rect.x-true_scroll[0]-400)/20
    true_scroll[1] += (player.rect.y-true_scroll[1]-300)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    player.update()
    health_bar.update_health(100-player.fall_damage)
    score_board.update_score(0.25)
    score_board.draw(screen)
    health_bar.draw(screen)
    # print(scroll[0])
    # print(scroll[0],end=" ")
    # print(player.rect.x,end=" ")
    # print(player.rect.x-scroll[0])
    # shift_back()
    # platform_group.draw(screen)   
    # platform_group.update()
    obstacle_group.update()
    enemy_group.update()
    # collision_sprite()
    
    infinite_generation()
    enemy_check()
    player_rect = player.rect.move(-scroll[0], -scroll[1])
    screen.blit(player.image, player_rect)
    for rope in ropes_group:
            rope_rect = rope.rect.move(-scroll[0], -scroll[1])
            screen.blit(rope.image, rope_rect)
    for platform in platform_group:
            platform_rect = platform.rect.move(-scroll[0], -scroll[1])
            screen.blit(platform.image, platform_rect) 
    for enemy in enemy_group:
        enemy_rect = enemy.rect.move(-scroll[0], -scroll[1])
        screen.blit(enemy.image, enemy_rect)  
    
    pygame.display.update() 
    clock.tick(60)      



    