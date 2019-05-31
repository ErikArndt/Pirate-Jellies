import math ## We'll probably end up needing this eventually
import pygame
import angles

pygame.mixer.pre_init(22050, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

## ********** CONSTANTS ***************
white = pygame.Color('white')
black = pygame.Color('black')
red = pygame.Color('red')
blue = pygame.Color('blue')
green = pygame.Color('green')
yellow = pygame.Color('yellow')
## I recently found out those were built in, so might as well use them

winheight = 600
winlength = 800
mapheight = 1000
maplength = 1000

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

## Game states - not in use, but will be eventually
PLAYING = 0
MAINMENU = 1
PAUSED = 2

## Sounds - these are just placeholders
boop = pygame.mixer.Sound('boop.wav') # I'm told wav files work better than mp3's
kaboom = pygame.mixer.Sound('kaboom.wav')

## Fonts - not in use, but probably will be eventually
font1 = pygame.font.SysFont('timesnewroman', 24)

## ************************************

win = pygame.display.set_mode((winlength, winheight)) # creates the window

pygame.display.set_caption('Captain WiFi') # sets the window caption

map1 = pygame.Surface((maplength, mapheight))

camTracking = True # must be set before class definitions
camXpos = -100 # these should always be negative
camYpos = -100

class enemy:
    ## Will probably have to rework this once we get multiple enemy types
    def __init__(self, startingX, startingY):
        '''
        Enemies must be initialized with starting x and y coordinates.
        '''
        self.x = startingX
        self.y = startingY
        self.radius = 20
        self.speedCap = 5
        self.accel = 0.1
        self.xSpeed = 0
        self.ySpeed = 0
        self.xAccel = 0
        self.yAccel = 0
    
    def draw(self):
        pygame.draw.circle(map1, red, (self.x, self.y), self.radius)
    
    def moveToward(self, hero):
        '''
        moves the enemy toward the given player (i.e. captain). Yes, this is
        actually physics.
        '''
        angle = angles.angleTo(self.x, self.y, hero.x, hero.y)
        self.xAccel = self.accel * math.cos(math.radians(angle))
        self.yAccel = self.accel * math.sin(math.radians(angle))
        self.xSpeed += self.xAccel
        self.ySpeed += self.yAccel
        
        ## cap the enemy's speed
        curSpeed = math.sqrt(self.xSpeed * self.xSpeed + self.ySpeed * self.ySpeed)
        if (curSpeed > self.speedCap):
            scaleFactor = curSpeed / self.speedCap
            self.xSpeed /= scaleFactor
            self.ySpeed /= scaleFactor
        
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.x = round(self.x)
        self.y = round(self.y)

class player:
    def __init__(self, startingX, startingY):
        '''
        Player must be initialized with starting x and y coordinates.
        '''
        self.x = startingX
        self.y = startingY
        self.facing = NORTH
        self.speed = 3
        self.radius = 25
    
    def draw(self):
        '''
        Draws the player character
        '''
        pygame.draw.rect(map1, green, (self.x - self.radius, self.y - self.radius, \
                                      self.radius*2, self.radius*2))
        ## black line to indicate facing
        if self.facing == NORTH:
            pygame.draw.line(map1, black, (self.x, self.y), (self.x, self.y - self.radius), 2)
        elif self.facing == EAST:
            pygame.draw.line(map1, black, (self.x, self.y), (self.x + self.radius, self.y), 2)
        elif self.facing == SOUTH:
            pygame.draw.line(map1, black, (self.x, self.y), (self.x, self.y + self.radius), 2)
        elif self.facing == WEST:
            pygame.draw.line(map1, black, (self.x, self.y), (self.x - self.radius, self.y), 2)
        else:
            print('Error: player is not facing a valid direction.')
            running = False
    
    def moveNorth(self):
        self.y -= self.speed
        if camTracking:
            ## Might put camera stuff in a class/module/something eventually, 
            ## but for now it's global
            global camYpos
            camYpos += self.speed
    
    def moveEast(self):
        self.x += self.speed
        if camTracking:
            global camXpos
            camXpos -= self.speed
    
    def moveSouth(self):
        self.y += self.speed
        if camTracking:
            global camYpos
            camYpos -= self.speed
    
    def moveWest(self):
        self.x -= self.speed
        if camTracking:
            global camXpos
            camXpos += self.speed
        
    def checkFacing(self):
        '''
        checks where the mouse is and updates the facing property
        '''
        ## once again, camera is just global for now
        global camXpos
        global camYpos
        mouseX = pygame.mouse.get_pos()[0] - camXpos
        mouseY = pygame.mouse.get_pos()[1] - camYpos
        
        Xdist = abs(mouseX - self.x)
        Ydist = abs(mouseY - self.y)
        
        if Ydist >= Xdist and self.y >= mouseY:
            self.facing = NORTH
        elif Ydist >= Xdist:
            self.facing = SOUTH
        elif Ydist < Xdist and self.x <= mouseX:
            self.facing = EAST
        else:
            self.facing = WEST

## Main loop
captain = player(500, 400)
jelly = enemy(200, 200)
print(camYpos)

running = True
while running:
    pygame.time.delay(10) ## apparently this helps with inputs
    
    pygame.draw.rect(win, black, (0, 0, winlength, winheight))
    pygame.draw.rect(map1, white, (0, 0, maplength, mapheight)) # draws the background
    
    pygame.draw.rect(map1, blue, (200, 250, 100, 150)) # random rect on the map
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # what happens when X is pressed
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 32: # what happens when space is pressed
                ## idk maybe space can be a pause button
                print("Space doesn't do anything ya dingus")
                
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): # left mouse button
            boop.play()
        
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3): # right mouse button
            kaboom.play()
     
    keys = pygame.key.get_pressed() # keys is a giant array of booleans
    if keys[pygame.K_w]:
        captain.moveNorth()
    if keys[pygame.K_d]:
        captain.moveEast()
    if keys[pygame.K_s]:
        captain.moveSouth()
    if keys[pygame.K_a]:
        captain.moveWest()
    ## Don't use elifs, or else diagonal mvmt won't be possible
    
    captain.checkFacing()
    captain.draw()
    
    jelly.moveToward(captain)
    jelly.draw()
    
    # just a sec, I'm gonna try drawing a semitransparent circle
    s = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.circle(s, (100, 100, 255, 100), (100, 100), 100)
    map1.blit(s, (600, 600))    
    
    win.blit(map1, (camXpos, camYpos))
    
    ## Camera follow rect
    pygame.draw.rect(win, red, (200, 200, winlength - 400, winheight - 400), 5)
    
    pygame.display.update() # put this at the end of your main loop

pygame.quit() # put this at the end of all your pygame files