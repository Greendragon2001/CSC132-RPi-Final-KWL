#######################################################Pre-game########################################################

#################Imports###################
import pygame
import os
##import RPi.GPIO as GPIO
import time
from random import randint
#################Imports###################

##################GPIO#####################
#sets GPIO pins as variables
TRIG = 24
ECHO = 12
LIGHT = 17
##################GPIO#####################

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
#window dimensions
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#bg in RGB
WHITE = (200, 200, 200)
# frames constant
FPS = 60
# scaling for game characters
WIDTH_CHARACTER, HEIGHT_CHARACTER = 100, 100
WIDTH_ENEMY, HEIGHT_ENEMY = 70, 70
#velocity
VELOCITY = 5
#################Constants#################

#######################################################Pre-game########################################################


##################################################Initalize all images##################################################

##########################Game essentials##########################
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
##########################Game essentials##########################

##########################PC CONTROLS##########################
# initialize the menu
#play button
PLAY_original = pygame.image.load(os.path.join('play.jpg'))
PLAY = pygame.transform.scale(PLAY_original, (100, 100))
#keyboard control button
KEYBOARD_original = pygame.image.load(os.path.join('arrows.PNG'))
KEYBOARD = pygame.transform.scale(KEYBOARD_original, (480, 480))
#mouse control button
MOUSE_original = pygame.image.load(os.path.join('mouse.PNG'))
MOUSE = pygame.transform.scale(MOUSE_original, (480, 480))
#controller control button
CONTROLLER_original = pygame.image.load(os.path.join('controller.PNG'))
CONTROLLER = pygame.transform.scale(CONTROLLER_original, (480, 480))
#dancepad control button
DANCE_original = pygame.image.load(os.path.join('dance_1.PNG'))
DANCE = pygame.transform.scale(DANCE_original, (480, 480))
##########################PC CONTROLS##########################

##########################PI CONTROLS##########################
###echo control button
##SONIC_original = pygame.image.load(os.path.join('sonic.jpg'))
##SONIC = pygame.transform.scale(SONIC_original, (200, 200))
###GPIO buttons control button
##BUTTON_original = pygame.image.load(os.path.join('buttons.jpg'))
##BUTTON = pygame.transform.scale(BUTTON_original, (200, 200))
###touch contol button
##TOUCH_original = pygame.image.load(os.path.join('touch.jpg'))
##TOUCH = pygame.transform.scale(TOUCH_original, (200, 200))
###move right button for touch
##RT_original = pygame.image.load(os.path.join('right_arrow.jpg'))
##RT = pygame.transform.scale(RT_original, (60, 50))
###move left button for touch
##LT_original = pygame.image.load(os.path.join('left_arrow.jpg'))
##LT = pygame.transform.scale(LT_original, (60, 50))
###jump button for touch
##JT_original = pygame.image.load(os.path.join('up_arrow.jpg'))
##JT = pygame.transform.scale(JT_original, (60, 50))
###light sensor control button
##PHOTO_original = pygame.image.load(os.path.join('light.jpg'))
##PHOTO = pygame.transform.scale(PHOTO_original, (200, 200))
##########################PI CONTROLS##########################

##################################################Initalize all images##################################################

########################################################Movement########################################################

##########################Non-player##########################
#enemy movement
def moveEnemy(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox):
    #import the emies movement speed
    global enemy1_speed
    global enemy2_speed
    global enemy3_speed
    # move the enemies
    enemy1_hitbox.x -= enemy1_speed
    enemy2_hitbox.x -= enemy2_speed
    enemy3_hitbox.x -= enemy3_speed
    # resest the enemies if they move off the screen
    if enemy1_hitbox.x < -300:
        enemy1_hitbox.x = 2000
        #randmize the ememies speed when it respawns
        enemy1_speed = randint (5, 24)
    if enemy2_hitbox.x < -300:
        enemy2_hitbox.x = 2000
        #randmize the ememies speed when it respawns
        enemy2_speed = randint(5, 24)
    if enemy3_hitbox.x < -300:
        enemy3_hitbox.x = 2000
        #randmize the ememies speed when it respawns
        enemy3_speed = randint(5, 24)
#background movement        
def backGround():
    global bgx
    # slowly move the background
    bgx -= 2
    #if the bacground moves too far to the left, it is respawned on the right
    # there are 3 backgrounds in constant rotation with each other
    if bgx <= -1920:
        bgx = 0
##########################Non-player##########################

############################Player############################
# keyboard
def keyboard_movement(keys_pressed, character_hitbox):
    global jump
    #JUMP
    # make sure the character is on the ground before allowing the player to jump again
    if keys_pressed[pygame.K_UP] and character_hitbox.y == 830:
        jump = 1
    #LEFT
    #the character cannt move past the left boundary
    if keys_pressed[pygame.K_LEFT] and character_hitbox.x > 0:
        character_hitbox.x -= VELOCITY
    #RIGHT
    #the character cannt move past the left boundary
    if keys_pressed[pygame.K_RIGHT] and character_hitbox.x < 1920:
        character_hitbox.x += VELOCITY
        
#mouse   
def mouse_movement(left, middle, right, character_hitbox):
    global jump
    #JUMP
    # make sure the character is on the ground before allowing the player to jump again
    if middle and character_hitbox.y == 830:
        jump = 1
    #LEFT
    #the character cannt move past the left boundary
    if left and character_hitbox.x > 0:
        character_hitbox.x -= VELOCITY
    #RIGHT
    #the character cannt move past the left boundary
    if right and character_hitbox.x < 1920:
        character_hitbox.x += VELOCITY
        
#controller        
def controller_movement(joystick, buttons, character_hitbox):
    global jump
    for i in range( buttons ):
        #JUMP
        button = joystick.get_button( i )
        #check if the button is pressed, and it it is the correct button
        if i == 0 and button == 1:
            # make sure the character is on the ground before allowing the player to jump again
            if character_hitbox.y == 830:
                jump = 1
        #LEFT
        if i == 4 and button == 1:
            #the character cannt move past the left boundary
            if character_hitbox.x > 0:
                character_hitbox.x -= VELOCITY
        #RIGHT
        if i == 5 and button == 1:
            #the character cannt move past the right boundary
            if character_hitbox.x < 1920:
                character_hitbox.x += VELOCITY
                
def dancepad_movement(joystick, buttons, character_hitbox):
    global jump
    for i in range( buttons ):
        #JUMP
        button = joystick.get_button( i )
        #check if the button is pressed, and it it is the correct button
        if i == 0 and button == 1:
            # make sure the character is on the ground before allowing the player to jump again
            if character_hitbox.y == 830:
                jump = 1
        #LEFT
        if i == 2 and button == 1:
            #the character cannt move past the left boundary
            if character_hitbox.x > 0:
                character_hitbox.x -= VELOCITY
        #RIGHT
        if i == 3 and button == 1:
            #the character cannt move past the right boundary
            if character_hitbox.x < 1920:
                character_hitbox.x += VELOCITY

##def Echo_movement(dist, character_hitbox):
##    global jump
    #LEFT
##    if dist > 0 and dist <= 15:
        #the character cannt move past the left boundary
##        if character_hitbox.x < 780:
##            character_hitbox.x += VELOCITY
    #JUMP
##    if dist > 15 and dist <= 30:
##        if character_hitbox.y == 300:
##            jump = 1
    #RIGHT
##    if dist > 30 and dist <= 45:
##        if character_hitbox.x > 0:
##            character_hitbox.x -= VELOCITY
##
##def button_movement(character_hitbox):
##    global jump
    #LEFT
##    if GPIO.input(18) == GPIO.LOW:
        #the character cannt move past the left boundary
##        if character_hitbox.x > 0:
##            character_hitbox.x -= VELOCITY
    #JUMP
##    if GPIO.input(19) == GPIO.LOW:
##        if character_hitbox.y == 300:
##            jump = 1
    #RIGHT
##    if GPIO.input(20) == GPIO.LOW:
##        if character_hitbox.x < 780:
##            character_hitbox.x += VELOCITY
##
# move left for touch screen
##def touch_left(character_hitbox):
##    global LEFT
##    global pressed
##    if LEFT == 1:
##        character_hitbox.x -= VELOCITY
##        if pressed == 0:
##            LEFT = 0
#move right for touch screen
##def touch_right(character_hitbox):
##    global RIGHT
##    global pressed
##    if RIGHT == 1:
##        character_hitbox.x += VELOCITY
##        if pressed == 0:
##            RIGHT = 0
##            
##def light_movement(count, character_hitbox):
##    global jump
    #JUMP
##    if count < 5 and character_hitbox.y == 300:
##        jump = 1
############################Player############################

##########################################Support functions##########################################
        
#######################Movement support#######################
# distance function for the sonic sensor
##def distance():
    # send out a pulse
##    GPIO.output(TRIG, GPIO.HIGH)
##    time.sleep(.00001)
    # stop sending pulse
##    GPIO.output(TRIG, GPIO.LOW)
    #set time as variables
##    Start_Time = time.time()
##    Stop_Time = time.time()
    # records the time it takes for the pulse to get back
##    while GPIO.input(ECHO) == 0:
##        Start_Time = time.time()
##
##    while GPIO.input(ECHO) == 1:
##        Stop_Time = time.time()
    # takes the time and uses it to calculate the distance traveled
##    ElapsedTime = Stop_Time - Start_Time
##
##    distance = (ElapsedTime * 34300) / 2
##
##    return distance

##def photo_time(LIGHT):
##    count = 0
    # starts charging a .1UF capacitor
##    GPIO.setup(LIGHT, GPIO.OUT)
##    GPIO.output(LIGHT, GPIO.LOW)
##    time.sleep(0.1)
    #switches to input and waits for the capacitor to charge
##    GPIO.setup(LIGHT, GPIO.IN)
    # once the capacitor is charged it will discharge and the total count will be returned
##    while GPIO.input(LIGHT) == GPIO.LOW:
##        count += 1
##
##    return count

# jump
def jumpUp(character_hitbox):
    global jump
    global jump_count
    global gravity
    # while the character is in the air they are affected by gravity
    if character_hitbox.y < 830:
        #slowly moves the character down
        character_hitbox.y += gravity
        
    if jump == 1:
        #the character will move uyp at a rate of 25 pixels per seconduntill the count reaches 20
        character_hitbox.y -= 25
        jump_count += 1
        if jump_count > 20:
            jump_count = 0
            jump = 0
#######################Movement support#######################

############################DEATH#############################
# resets the position of all game assets, cleans the GPIO pins, and prints the final score in the shell
def reset(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox, final_score):
    global enemy1_speed
    global enemy2_speed
    global enemy3_speed
    enemy1_speed = 5
    enemy2_speed = 5
    enemy3_speed = 5
    enemy1_hitbox.x = 2000
    enemy2_hitbox.x = 2600
    enemy3_hitbox.x = 3200
    #GPIO.cleanup()
    print(final_score)
############################DEATH#############################

############################LIFE##############################
def draw_window(character_hitbox, enemy1_hitbox, enemy2_hitbox, enemy3_hitbox):
    global bgx
    global image
    global control
    #color the window   
    WIN.fill(WHITE)
    #add in the background
    # there are three backgrounds that rotate with each other
    image = WIN.blit(BKGD, (bgx - 1919, 0))
    WIN.blit(BKGD, (bgx, 0))
    WIN.blit(BKGD, (bgx + 1919, 0))

    #images are classified as surfaces within pygame, .blit will draw the surface/image on the screen
    # blit is drawn as a rectangle starting at the top left
    # if I initalize an image at (0,0) only the tpo left will be at that point
    WIN.blit(CHARACTER, (character_hitbox.x, character_hitbox.y))
    # blit the enemies
    WIN.blit(ENEMY1, (enemy1_hitbox.x, enemy1_hitbox.y))
    WIN.blit(ENEMY2, (enemy2_hitbox.x, enemy2_hitbox.y))
    WIN.blit(ENEMY3, (enemy3_hitbox.x, enemy3_hitbox.y))
##    if control == 6:
##        WIN.blit(LT,(600,0))
##        WIN.blit(JT,(666,0))
##        WIN.blit(RT,(733,0))
    #refreshes the display with any new information that we draw for it
    pygame.display.update()
############################LIFE##############################
    
##########################################Support functions##########################################

############################################Main functions###########################################

############################GAME##############################
def main():
    #import global variables
    global button_pressed
    global jump
    global pressed
    global LEFT
    global RIGHT
    global control
    score = 0
    #make hitboxes for the character and the ememies
    #these are linked to the image locations so when the hitbox moves so deos the image
    character_hitbox = pygame.Rect(200, 830, WIDTH_CHARACTER, HEIGHT_CHARACTER)
    enemy1_hitbox = pygame.Rect(2000, 870, WIDTH_ENEMY, HEIGHT_ENEMY)
    enemy2_hitbox = pygame.Rect(2600, 870, WIDTH_ENEMY, HEIGHT_ENEMY)
    enemy3_hitbox = pygame.Rect(3200, 870, WIDTH_ENEMY, HEIGHT_ENEMY)

    
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
            # only the touch screen is coded as an event because we need the mouse location
            # we can only get the mouse location from the event.pos
##            if control == 6:
##                if event.type == pygame.MOUSEBUTTONDOWN:
##                    pressed = 1
##                    if event.pos[0] in range(600,666) and event.pos[1] in range(0,50):
##                        if character_hitbox.x > 0:
##                            LEFT = 1
##                    if event.pos[0] in range(667, 733) and event.pos[1] in range(0,50):
##                        if character_hitbox.y == 300:
##                            jump = 1
##                    if event.pos[0] in range(733, 800) and event.pos[1] in range(0,50):
##                        if character_hitbox.x < 780:
##                            RIGHT = 1
##                if event.type == pygame.MOUSEBUTTONUP:
##                    pressed = 0
            
                
                

        # if the character hitbox and enemy hitbox colide the game is reset and sent back to the start menu         
        if character_hitbox.colliderect(enemy1_hitbox):
            reset(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox, score)
            start()
        # if the character hitbox and enemy hitbox colide the game is reset and sent back to the start menu
        if character_hitbox.colliderect(enemy2_hitbox):
            reset(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox, score)
            start()
        # if the character hitbox and enemy hitbox colide the game is reset and sent back to the start menu
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
        # the buttons on the controller/ dance pad are assigned a value
        # 0-16 for controller, 0-9 for dance pad
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            buttons = joystick.get_numbuttons()
        #execute keyboard
        if control == 0:
            # calls for the keyboard_movement function if the player selected the keyboard in the input menu
            keyboard_movement(keys_pressed, character_hitbox)
            #checks if the player has jumped
            jumpUp(character_hitbox)
        #execute mouse
        if control == 1:
            # calls for the mouse_movement function if the player selected the mouse in the input menu
            mouse_movement(left, middle, right, character_hitbox)
            #checks if the player has jumped
            jumpUp(character_hitbox)
        #execute controller 
        if control == 2:
            # calls for the controller_movement function if the player selected the controller in the input menu
            controller_movement(joystick, buttons, character_hitbox)
            #checks if the player has jumped
            jumpUp(character_hitbox)
        #execute dancepad
        if control == 3:
            # calls for the dancepad_movement function if the player selected the dancepad in the input menu
            dancepad_movement(joystick, buttons, character_hitbox)
            #checks if the player has jumped
            jumpUp(character_hitbox)
##        # execute Echo
##        if control == 4:
            # calls for the Echo_movement function if the player selected the sonic sensor in the input menu
##            dist = distance()
##            if dist <= 60:
##                Echo_movement(dist, character_hitbox)
                #checks if the player has jumped
##                jumpUp(character_hitbox)
##        #execute Button
##        if control == 5:
            # calls for the button_movement function if the player selected the buttons in the input menu
##            button_movement(character_hitbox)
            #checks if the player has jumped
##            jumpUp(character_hitbox)
##        # execute touch
##        if control == 6:
            # calls for the touch_movement function if the player selected the hand in the input menu
##            touch_left(character_hitbox)
##            touch_right(character_hitbox)
            #checks if the player has jumped
##            jumpUp(character_hitbox)
##        #execute photo_resistor
##        if control == 7:
            # calls for the light_movement function if the player selected the lightbulb in the input menu
##            count = photo_time(LIGHT)
##            light_movement(count, character_hitbox)
            #checks if the player has jumped
##            jumpUp(character_hitbox)
            

 
  
        #create the window
        # increments the score every time the menu is executed(60 times per second
        score += 1
        pygame.display.set_caption("Score: {}".format(score))
        # calls for the enemies to move
        moveEnemy(enemy1_hitbox, enemy2_hitbox, enemy3_hitbox)
        #calls for the background to move
        backGround()
        # creats the window, character, enemies, and background as well as updates the display
        draw_window(character_hitbox, enemy1_hitbox, enemy2_hitbox, enemy3_hitbox)
############################GAME##############################
        
#######################Input Selection########################
def menu():
    global control
    running = True
    while running:
        #restes the score to 0 on death
        pygame.display.set_caption("Score: {}".format(0))
        # the game, input_menu, and start menu all share the same backgound
        # the background for the input_menu and start menu do not move
        # add the background to the window
        WIN.blit(BKGD, (0, 0))
        #line 1
        # add the input images to the window
        WIN.blit(KEYBOARD, (0,300))
        WIN.blit(MOUSE,(480,300))
        WIN.blit(CONTROLLER, (960,300))
        WIN.blit(DANCE, (1440,300))
        #line 2
##        WIN.blit(SONIC, (0,200))
##        WIN.blit(BUTTON, (200,200))
##        WIN.blit(TOUCH, (400, 200))
##        WIN.blit(PHOTO, (600, 200))
        
        # create invisible/pseudo-buttons so the player can select their input
        for event in pygame.event.get():
            #chose the input
            if event.type == pygame.MOUSEBUTTONDOWN:
                #keyboard
                if event.pos[0] in range(0,480) and event.pos[1] in range(300,780):
                    # chages the control variable so the program knows what input the player wants to use
                    control = 0
                    # starts the main function
                    main()
                #mouse
                if event.pos[0] in range(480, 960) and event.pos[1] in range(300,780):
                    # chages the control variable so the program knows what input the player wants to use
                    control = 1
                    # starts the main function
                    main()
                #controller
                if event.pos[0] in range(961, 1440) and event.pos[1] in range(300,780):
                    # chages the control variable so the program knows what input the player wants to use
                    control = 2
                    # starts the main function
                    main()
                #dancepad
                if event.pos[0] in range(1441, 1920) and event.pos[1] in range(300,780):
                    # chages the control variable so the program knows what input the player wants to use
                    control = 3
                    # starts the main function
                    main()
                
##                #Echo
##                if event.pos[0] in range(0, 200) and event.pos[1] in range(201,400):
##                    control = 4
##                    GPIO.setmode(GPIO.BCM)
##                    GPIO.setup(TRIG, GPIO.OUT)
##                    GPIO.setup(ECHO, GPIO.IN)
##                    main()
##                #buttons
##                if event.pos[0] in range (201, 400) and event.pos[1] in range(201,400):
##                    control = 5
##                    GPIO.setmode(GPIO.BCM)
##                    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##                    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##                    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##                    main()
##                # touch
##                if event.pos[0] in range(401, 600) and event.pos[1] in range(201,400):
##                    control = 6
##                    main()
##                # photoresistor
##                if event.pos[0] in range(601, 800) and event.pos[1] in range(201,400):
##                    control = 7
##                    GPIO.setmode(GPIO.BCM)
##                    main()
            #closes the window when x is pressed
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                exit()
        #updates the display
        # we need to update the display anytime we try to add anything to it
        pygame.display.update()
#######################Input Selection########################
        
#########################Start menu###########################
def start():
    running = True
    while running:
        # adds the background
        WIN.blit(BKGD,(0,0))
        # adds a playbutton in the center of the window
        WIN.blit(PLAY,(900, 500))
        #closes the window when x is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                exit()
            # if the player clicks on the button they will be taken to the input menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(900, 1000) and event.pos[1] in range(500,600):
                    menu()
        # update the display
        pygame.display.update()
#########################Start menu###########################        
#start the program   
    
start()

############################################Main functions###########################################
