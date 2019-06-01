import math ## We'll probably end up needing this eventually
import pygame
import functions

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

## Player states
FREE = 0 # walking or idle
PUNCH = 1 # punching

## Sounds - these are just placeholders
boop = pygame.mixer.Sound('boop.wav') # I'm told wav files work better than mp3's
kaboom = pygame.mixer.Sound('kaboom.wav')

## Fonts - not in use, but probably will be eventually
font1 = pygame.font.SysFont('timesnewroman', 24)

## ************************************

win = pygame.display.set_mode((winlength, winheight)) # creates the window

pygame.display.set_caption('Captain WiFi') # sets the window caption

map1 = pygame.Surface((maplength, mapheight))

camXpos = -100 # these should always be negative
camYpos = -100
camFollowRect = (200, 200, winlength - 400, winheight - 400)

activeParticles = [] ## Array of particle effects

class particle:
    ## This is a superclass. Don't actually use it. Use it's subclasses.
    def __init__(self, x, y, duration):
        self.x = x
        self.y = y
        self.duration = duration
    
    def draw(self):
        ## placeholder
        return
    
    def stop(self):
        ## some particles might need to do special things before being removed
        return

class punchParticle(particle):
    ## Subclass of particle
    def __init__(self, hero):
        self.duration = 10
        self.radius = 15
        self.colour = red
        self.owner = hero
        
        if hero.facing == NORTH:
            self.x = hero.x - self.radius
            self.y = hero.y - hero.radius - 2*self.radius
        elif hero.facing == EAST:
            self.x = hero.x + hero.radius
            self.y = hero.y - self.radius
        elif hero.facing == SOUTH:
            self.x = hero.x - self.radius
            self.y = hero.y + hero.radius
        else: # West
            self.x = hero.x - hero.radius - 2*self.radius
            self.y = hero.y - self.radius
        
        hero.state = PUNCH
    
    def draw(self):
        pygame.draw.rect(map1, self.colour, (self.x, self.y, 2*self.radius, 2*self.radius))
    
    def stop(self):
        self.owner.state = FREE

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
        angle = functions.angleTo(self.x, self.y, hero.x, hero.y)
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
        self.state = FREE
    
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
        ## Ensures the player can actually move
        if not(self.state == FREE):
            return
        self.y -= self.speed
        ## Might put camera stuff in a class/module/something eventually, 
        ## but for now it's global
        global camYpos        
        if (self.y - self.radius + camYpos <= camFollowRect[1] \
            and camYpos < 0):
            camYpos += self.speed
    
    def moveEast(self):
        if not(self.state == FREE):
            return        
        self.x += self.speed
        global camXpos
        if (self.x + self.radius + camXpos >= camFollowRect[0] + camFollowRect[2] \
            and camXpos > -maplength + winlength):
            camXpos -= self.speed
    
    def moveSouth(self):
        if not(self.state == FREE):
            return        
        self.y += self.speed
        global camYpos
        if (self.y + self.radius + camYpos >= camFollowRect[1] + camFollowRect[3] \
            and camYpos > -mapheight + winheight):
            camYpos -= self.speed
    
    def moveWest(self):
        if not(self.state == FREE):
            return        
        self.x -= self.speed
        global camXpos
        if (self.x - self.radius + camXpos <= camFollowRect[0] \
            and camXpos < 0):
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
    
    def punch(self):
        activeParticles.append(punchParticle(self))
            
def drawParticles():
    '''
    iterates through activeParticles, draws each one, and decreases their
    durations.
    '''
    ## removes dead particles
    i = 0
    while i < len(activeParticles):
        p = activeParticles[i]
        if p.duration <= 0:
            p.stop()
            activeParticles.pop(i)
            i -= 1
        else:
            p.duration -= 1
            p.draw()
        i += 1

## Main loop
captain = player(500, 400)
jelly = enemy(200, 200)

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
            if captain.state == FREE:
                boop.play()
                captain.punch()
        
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
    
    ## It looks a bit better if the player can't move or turn while punching
    if captain.state == FREE:
        captain.checkFacing()
    captain.draw()
    
    jelly.moveToward(captain)
    jelly.draw()
    
    drawParticles()
    
    # just a sec, I'm gonna try drawing a semitransparent circle
    s = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.circle(s, (100, 100, 255, 100), (100, 100), 100)
    map1.blit(s, (600, 600))    
    
    win.blit(map1, (camXpos, camYpos))
    
    ## Camera follow rect
    pygame.draw.rect(win, red, camFollowRect, 5)
    
    pygame.display.update() # put this at the end of your main loop

pygame.quit() # put this at the end of all your pygame files