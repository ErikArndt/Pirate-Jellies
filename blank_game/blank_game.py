import math ## We'll probably end up needing this eventually
import pygame

## Don't worry about understanding these. You need the third one at the top of 
## every file that uses pygame, and the first two at the top of every file that
## plays sounds.
pygame.mixer.pre_init(22050, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

## ********** CONSTANTS ***************
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 50, 50)
blue = (0, 0, 255)

winheight = 600
winlength = 800

## Jim states
STOPPED = 0
WALKING = 1

## Sounds
boop = pygame.mixer.Sound('boop.wav') # I'm told wav files work better than mp3's

## Images
jimIdle = pygame.image.load('jim_pose1.png')
jimPoses = [pygame.image.load('jim_pose1.png'), pygame.image.load('jim_pose2.png'), \
            pygame.image.load('jim_pose3.png'), pygame.image.load('jim_pose4.png'), \
            pygame.image.load('jim_pose5.png'), pygame.image.load('jim_pose6.png'), \
            pygame.image.load('jim_pose7.png'), pygame.image.load('jim_pose8.png')]
## For animations, it helps to make an array of images

## ************************************

win = pygame.display.set_mode((winlength, winheight)) # creates the window

pygame.display.set_caption('Waddup ma dudes') # sets the window caption


## How to draw a rectangle

pygame.draw.rect(win, red, (100, 150, 200, 70))


## How to write text

font1 = pygame.font.SysFont('timesnewroman', 24)
space_text = font1.render('Press space to boop', False, white)
win.blit(space_text, (300, 500))

click_text1 = font1.render('Click here to', False, blue)
click_text_stopped = font1.render('make Jim walk', False, blue)
click_text_walking = font1.render('make Jim stop', False, blue)
# I'll blit these later, in the main loop


## How to display images
## See line 27 for how to load images

# I just realized the images are the wrong size. 
jimIdle = pygame.transform.scale(jimIdle, (round(jimIdle.get_size()[0] / 2.5), \
                                           round(jimIdle.get_size()[1] / 2.5)))
# I probably should have resized the image earlier with ms paint or something
# but oh well.
win.blit(jimIdle, (500 - jimIdle.get_size()[0] / 2,0))

## Shoot, I'm gonna have to resize all the other images, too. Just a sec.
for i in range(len(jimPoses)):
    jimPoses[i] = pygame.transform.scale(jimPoses[i], (round(jimPoses[i].get_size()[0] / 2.5), \
                                                       round(jimPoses[i].get_size()[1] / 2.5)))
## Okay, we good now.


## Main loop

jim_state = STOPPED # flips between STOPPED and WALKING
walk_count = 0 # used for animating Jim's walk
time_between_frames = 6 # controls speed of animation

running = True
while running:
    pygame.time.delay(10) ## apparently this helps with inputs
    
    pygame.draw.rect(win, black, (0, 0, winlength, winheight))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # what happens when X is pressed
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 32: # what happens when space is pressed
                
                # how to play sounds
                boop.play()
                # see line 24 for how to load sounds
                
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): # left mouse button
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            
            if (100 <= mouse_x and mouse_x <= 300 and 150 <= mouse_y and \
                mouse_y <= 220): # what happens when red button is clicked
                if jim_state == STOPPED:
                    jim_state = WALKING
                    walk_count = 0
                elif jim_state == WALKING:
                    jim_state = STOPPED
                else:
                    print('There was an error.')
    
    win.blit(space_text, (300, 500))
    pygame.draw.rect(win, red, (100, 150, 200, 70))    
    win.blit(click_text1, (100, 150))   
    
    if jim_state == STOPPED:
        win.blit(click_text_stopped, (100, (150 + click_text1.get_height()))) 
        win.blit(jimIdle, (500 - jimIdle.get_size()[0] / 2,0))
    elif jim_state == WALKING:
        win.blit(click_text_walking, (100, (150 + click_text1.get_height())))
        
        if walk_count >= 8 * time_between_frames:
            walk_count = 0
        jim_current_pose = jimPoses[walk_count // time_between_frames]
        win.blit(jim_current_pose, (500 - jim_current_pose.get_size()[0] / 2, 0))
        walk_count +=1
            
    pygame.display.update() # put this at the end of your main loop

pygame.quit() # put this at the end of all your pygame files