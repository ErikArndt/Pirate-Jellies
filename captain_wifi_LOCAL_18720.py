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
## I recently found out t4hose were built in, so might as well use them

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
HURT = 2 # just been damaged

## Sounds - these are just placeholders
boop = pygame.mixer.Sound('boop.wav') # I'm told wav files work better than mp3's
kaboom = pygame.mixer.Sound('kaboom.wav')

## Fonts - not in use, but probably will be eventually
font1 = pygame.font.SysFont('timesnewroman', 24)

## ************************************

win = pygame.display.set_mode((winlength, winheight)) # creates the window

pygame.display.set_caption('Captain WiFi') # sets the window caption

## ******************* IMAGES *************
## I need to put them here after defining win

idles = [pygame.image.load('images/idleU1.png').convert_alpha(), \
         pygame.image.load('images/idleU2.png').convert_alpha(),
         pygame.image.load('images/idleR1.png').convert_alpha(),
         pygame.image.load('images/idleR2.png').convert_alpha(),
         pygame.image.load('images/idleD1.png').convert_alpha(),
         pygame.image.load('images/idleD2.png').convert_alpha(),
         pygame.image.load('images/idleL1.png').convert_alpha(),
         pygame.image.load('images/idleL2.png').convert_alpha()]
for i in range(len(idles)):
    idles[i] = pygame.transform.scale(idles[i], (50, 125))

## ****************************************

map1 = pygame.Surface((maplength, mapheight))

camXpos = -100 # these should always be negative
camYpos = -100
camFollowRect = (200, 200, winlength - 400, winheight - 400)

class wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(map1, black, (self.x, self.y, self.width, self.height), 0)

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
    ## Subclass of particle. It also contains functions for damaging enemies.
    def __init__(self, hero):
        self.duration = 10
        self.radius = 15
        self.colour = red
        self.owner = hero
        self.damage = 1
        
        if hero.facing == NORTH:
            self.x = hero.x - self.radius
            self.y = hero.y - hero.yRad - 2*self.radius
        elif hero.facing == EAST:
            self.x = hero.x + hero.xRad
            self.y = hero.y - self.radius
        elif hero.facing == SOUTH:
            self.x = hero.x - self.radius
            self.y = hero.y + hero.yRad
        else: # West
            self.x = hero.x - hero.xRad - 2*self.radius
            self.y = hero.y - self.radius
        
        hero.state = PUNCH
    
    def draw(self):
        pygame.draw.rect(map1, self.colour, (self.x, self.y, 2*self.radius, 2*self.radius))
    
    def stop(self):
        self.owner.state = FREE
    
    def checkDamage(enemies):
        ## TODO
        return

class enemy:
    ## superclass for all enemy types
    def __init__(self, startingX, startingY):
        self.x = startingX
        self.y = startingY
        self.health = 1 # default value, different for specific enemies
    
    def draw(self):
        ## placeholder
        return

    def hurt(self):
        ## placeholder
        return

class jelly(enemy):
    def __init__(self, startingX, startingY):
        '''
        Enemies must be initialized with starting x and y coordinates.
        '''
        self.x = startingX
        self.y = startingY
        self.xRad = 20
        self.yRad = 20
        
        self.speedCap = 5
        self.accel = 0.1
        self.xSpeed = 0
        self.ySpeed = 0
        self.xAccel = 0
        self.yAccel = 0
        
        self.state = FREE
        self.damage = 1
        self.health = 3
        self.animTimers = {
            'hurt': 0,
        }
    
    def draw(self):
        pygame.draw.rect(map1, yellow, (self.x - self.xRad, self.y - self.yRad, \
                                        self.xRad*2, self.yRad*2))
        ## Do something different if damaged
    
    def moveToward(self, hero):
        '''
        moves the enemy toward the given player (i.e. captain). Yes, this is
        actually physics.
        Note: This does not check the enemy's state to see if it is allowed to
        move or not.
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
        if self.xSpeed > 0:
            for i in range(len(walls)):
                if functions.checkCollision((walls[i].x, walls[i].y), (walls[i].x, walls[i].y+walls[i].height),\
                                  (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 1, self.xSpeed):
                    self.x = walls[i].x - self.xRad
                    self.xSpeed = 0
                    break
        elif self.xSpeed < 0:
            for i in range(len(walls)):
                if functions.checkCollision((walls[i].x+walls[i].width, walls[i].y), (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                                  (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 3, -self.xSpeed):
                    self.x = walls[i].x + walls[i].width + self.xRad
                    self.xSpeed = 0
                    break
        self.y += self.ySpeed
        if self.ySpeed < 0:
            for i in range(len(walls)):
                if functions.checkCollision((walls[i].x, walls[i].y+walls[i].height), (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                                  (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 0, -self.ySpeed):
                    self.y = walls[i].y + walls[i].height + self.yRad
                    self.ySpeed = 0
                    break
        elif self.ySpeed > 0:
            for i in range(len(walls)):
                if functions.checkCollision((walls[i].x, walls[i].y), (walls[i].x+walls[i].width, walls[i].y),\
                                  (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 2, self.ySpeed):
                    self.y = walls[i].y - self.yRad
                    self.ySpeed = 0
                    break
            
        self.x = round(self.x)
        self.y = round(self.y)
    
    def hurt(self, damage):
        '''
        Call when enemy is damaged. Parameter is the amount of damage the enemy
        took.
        '''
        ## TODO: write this
        return

class player:
    def __init__(self, startingX, startingY):
        '''
        Player must be initialized with starting x and y coordinates.
        '''
        self.x = startingX
        self.y = startingY
        self.facing = NORTH
        self.speed = 3
        self.xRad = 25
        self.yRad = 50
        
        self.health = 4
        self.state = FREE
        self.animTimers = {
            'idle': 0 # 0 means animation is not playing, positive means it's playing
        }
    
    def draw(self):
        '''
        Draws the player character
        '''
        ## Green hitbox indicator
        pygame.draw.rect(map1, green, (self.x - self.xRad, self.y - self.yRad, \
                                      self.xRad*2, self.yRad*2))
        ## For now I'm just using the basic idle sprites
        if self.facing == NORTH:
            map1.blit(idles[0], (self.x - self.xRad, self.y - self.yRad - 25))
        elif self.facing == EAST:
            map1.blit(idles[2], (self.x - self.xRad, self.y - self.yRad - 25))
        elif self.facing == SOUTH:
            map1.blit(idles[4], (self.x - self.xRad, self.y - self.yRad - 25))
        elif self.facing == WEST:
            map1.blit(idles[6], (self.x - self.xRad, self.y - self.yRad - 25))
        else:
            print('Error: player is not facing a valid direction.')
            running = False
    
    def moveNorth(self):
        ## Ensures the player can actually move
        if not(self.state == FREE):
            return
        self.y -= self.speed

        ## Collision stuffs
        for i in range(len(walls)):
            if functions.checkCollision((walls[i].x, walls[i].y+walls[i].height), (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                              (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 0, self.speed):
                self.y = walls[i].y + walls[i].height + self.yRad
                break
        else: # Camera movement only happens if there are no wall collisions
        
            ## Might put camera stuff in a class/module/something eventually, 
            ## but for now it's global
            global camYpos        
            if (self.y - self.yRad + camYpos <= camFollowRect[1] \
                and camYpos < 0):
                camYpos += self.speed

    def moveEast(self):
        if not(self.state == FREE):
            return        
        self.x += self.speed
        for i in range(len(walls)):
            if functions.checkCollision((walls[i].x, walls[i].y), (walls[i].x, walls[i].y+walls[i].height),\
                              (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 1, self.speed):
                self.x = walls[i].x - self.xRad
                break
        else:
            global camXpos
            if (self.x + self.xRad + camXpos >= camFollowRect[0] + camFollowRect[2] \
                and camXpos > -maplength + winlength):
                camXpos -= self.speed
    
    def moveSouth(self):
        if not(self.state == FREE):
            return        
        self.y += self.speed
        for i in range(len(walls)):
            if functions.checkCollision((walls[i].x, walls[i].y), (walls[i].x+walls[i].width, walls[i].y),\
                              (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 2, self.speed):
                self.y = walls[i].y - self.yRad
                break
        else:
            global camYpos
            if (self.y + self.yRad + camYpos >= camFollowRect[1] + camFollowRect[3] \
                and camYpos > -mapheight + winheight):
                camYpos -= self.speed
    
    def moveWest(self):
        if not(self.state == FREE):
            return        
        self.x -= self.speed
        for i in range(len(walls)):
            if functions.checkCollision((walls[i].x+walls[i].width, walls[i].y), (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                              (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 3, self.speed):
                self.x = walls[i].x + walls[i].width + self.xRad
                break
        else:
            global camXpos
            if (self.x - self.xRad + camXpos <= camFollowRect[0] \
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
captain = player(600, 600)

enemies = []
jelly1 = jelly(200, 200)
## TODO: Change this so it adds jelly1 to the list

walls = [wall(300, 200, 300, 200),
         wall(0, 0, 1000, 2),
         wall(0, 0, 2, 1000),
         wall(1000, 0, 2, 1000),
         wall(0, 1000, 1000, 2),
         ]

activeParticles = [] ## Array of particle effects

running = True
while running:
    pygame.time.delay(10) ## apparently this helps with inputs
    
    pygame.draw.rect(win, black, (0, 0, winlength, winheight))
    pygame.draw.rect(map1, white, (0, 0, maplength, mapheight)) # draws the background
    
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

    pygame.draw.rect(map1, blue, (200, 250, 100, 150)) # random rect on the map
    
    for i in range(len(walls)):
        walls[i].draw()    
    
    ## It looks a bit better if the player can't move or turn while punching
    if captain.state == FREE:
        captain.checkFacing()
    captain.draw()
    
    ## TODO: Iterate through enemies list
    jelly1.moveToward(captain)
    jelly1.draw()
    
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
