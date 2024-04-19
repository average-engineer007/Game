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
        pygame.draw.rect(self.image, border_color, (0, 0, image_width, image_height), border_width)
        
        
        self.gravity=0
        self.player_index=0
        self.x_pos=self.rect.x
        self.y_pos=self.rect.y
        self.move_x=0
        self.move_y=0
        self.line_collision = False
        self.fall_damage=0
        self.speed = 5
    
    def above(self,start_point, end_point):
        v1 = (end_point[0]- start_point[0], end_point[1] - start_point[1])
        v2 = (self.rect.x+self.rect.width/2- start_point[0], self.rect.y+self.rect.height - start_point[1])
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]
        above = False
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
        print(self.fall_damage)
        # terminal velocity
        if(self.gravity>0.16):
            self.gravity=0.16
        keys=pygame.key.get_pressed()

        if keys[pygame.K_UP] :
            self.move_y=-5
            self.gravity=-0.2
        elif keys[pygame.K_DOWN] :
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
                self.rect.top = tile.rect.bottom
                self.move_y = 0
                bottom_platform=True

        # collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        if keys[pygame.K_RIGHT] :
            self.move_x=5
        elif keys[pygame.K_LEFT] :
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
                    self.fall_damage+=1
                self.move_x = tangent_x * self.speed
                self.move_y = -tangent_y * self.speed
            else:                
                tangent_x, tangent_y = self.calculate_tangent_vector(avg_start_pos, avg_end_pos)
               
                self.move_x = tangent_x * self.speed
                self.move_y = tangent_y * self.speed
            

        
    def update(self):
        
        # self.rect.x=self.x_pos -scroll_x
        # self.rect.y=self.y_pos  - scroll_y
        self.player_movement()
        # self.stickman.draw(player.rect.x, player.rect.y)
        # if(self.rect.x>1000):
        #     self.rect.x-=1000
        #     true_scroll[0]-=1000

        # self.x_pos=self.rect.x+scroll_x
        # self.y_pos=self.rect.y+scroll_y
        
        # self.apply_gravity()
        # self.animate()

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
        self.image.fill('RED')
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


def check_overlap(new_platform, group):
    hit_list = pygame.sprite.spritecollide(new_platform,platform_group,False)
    if(len(hit_list)>0):
        return True
    return False

def infinite_generation():
    for rope in ropes_group:
        if(rope.rect.x-scroll[0]<-30) or (rope.rect.y - scroll[1]<-30):
            rope.destroy()
            ropes_group.remove(rope)
            
    for platform in platform_group:
        if(platform.rect.x - scroll[0] < -300) or (platform.rect.y - scroll[1]<-300):
            platform.destroy()
            platform_group.remove(platform)

    if(len(ropes_group)<3):
        rope = Ropes()
        rope.rect.x+=true_scroll[0]+1000
        rope.rect.y += true_scroll[1] 
        ropes_group.add(rope)

    if(len(platform_group)<num_platform):
        platform = platforms()
        platform.rect.x+=true_scroll[0]+1000
        platform.rect.y += true_scroll[1] 
        platform_group.add(platform)

    if len(ropes_group) < 5:
        new_rope = Ropes()
        new_rope.rect.x += true_scroll[0] + 1000
        new_rope.rect.y += true_scroll[1] 
        # Check for overlap with existing ropes
        while check_overlap(new_rope, ropes_group):
            new_rope = Ropes()
            new_rope.rect.x += true_scroll[0] + 1000
            new_rope.rect.y += true_scroll[1] 
        ropes_group.add(new_rope)

    if len(platform_group) < num_platform:
        new_platform = platforms()
        new_platform.rect.x += true_scroll[0] + 1000
        new_platform.rect.y += true_scroll[1] 
        # Check for overlap with existing platforms
        new_platform = platforms()
        while check_overlap(new_platform, platform_group):
            new_platform.rect.x +=  + 1000
            new_platform.rect.y += +100
        platform_group.add(new_platform)




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

while True: 
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill(screen_color)
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
    screen.fill(screen_color)  # Clear screen
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
    # print(scroll[0],end=" ")
    # print(player.rect.x,end=" ")
    # print(player.rect.x-scroll[0])
    # shift_back()
    # platform_group.draw(screen)   
    # platform_group.update()
    obstacle_group.update()
    # collision_sprite()
    infinite_generation()

    player_rect = player.rect.move(-scroll[0], -scroll[1])
    screen.blit(player.image, player_rect)
    for rope in ropes_group:
            rope_rect = rope.rect.move(-scroll[0], -scroll[1])
            screen.blit(rope.image, rope_rect)
    for platform in platform_group:
            platform_rect = platform.rect.move(-scroll[0], -scroll[1])
            screen.blit(platform.image, platform_rect)  
    player.speed+=0.0001
    pygame.display.update() 
    clock.tick(60)      



    