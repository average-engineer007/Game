from numpy import sqrt
import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animated Stickman")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
# Stickman parameters
stickman_color = white
stickman_width = 2
# Stickman coordinates
head_radius = 20
head_x = screen_width // 2
head_y = screen_height // 4
torso_length = 81
torso_x = head_x
torso_y = head_y + head_radius
initial_arm_length = 50
arm_length = initial_arm_length
arm_x = torso_x
arm_y = torso_y + torso_length
upperArmLength = 0.4*torso_length
upperArm_x = torso_x
upperArm_y = torso_y
foreArmLength = upperArmLength
leg_length = 70
leg_x = torso_x
leg_y = torso_y + torso_length
tibia_length = torso_length/2
femur_length = torso_length/2
min_leg_angle = 45
max_leg_angle = 90
leg_angle = min_leg_angle
elevation = int((tibia_length+femur_length)/1.414)
# print('eleveation')
# print(elevation)
# Animation parameters


max_arm_angle = 60  # Maximum angle for arm rotation
min_arm_angle =0
min_rel_forearm_angle = 60
max_rel_forearm_angle = 90
min_rel_tibia_angle = 120
max_rel_tibia_angle = 180

rel_arm_angle = 60
foreArmAngle = -30

arm_speed = 0.05  # Speed of arm movement
# foreArmSpeed = (arm_speed*(max_forearm_angle-min_forearm_angle))/(max_arm_angle-min_arm_angle)
oscillation =0
# Main loop
upperArm_right = []
upperArm_left = []
foreArm_right = []
foreArm_left = []
femur_left = []
femur_right = []
tibia_left =[]
tibia_right =[]


while oscillation !=2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update arm angle
    rel_arm_angle -= arm_speed
    if rel_arm_angle >= max_arm_angle:
        arm_speed *= -1  # Reverse direction of arm movement when reaching the maximum angl
        oscillation+=1
    if rel_arm_angle < min_arm_angle:
        arm_speed*=-1
        oscillation+=1
    
    # foreArmAngle += foreArmSpeed
    # if foreArmAngle >= max_forearm_angle:
    #     foreArmSpeed *= -1  # Reverse direction of arm movement when reaching the maximum angl
    # if foreArmAngle < min_forearm_angle:
    #     foreArmSpeed*=-1

    # Clear the screen
    screen.fill(black)

    # Draw stickman
    pygame.draw.circle(screen, stickman_color, (head_x, head_y), head_radius, stickman_width)
    pygame.draw.line(screen, stickman_color, (torso_x, torso_y), (torso_x, torso_y + torso_length), stickman_width)

    #upper arm position calculations
    arm_angle = 90 - rel_arm_angle
    upperArm_x_right = upperArm_x + upperArmLength*math.cos(math.radians(arm_angle))
    upperArm_x_left = upperArm_x - upperArmLength*math.cos(math.radians(arm_angle))
    upperArm_y_right = upperArm_y + upperArmLength*math.sin(math.radians(arm_angle))
    upperArm_y_left = upperArm_y + upperArmLength*math.sin(math.radians(arm_angle))
    #fore arm position calculations

    foreArmAngle = math.radians((((max_rel_forearm_angle - min_rel_forearm_angle)/(max_arm_angle - min_arm_angle))+1)*(rel_arm_angle - min_arm_angle) + 90 - max_rel_forearm_angle + min_arm_angle)
    foreArm_x_right = upperArm_x_right - foreArmLength*math.cos(foreArmAngle)
    forerArm_y_right = upperArm_y_right + foreArmLength*math.sin(foreArmAngle)
    forerArm_x_left = upperArm_x_left - foreArmLength*math.cos(foreArmAngle)
    forerArm_y_left = upperArm_y_left - foreArmLength*math.sin(foreArmAngle)
    # print(math.degrees(foreArmAngle))
    #tibia position
    # print('ele')
    
    # femur_angle = math.acos((elevation/(2*math.cos(math.radians(90-arm_angle))))/femur_length) + math.radians(arm_angle)
    femur_x_right = leg_x+femur_length*math.cos(math.radians(arm_angle))
    femur_y_right = leg_y+femur_length*math.sin(math.radians(arm_angle))

    femur_x_left = leg_x - femur_length * math.cos(math.radians(arm_angle))
    femur_y_left = leg_y + femur_length * math.sin(math.radians(arm_angle))
    # print(math.cos(femur_angle))

    # tibiaAngle = math.radians((((max_rel_tibia_angle - min_rel_tibia_angle)/(max_arm_angle - min_arm_angle))+1)*(max_arm_angle-rel_arm_angle) + min_rel_tibia_angle - 90 - max_arm_angle)
    tibia_x_left = femur_x_left-tibia_length*math.cos(math.radians(2*arm_angle/3 + 30))
    tibia_y_left = femur_y_left+tibia_length*math.sin(math.radians(2*arm_angle/3 + 30))
    
    tibia_x_right = femur_x_right +tibia_length*math.cos(math.radians(2*arm_angle -90))
    tibia_y_right = femur_y_right + tibia_length*math.sin(math.radians(2*arm_angle -90))
    # print(math.degrees(tibiaAngle))
    # print(math.cos(math.radians(arm_angle/3 + 45)))

    

    # Draw upperarms
    pygame.draw.line(screen, stickman_color, (upperArm_x, upperArm_y), (upperArm_x_left, upperArm_y_left), stickman_width)
    pygame.draw.line(screen, stickman_color, (upperArm_x, upperArm_y), (upperArm_x_right, upperArm_y_right), stickman_width)

    pygame.draw.line(screen, stickman_color, (upperArm_x_left, upperArm_y_left), (forerArm_x_left, forerArm_y_left), stickman_width)
    # pygame.draw.line(screen, stickman_color, (upperArm_x_right, upperArm_y_right),(foreArm_x_right,forerArm_y_right), stickman_width)

    pygame.draw.line(screen, stickman_color, (leg_x, leg_y), (femur_x_left,femur_y_left), stickman_width)
    pygame.draw.line(screen, stickman_color, (femur_x_left,femur_y_left), (tibia_x_left,tibia_y_left), stickman_width)

    pygame.draw.line(screen, stickman_color, (leg_x, leg_y), (femur_x_right,femur_y_right), stickman_width)
    pygame.draw.line(screen, stickman_color, (femur_x_right,femur_y_right), (tibia_x_right,tibia_y_right), stickman_width)
    upperArm_left.append((upperArm_x_left,upperArm_y_left))
    upperArm_right.append((upperArm_x_right,upperArm_y_right))
    foreArm_right.append((foreArm_x_right,forerArm_y_right))
    foreArm_left.append((forerArm_x_left,forerArm_y_left))
    tibia_left.append((tibia_x_left,tibia_y_left))
    tibia_right.append((tibia_x_right,tibia_y_right))
    femur_left.append((femur_x_left,femur_y_left))
    femur_right.append((femur_x_right,femur_y_right))
    pygame.display.flip()
# print(upperArm_left)
# print(upperArm_right)
# print(foreArm_left)
# print(foreArm_right)
# print(tibia_left)
# print(tibia_right)
# print(femur_left)
# print(femur_right)
while True:
    for i in range(len(upperArm_left)) :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)
        pygame.draw.circle(screen, stickman_color, (head_x, head_y), head_radius, stickman_width)
        pygame.draw.line(screen, stickman_color, (torso_x, torso_y), (torso_x, torso_y + torso_length), stickman_width)
        pygame.draw.line(screen, stickman_color, (upperArm_x, upperArm_y), upperArm_left[i], stickman_width)
        pygame.draw.line(screen, stickman_color, (upperArm_x, upperArm_y), upperArm_right[i], stickman_width)

        pygame.draw.line(screen, stickman_color, upperArm_left[i], foreArm_left[i], stickman_width)
        pygame.draw.line(screen, stickman_color, upperArm_right[i], foreArm_right[i], stickman_width)

        pygame.draw.line(screen, stickman_color, (leg_x, leg_y), femur_left[i], stickman_width)
        pygame.draw.line(screen, stickman_color, femur_left[i], tibia_left[i], stickman_width)

        pygame.draw.line(screen, stickman_color, (leg_x, leg_y), femur_right[i], stickman_width)
        pygame.draw.line(screen, stickman_color, femur_right[i], tibia_right[i], stickman_width)
        pygame.display.flip()

