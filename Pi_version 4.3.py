import pygame
import os
import RPi.GPIO as GPIO
import time
from time import sleep
from random import randint
##################GPIO#####################
#GPIO.setmode(GPIO.BCM)
TRIG = 24
ECHO = 12
LIGHT = 17



#################Constants#################
#background
bgx = 0

#jump
jump = 0
gravity = 5
jump_count = 0

#enemy
enemy1_speed = 5
enemy2_speed = 5
enemy3_speed = 5

#inputs
control = 0
button_pressed = 4
pygame.init()
pygame.joystick.init()
LEFT = 0
RIGHT = 0
pressed = 0
#################Constants#################

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Score: {}".format(score))

#bg in RGB
WHITE = (200, 200, 200)
# frams constant
FPS = 60
# scaling for game characters
WIDTH_CHARACTER, HEIGHT_CHARACTER = 50, 50
WIDTH_ENEMY, HEIGHT_ENEMY = 30, 30
#velocity
VELOCITY = 5

# initialize the character as an image
CHARACTER_original = pygame.image.load(os.path.join('character.jpg'))
#CHARACTER_resized = pygame.transform.rotate(pygame.transform.scale(CHARACTER, (SCALE_WIDTH, SCALE_HEIGHT)), 90)
#.rotate to change image angle, .scale to change image size
CHARACTER = pygame.transform.scale(CHARACTER_original, (WIDTH_CHARACTER, HEIGHT_CHARACTER))
# initialize the background
BKGD_original = pygame.image.load(os.path.join('background.jpg'))
BKGD = pygame.transform.scale(BKGD_original, (WIDTH, HEIGHT))
# initialze the enemy
ENEMY1_original = pygame.image.load(os.path.join('enemy.jpg'))
ENEMY1 = pygame.transform.scale(ENEMY1_original, (WIDTH_ENEMY, HEIGHT_ENEMY))
ENEMY2_original = pygame.image.load(os.path.join('enemy.jpg'))
ENEMY2 = pygame.transform.scale(ENEMY2_original, (WIDTH_ENEMY, HEIGHT_ENEMY))
ENEMY3_original = pygame.image.load(os.path.join('enemy.jpg'))
ENEMY3 = pygame.transform.scale(ENEMY3_original, (WIDTH_ENEMY, HEIGHT_ENEMY))
# initialize the menu
#play button
PLAY_original = pygame.image.load(os.path.join('play.jpg'))
PLAY = pygame.transform.scale(PLAY_original, (50, 50))
#move right button for touch
RT_original = pygame.image.load(os.path.join('right_arrow.jpg'))
RT = pygame.transform.scale(RT_original, (60, 50))
#move left button for touch
LT_original = pygame.image.load(os.path.join('left_arrow.jpg'))
LT = pygame.transform.scale(LT_original, (60, 50))
#jump button for touch
JT_original = pygame.image.load(os.path.join('up_arrow.jpg'))
JT = pygame.transform.scale(JT_original, (60, 50))
#keyboard control button
KEYBOARD_original = pygame.image.load(os.path.join('arrows.jpg'))
KEYBOARD = pygame.transform.scale(KEYBOARD_original, (200, 200))
#mouse control button
MOUSE_original = pygame.image.load(os.path.join('mouse.jpg'))
MOUSE = pygame.transform.scale(MOUSE_original, (200, 200))
#controller control button
CONTROLLER_original = pygame.image.load(os.path.join('controller.jpg'))
CONTROLLER = pygame.transform.scale(CONTROLLER_original, (200, 200))
#dancepad control button
DANCE_original = pygame.image.load(os.path.join('dance.jpg'))
DANCE = pygame.transform.scale(DANCE_original, (200, 200))
#echo control button
SONIC_original = pygame.image.load(os.path.join('sonic.jpg'))
SONIC = pygame.transform.scale(SONIC_original, (200, 200))
#GPIO buttons control button
BUTTON_original = pygame.image.load(os.path.join('buttons.jpg'))
BUTTON = pygame.transform.scale(BUTTON_original, (200, 200))
#touch contol button
TOUCH_original = pygame.image.load(os.path.join('touch.jpg'))
TOUCH = pygame.transform.scale(TOUCH_original, (200, 200))
#light sensor control button
PHOTO_original = pygame.image.load(os.path.join('light.jpg'))
PHOTO = pygame.transform.scale(PHOTO_original, (200, 200))


def moveEnemy(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox):
    global enemy1_speed
    global enemy2_speed
    global enemy3_speed
    enemy1_hitbox.x -= enemy1_speed
    enemy2_hitbox.x -= enemy2_speed
    enemy3_hitbox.x -= enemy3_speed
    if enemy1_hitbox.x < -300:
        enemy1_hitbox.x = 1450
        enemy1_speed = randint (5, 18)
    if enemy2_hitbox.x < -300:
        enemy2_hitbox.x = 1450
        enemy2_speed = randint(5, 18)
    if enemy3_hitbox.x < -300:
        enemy3_hitbox.x = 1450
        enemy3_speed = randint(5, 18)

def keyboard_movement(keys_pressed, character_hitbox):
    global jump
    #JUMP
    if keys_pressed[pygame.K_UP] and character_hitbox.y == 300:
        jump = 1
    #LEFT
    if keys_pressed[pygame.K_LEFT] and character_hitbox.x > 0:
        character_hitbox.x -= VELOCITY
    #RIGHT
    if keys_pressed[pygame.K_RIGHT] and character_hitbox.x < 780:
        character_hitbox.x += VELOCITY
            
def mouse_movement(left, middle, right, character_hitbox):
    global jump
    #JUMP
    if middle and character_hitbox.y == 300:
        jump = 1
    #LEFT
    if left and character_hitbox.x > 0:
        character_hitbox.x -= VELOCITY
    #RIGHT
    if right and character_hitbox.x < 780:
        character_hitbox.x += VELOCITY
        

def controller_movement(joystick, buttons, character_hitbox):
    global jump
    for i in range( buttons ):
        button = joystick.get_button( i )
        if i == 0 and button == 1:
            if character_hitbox.y == 300:
                jump = 1
        if i == 4 and button == 1:
            if character_hitbox.x > 0:
                character_hitbox.x -= VELOCITY
        if i == 5 and button == 1:
            if character_hitbox.x < 780:
                character_hitbox.x += VELOCITY
                
def dancepad_movement(joystick, buttons, character_hitbox):
    global jump
    for i in range( buttons ):
        button = joystick.get_button( i )
        if i == 0 and button == 1:
            if character_hitbox.y == 300:
                jump = 1
        if i == 2 and button == 1:
            if character_hitbox.x > 0:
                character_hitbox.x -= VELOCITY
        if i == 3 and button == 1:
            if character_hitbox.x < 780:
                character_hitbox.x += VELOCITY

def Echo_movement(dist, character_hitbox):
    global jump
    if dist > 0 and dist <= 20:
        if character_hitbox.x > 0:
            character_hitbox.x -= VELOCITY      
    if dist > 20 and dist <= 40:
        if character_hitbox.y == 300:
            jump = 1
    if dist > 40 and dist <= 60:
        if character_hitbox.x < 780:
            character_hitbox.x += VELOCITY

def button_movement(character_hitbox):
    global jump
    if GPIO.input(18) == GPIO.LOW:
        if character_hitbox.x > 0:
            character_hitbox.x -= VELOCITY
    if GPIO.input(19) == GPIO.LOW:
        if character_hitbox.y == 300:
            jump = 1
    if GPIO.input(20) == GPIO.LOW:
        if character_hitbox.x < 780:
            character_hitbox.x += VELOCITY
            
def light_movement(count, character_hitbox):
    global jump
    if count < 5 and character_hitbox.y == 300:
        jump = 1


def distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(.00001)
    GPIO.output(TRIG, GPIO.LOW)
    Start_Time = time.time()
    Stop_Time = time.time()

    while GPIO.input(ECHO) == 0:
        Start_Time = time.time()

    while GPIO.input(ECHO) == 1:
        Stop_Time = time.time()

    ElapsedTime = Stop_Time - Start_Time

    distance = (ElapsedTime * 34300) / 2

    return distance

def photo_time(LIGHT):
    count = 0
    GPIO.setup(LIGHT, GPIO.OUT)
    GPIO.output(LIGHT, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(LIGHT, GPIO.IN)

    while GPIO.input(LIGHT) == GPIO.LOW:
        count += 1

    return count



 
def jumpUp(character_hitbox):
    global jump
    global jump_count
    global gravity
    if character_hitbox.y < 300:
        character_hitbox.y += gravity
    if jump == 1:
        character_hitbox.y -= 15
        jump_count += 2
        if jump_count > 20:
            jump_count = 0
            jump = 0

def touch_left(character_hitbox):
    global LEFT
    global pressed
    if LEFT == 1:
        character_hitbox.x -= VELOCITY
        if pressed == 0:
            LEFT = 0
def touch_right(character_hitbox):
    global RIGHT
    global pressed
    if RIGHT == 1:
        character_hitbox.x += VELOCITY
        if pressed == 0:
            RIGHT = 0

def reset(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox, final_score):
    global enemy1_speed
    global enemy2_speed
    global enemy3_speed
    enemy1_speed = 5
    enemy2_speed = 5
    enemy3_speed = 5
    enemy1_hitbox.x = 1400
    enemy2_hitbox.x = 1800
    enemy3_hitbox.x = 2200
    GPIO.cleanup()
    print(final_score)

def backGround():
    global bgx
    bgx -= 2
    if bgx <= -800:
        bgx = 0

def draw_window(character_hitbox, enemy1_hitbox, enemy2_hitbox, enemy3_hitbox):
    global bgx
    global image
    global control
    #color the window   
    WIN.fill(WHITE)
    #add in the background
    image = WIN.blit(BKGD, (bgx - 800, 0))
    WIN.blit(BKGD, (bgx, 0))
    WIN.blit(BKGD, (bgx + 800, 0))

    #images are classified as surfaces within pygame, .blit with draw the surface/image on the screen
    WIN.blit(CHARACTER, (character_hitbox.x, character_hitbox.y))
    # blit the enemies
    WIN.blit(ENEMY1, (enemy1_hitbox.x, enemy1_hitbox.y))
    WIN.blit(ENEMY2, (enemy2_hitbox.x, enemy2_hitbox.y))
    WIN.blit(ENEMY3, (enemy3_hitbox.x, enemy3_hitbox.y))
    if control == 6:
        WIN.blit(LT,(600,0))
        WIN.blit(JT,(666,0))
        WIN.blit(RT,(733,0))
    #refreshes the display with any new information that we draw for ita
    pygame.display.update()


def main():
    global button_pressed
    global jump
    global pressed
    global LEFT
    global RIGHT
    global control
    global enemy1_speed
    global enemy2_speed
    global enemy3_speed
    score = 0 
    character_hitbox = pygame.Rect(200, 300, WIDTH_CHARACTER, HEIGHT_CHARACTER)
    enemy1_hitbox = pygame.Rect(1400, 330, WIDTH_ENEMY, HEIGHT_ENEMY)
    enemy2_hitbox = pygame.Rect(1800, 330, WIDTH_ENEMY, HEIGHT_ENEMY)
    enemy3_hitbox = pygame.Rect(2200, 330, WIDTH_ENEMY, HEIGHT_ENEMY)

    
    running = True
    #limits the display refresh to staballize game variance 
    clock = pygame.time.Clock()
    
    while running:
        # display update will never exceed the defined FPS
        clock.tick(FPS)
        #reads all pygame events
        for event in pygame.event.get():
            #closes the window when x is pressed
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                exit()
            if control == 6:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressed = 1
                    if event.pos[0] in range(600,666) and event.pos[1] in range(0,50):
                        if character_hitbox.x > 0:
                            LEFT = 1
                    if event.pos[0] in range(667, 733) and event.pos[1] in range(0,50):
                        if character_hitbox.y == 300:
                            jump = 1
                    if event.pos[0] in range(733, 800) and event.pos[1] in range(0,50):
                        if character_hitbox.x < 780:
                            RIGHT = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    pressed = 0
            
                
                

                    
        if character_hitbox.colliderect(enemy1_hitbox):
            #pygame.display.quit()
            reset(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox, score)
            start()
        if character_hitbox.colliderect(enemy2_hitbox):
            reset(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox, score)
            start()
        if character_hitbox.colliderect(enemy3_hitbox):
            reset(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox, score)
            start()
                
            #INPUT
        # initalize keyboard
        keys_pressed = pygame.key.get_pressed()
        # initalize mouse
        left, middle, right = pygame.mouse.get_pressed()
        # initalize controller/dancepad
        joystick_count = pygame.joystick.get_count()
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            buttons = joystick.get_numbuttons()
        #execute keyboard
        if control == 0:
            keyboard_movement(keys_pressed, character_hitbox)
            jumpUp(character_hitbox)
        #execute mouse
        if control == 1:
            mouse_movement(left, middle, right, character_hitbox)
            jumpUp(character_hitbox)
        #execute controller 
        if control == 2:
            controller_movement(joystick, buttons, character_hitbox)
            jumpUp(character_hitbox)
        #execute dancepad
        if control == 3:
            dancepad_movement(joystick, buttons, character_hitbox)
            jumpUp(character_hitbox)
        # execute Echo
        if control == 4:
            dist = distance()
            if dist <= 100:
                Echo_movement(dist, character_hitbox)
                jumpUp(character_hitbox)
        #execute Button
        if control == 5:
            button_movement(character_hitbox)
            jumpUp(character_hitbox)
        # execute touch
        if control == 6:
            touch_left(character_hitbox)
            touch_right(character_hitbox)
            jumpUp(character_hitbox)
        #execute photo_resistor
        if control == 7:
            count = photo_time(LIGHT)
            light_movement(count, character_hitbox)
            jumpUp(character_hitbox)
            

 
  
        #create the window

        score += 1
        pygame.display.set_caption("Score: {}".format(score))
        moveEnemy(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox)
        backGround()
        
        draw_window(character_hitbox, enemy1_hitbox, enemy2_hitbox, enemy3_hitbox)
def menu():
    global control
    running = True
    while running:
        #global bgx
        pygame.display.set_caption("Score: {}".format(0))
        WIN.blit(BKGD, (0, 0))
        #line 1
        WIN.blit(KEYBOARD, (0,0))
        WIN.blit(MOUSE,(200,0))
        WIN.blit(CONTROLLER, (400,0))
        WIN.blit(DANCE, (600,0))
        #line 2
        WIN.blit(SONIC, (0,200))
        WIN.blit(BUTTON, (200,200))
        WIN.blit(TOUCH, (400, 200))
        WIN.blit(PHOTO, (600, 200))
        for event in pygame.event.get():
            #chose the input
            if event.type == pygame.MOUSEBUTTONDOWN:
                #keyboard
                if event.pos[0] in range(0,200) and event.pos[1] in range(0,200):
                    control = 0
                    main()
                #mouse
                if event.pos[0] in range(201, 400) and event.pos[1] in range(0,200):
                    control = 1
                    main()
                #controller
                if event.pos[0] in range(401, 600) and event.pos[1] in range(0,200):
                    control = 2
                    main()
                #dancepad
                if event.pos[0] in range(601, 800) and event.pos[1] in range(0,200):
                    control = 3
                    main()
                
                #Echo
                if event.pos[0] in range(0, 200) and event.pos[1] in range(201,400):
                    control = 4
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(TRIG, GPIO.OUT)
                    GPIO.setup(ECHO, GPIO.IN)
                    main()
                #buttons
                if event.pos[0] in range (201, 400) and event.pos[1] in range(201,400):
                    control = 5
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    main()
                # touch
                if event.pos[0] in range(401, 600) and event.pos[1] in range(201,400):
                    control = 6
                    main()
                # photoresistor
                if event.pos[0] in range(601, 800) and event.pos[1] in range(201,400):
                    control = 7
                    GPIO.setmode(GPIO.BCM)
                    main()
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                exit()
        pygame.display.update()

def start():
    running = True
    while running:
        WIN.blit(BKGD,(0,0))
        WIN.blit(PLAY,(370, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                exit()
            #cstart the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(370, 420) and event.pos[1] in range(150,200):
                    menu()
        pygame.display.update()
        
    
    
start()

