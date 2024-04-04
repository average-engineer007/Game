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
femur_length = 2*torso_length/3

min_leg_angle = 45
max_leg_angle = 90
leg_angle = min_leg_angle
elevation = int((tibia_length+femur_length)/1.414)
print('eleveation')
print(elevation)



# Animation parameters


max_arm_angle = 90  # Maximum angle for arm rotation
min_arm_angle =45
min_forearm_angle = -30
max_forearm_angle = 0

arm_angle = 45
foreArmAngle = -30

arm_speed = 0.05  # Speed of arm movement
foreArmSpeed = (arm_speed*(max_forearm_angle-min_forearm_angle))/(max_arm_angle-min_arm_angle)
# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update arm angle
    arm_angle += arm_speed
    if arm_angle >= max_arm_angle:
        arm_speed *= -1  # Reverse direction of arm movement when reaching the maximum angl
    if arm_angle < min_arm_angle:
        arm_speed*=-1
    foreArmAngle += foreArmSpeed
    if foreArmAngle >= max_forearm_angle:
        foreArmSpeed *= -1  # Reverse direction of arm movement when reaching the maximum angl
    if foreArmAngle < min_forearm_angle:
        foreArmSpeed*=-1

    # Clear the screen
    screen.fill(black)

    # Draw stickman
    pygame.draw.circle(screen, stickman_color, (head_x, head_y), head_radius, stickman_width)
    pygame.draw.line(screen, stickman_color, (torso_x, torso_y), (torso_x, torso_y + torso_length), stickman_width)

    # Calculate arm position based on the angle
    # arm_x_left = arm_x - initial_arm_length * math.cos(math.radians(arm_angle))
    # arm_x_right = arm_x + initial_arm_length * math.cos(math.radians(arm_angle))
    # arm_y_left = arm_y + initial_arm_length * math.sin(math.radians(arm_angle))
    # arm_y_right = arm_y - initial_arm_length * math.sin(math.radians(arm_angle))
    #upper arm position calculations
    upperArm_x_right = upperArm_x + upperArmLength*math.cos(math.radians(arm_angle))
    upperArm_x_left = upperArm_x - upperArmLength*math.cos(math.radians(arm_angle))
    upperArm_y_right = upperArm_y + upperArmLength*math.sin(math.radians(arm_angle))
    upperArm_y_left = upperArm_y + upperArmLength*math.sin(math.radians(arm_angle))
    #fore arm position calculations
    foreArm_x_right = upperArm_x_right + foreArmLength*math.cos(math.radians(foreArmAngle-(max_arm_angle-arm_angle)))
    forerArm_y_right = upperArm_y_right + foreArmLength*math.sin(math.radians(foreArmAngle-(max_arm_angle-arm_angle)))
    forerArm_x_left = upperArm_x_left + foreArmLength*math.cos(math.radians(foreArmAngle-(max_arm_angle-arm_angle)))
    forerArm_y_left = upperArm_y_left - foreArmLength*math.sin(math.radians(foreArmAngle-(max_arm_angle-arm_angle)))
    print(foreArmLength*math.sin(math.radians(foreArmAngle-(max_arm_angle-arm_angle))))

    #tibia position
    print('ele')
    
    femur_angle = math.acos((elevation/(2*math.cos(math.radians(90-arm_angle))))/femur_length) + math.radians(arm_angle)
    femur_x_right = leg_x+femur_length*math.cos(math.radians(arm_angle))
    femur_y_right = leg_y+femur_length*math.sin(math.radians(arm_angle))

    femur_x_left = leg_x - femur_length * math.cos(math.radians(arm_angle))
    femur_y_left = leg_y + femur_length * math.sin(math.radians(arm_angle))
    print(math.cos(femur_angle))
    tibia_x_left = leg_x-elevation/math.tan(math.radians(arm_angle))
    tibia_y_left = leg_y+elevation

    tibia_x_right = femur_x_right 
    tibia_y_right = femur_y_right + tibia_length
    

    # Draw upperarms
    pygame.draw.line(screen, stickman_color, (upperArm_x, upperArm_y), (upperArm_x_left, upperArm_y_left), stickman_width)
    pygame.draw.line(screen, stickman_color, (upperArm_x, upperArm_y), (upperArm_x_right, upperArm_y_right), stickman_width)

    pygame.draw.line(screen, stickman_color, (upperArm_x_left, upperArm_y_left), (forerArm_x_left, forerArm_y_left), stickman_width)
    pygame.draw.line(screen, stickman_color, (upperArm_x_right, upperArm_y_right),(foreArm_x_right,forerArm_y_right), stickman_width)

    pygame.draw.line(screen, stickman_color, (leg_x, leg_y), (femur_x_left,femur_y_left), stickman_width)
    pygame.draw.line(screen, stickman_color, (femur_x_left,femur_y_left), (tibia_x_left,tibia_y_left), stickman_width)

    pygame.draw.line(screen, stickman_color, (leg_x, leg_y), (femur_x_right,femur_y_right), stickman_width)
    pygame.draw.line(screen, stickman_color, (femur_x_right,femur_y_right), (tibia_x_right,tibia_y_right), stickman_width)


    # Update the display
    pygame.display.flip()
