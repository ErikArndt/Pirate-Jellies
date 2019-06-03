import math
import pygame
import functions
import maps
import enemies
import collision
import menu

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

winlength = 800
winheight = 600

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

## Game states
PLAYING = 0
MENU = 1
PAUSED = 2

## Player states
FREE = 0 # walking or idle
PUNCH = 1 # punching
BEAM = 2 # shooting beam
DIE = 3 # playing the death animation

## Sounds - these are just placeholders
boop = pygame.mixer.Sound('boop.wav') # I'm told wav files work better than mp3's
kaboom = pygame.mixer.Sound('kaboorn.wav')

## Fonts
font1 = pygame.font.SysFont('timesnewroman', 24) # Currently only used for FPS

## ************************************

win = pygame.display.set_mode((winlength, winheight)) # creates the window

pygame.display.set_caption('Captain WiFi') # sets the window caption

## ******************* IMAGES *************
## I need to put them here after defining win

idles = [pygame.image.load('images/idleU1.png').convert_alpha(),
         pygame.image.load('images/idleU2.png').convert_alpha(),
         pygame.image.load('images/idleR1.png').convert_alpha(),
         pygame.image.load('images/idleR2.png').convert_alpha(),
         pygame.image.load('images/idleD1.png').convert_alpha(),
         pygame.image.load('images/idleD2.png').convert_alpha(),
         pygame.image.load('images/idleL1.png').convert_alpha(),
         pygame.image.load('images/idleL2.png').convert_alpha()]

punchPoses = [pygame.image.load('images/punchU1.png').convert_alpha(),
           pygame.image.load('images/punchU2.png').convert_alpha(),
           pygame.image.load('images/punchR1.png').convert_alpha(),
           pygame.image.load('images/punchR2.png').convert_alpha(),
           pygame.image.load('images/punchD1.png').convert_alpha(),
           pygame.image.load('images/punchD2.png').convert_alpha(),
           pygame.image.load('images/punchL1.png').convert_alpha(),
           pygame.image.load('images/punchL2.png').convert_alpha()]

walkPoses = [pygame.image.load('images/walkU1.png').convert_alpha(),
         pygame.image.load('images/walkU2.png').convert_alpha(),
         pygame.image.load('images/walkR1.png').convert_alpha(),
         pygame.image.load('images/walkD1.png').convert_alpha(),
         pygame.image.load('images/walkD2.png').convert_alpha(),
         pygame.image.load('images/walkL1.png').convert_alpha()]

healthBattery = [pygame.image.load('images/battery0.png').convert_alpha(),
                 pygame.image.load('images/battery1.png').convert_alpha(),
                 pygame.image.load('images/battery2.png').convert_alpha(),
                 pygame.image.load('images/battery3.png').convert_alpha(),
                 pygame.image.load('images/battery4.png').convert_alpha(),
                 pygame.image.load('images/battery5.png').convert_alpha(),
                 pygame.image.load('images/battery6.png').convert_alpha(),
                 pygame.image.load('images/battery7.png').convert_alpha(),
                 pygame.image.load('images/battery8.png').convert_alpha(),
                 pygame.image.load('images/battery9.png').convert_alpha(),
                 pygame.image.load('images/battery10.png').convert_alpha()]

for i in range(len(idles)):
    idles[i] = pygame.transform.scale(idles[i], (50, 125))
for i in range(len(punchPoses)):
    punchPoses[i] = pygame.transform.scale(punchPoses[i], (50, 125))
for i in range(len(walkPoses)):
    walkPoses[i] = pygame.transform.scale(walkPoses[i], (50, 125))
for i in range(len(healthBattery)):
    healthBattery[i] = pygame.transform.scale(healthBattery[i], (200, 100))

punches = [pygame.image.load('images/punch1.png').convert_alpha(), \
           pygame.image.load('images/punch2.png').convert_alpha()]
punches[0] = pygame.transform.scale(punches[0], (60, 60))
punches[1] = pygame.transform.scale(punches[1], (80, 80))
## I probably shouldn't hard code those numbers, but whatever

beams = [pygame.image.load('images/beam1.png').convert_alpha(), \
         pygame.image.load('images/beam2.png').convert_alpha()]
beams[0] = pygame.transform.scale(beams[0], (80, 200))
beams[1] = pygame.transform.scale(beams[1], (80, 400))
beams.extend([pygame.transform.scale(beams[0], (20, 200)),
              pygame.transform.scale(beams[1], (20, 400))])
## 80 was arrived at through trial and error.
## If you change it here, change beamParticle.width as well

enemies.loadSprites()
maps.loadSprites()
menu.loadSprites((winlength, winheight))

## ****************************************

level = 1 # This will be mutated
maplength = maps.mapSizes[level][0]
mapheight = maps.mapSizes[level][1]
currentMap = pygame.Surface((maplength, mapheight))

camXpos, camYpos = maps.camStartpoints[level]
camFollowRect = (200, 200, winlength - 400, winheight - 400)

class Particle:
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

class PunchParticle(Particle):
    ## Subclass of particle. It also contains functions for damaging enemies.
    def __init__(self, hero, wifi):
        self.duration = 10
        self.radius = 20
        self.colour = red # just for hitbox, will eventually remove
        self.owner = hero
        self.powered = wifi
        self.owner.particle = self
        self.damage = 1
        if self.powered:
            self.damage = 2
            self.radius = 30
            self.colour = blue
        
        ## these coordinates are for the top left corner
        if hero.facing == NORTH:
            self.x = hero.x - self.radius
            self.y = hero.y - hero.yRad - 2*self.radius - 20
        elif hero.facing == EAST:
            self.x = hero.x + hero.xRad + 20
            self.y = hero.y - self.radius
        elif hero.facing == SOUTH:
            self.x = hero.x - self.radius
            self.y = hero.y + hero.yRad + 20
        else: # West
            self.x = hero.x - hero.xRad - 2*self.radius - 20
            self.y = hero.y - self.radius
        
        hero.state = PUNCH
    
    def draw(self):
        ## hitbox
        if debug:
            pygame.draw.rect(currentMap, self.colour, (self.x, self.y, 2*self.radius, 2*self.radius))
        currentMap.blit(punches[self.powered], (self.x - 10, self.y - 10))
        ## I used a boolean to index a list, which is sketchy but it looks so cool
        ## False becomes 0, True becomes 1
    
    def stop(self):
        self.owner.state = FREE
    
    def checkDamage(self, enemyList):
        '''
        Checks whether the particle intersects with any enemies. Runs the hurt
        method on any enemies that were hit.
        '''
        for e in enemyList:
            if collision.rects((self.x, self.y, \
                                        2*self.radius, 2*self.radius), \
                                       (e.x - e.xRad, e.y - e.yRad, 2*e.xRad, 2*e.yRad)):
                if e.state == FREE: ## Might need to add more states
                    e.hurt(self.damage)
        return

class BeamParticle(Particle):
    def __init__(self, hero, wifi):
        self.x1 = hero.x
        self.y1 = hero.y
        mouseX = pygame.mouse.get_pos()[0] - camXpos
        mouseY = pygame.mouse.get_pos()[1] - camYpos
        self.length = 200
        self.width = 40
        self.angle = functions.angleTo(self.x1, self.y1, mouseX, mouseY)        
        self.duration = 20
        self.colour = red
        self.powered = wifi
        self.owner = hero
        self.damage = 1
        if self.powered:
            self.damage = 2
            self.length = 400
            self.colour = blue

        self.x2 = self.x1 + math.cos(self.angle*math.pi/180)*self.length
        self.y2 = self.y1 + math.sin(self.angle*math.pi/180)*self.length

        hero.state = BEAM

    def draw(self):
        ## debug Hitline:
        if debug:
            pygame.draw.line(currentMap, self.colour, (self.x1, self.y1), (self.x2, self.y2), 10)
        
        if self.duration >= 10:
            self.width = 10
            b = pygame.transform.rotate(beams[self.powered + 2], -1*(self.angle - 90))
        else: 
            self.width = 40
            b = pygame.transform.rotate(beams[self.powered], -1*(self.angle - 90))                        
        
        if self.angle >= 270: # NE
            angle = -1*self.angle
            beamX = self.x1 - self.width * math.sin(math.radians(angle))
            beamY = self.y2 - self.width * math.cos(math.radians(angle))
        elif self.angle >= 180: # NW
            angle = self.angle - 180
            beamX = self.x2 - self.width * math.sin(math.radians(angle))
            beamY = self.y2 - self.width * math.cos(math.radians(angle))
        elif self.angle >= 90: # SW
            angle = 180 - self.angle
            beamX = self.x2 - self.width * math.sin(math.radians(angle))
            beamY = self.y1 - self.width * math.cos(math.radians(angle))
        else: ## SE
            angle = self.angle
            beamX = self.x1 - self.width * math.sin(math.radians(angle))
            beamY = self.y1 - self.width * math.cos(math.radians(angle))
        currentMap.blit(b, (beamX, beamY))


    def stop(self):
        self.owner.state = FREE
    
    def checkDamage(self, enemyList):
        for e in enemyList:
            if functions.checkRectWithLine((self.x1, self.y1), (self.x2, self.y2),\
                                           (e.x - e.xRad, e.y - e.yRad, 2*e.xRad, 2*e.yRad)) != (-1, -1):
                if e.state == FREE:
                    e.hurt(self.damage)
        return

class player:
    def __init__(self, startingPos):
        '''
        Player must be initialized with starting x and y coordinates.
        '''
        self.x = startingPos[0]
        self.y = startingPos[1]
        self.facing = NORTH
        self.speed = 4
        self.xRad = 25
        self.yRad = 50
        self.isMoving = False
        self.particle = 0 # will point to a punch/beam particle
        
        self.health = 10
        self.state = FREE
        self.iFrames = 60
        self.animTimers = {
            'idle': 0, # 0 means animation is not playing, positive means it's playing
            'hurt': 0,
            'walk': 0
        }
        self.connected = False
    
    def draw(self):
        '''
        Draws the player character
        '''
        ## Hitbox indicator
        if debug:
            if self.connected:
                pygame.draw.rect(currentMap, blue, (self.x - self.xRad, self.y - self.yRad, \
                                              self.xRad*2, self.yRad*2))  
            else:
                pygame.draw.rect(currentMap, green, (self.x - self.xRad, self.y - self.yRad, \
                                              self.xRad*2, self.yRad*2))
        if self.state == FREE and not self.isMoving:
            if self.animTimers['idle'] <30:
                if self.facing == NORTH:
                    currentMap.blit(idles[1], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == EAST:
                    currentMap.blit(idles[3], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == SOUTH:
                    currentMap.blit(idles[5], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == WEST:
                    currentMap.blit(idles[7], (self.x - self.xRad, self.y - self.yRad - 25))
                else:
                    print('Error: player is not facing a valid direction.')
                    running = False
            else:
                if self.facing == NORTH:
                    currentMap.blit(idles[0], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == EAST:
                    currentMap.blit(idles[2], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == SOUTH:
                    currentMap.blit(idles[4], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == WEST:
                    currentMap.blit(idles[6], (self.x - self.xRad, self.y - self.yRad - 25))
                else:
                    print('Error: player is not facing a valid direction.')
                    running = False
        #walking animations
        elif self.state == FREE:
            if self.animTimers['walk'] <= 0:
                self.animTimers['walk'] = 80
            else:
                if self.animTimers['walk'] < 20 or (self.animTimers['walk'] < 60 and self.animTimers['walk'] >=40):
                    if self.facing == NORTH:
                        currentMap.blit(idles[1], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == EAST:
                        currentMap.blit(idles[3], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == SOUTH:
                        currentMap.blit(idles[5], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == WEST:
                        currentMap.blit(idles[7], (self.x - self.xRad, self.y - self.yRad - 25))
                    else:
                        print('Error: player is not facing a valid direction.')
                        running = False
                elif self.animTimers['walk'] >= 60:
                    if self.facing == NORTH:
                        currentMap.blit(walkPoses[0], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == EAST:
                        currentMap.blit(walkPoses[2], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == SOUTH:
                        currentMap.blit(walkPoses[3], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == WEST:
                        currentMap.blit(walkPoses[5], (self.x - self.xRad, self.y - self.yRad - 25))
                    else:
                        print('Error: player is not facing a valid direction.')
                        running = False
                elif self.animTimers['walk'] < 40 and self.animTimers['walk'] >= 20:
                    if self.facing == NORTH:
                        currentMap.blit(walkPoses[1], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == EAST:
                        currentMap.blit(walkPoses[2], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == SOUTH:
                        currentMap.blit(walkPoses[4], (self.x - self.xRad, self.y - self.yRad - 25))
                    elif self.facing == WEST:
                        currentMap.blit(walkPoses[5], (self.x - self.xRad, self.y - self.yRad - 25))
                    else:
                        print('Error: player is not facing a valid direction.')
                        running = False
                self.animTimers['walk'] -= 1
        elif self.state == PUNCH:
            if self.particle.duration >= 6:
                if self.facing == NORTH:
                    currentMap.blit(punchPoses[0], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == EAST:
                    currentMap.blit(punchPoses[2], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == SOUTH:
                    currentMap.blit(punchPoses[4], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == WEST:
                    currentMap.blit(punchPoses[6], (self.x - self.xRad, self.y - self.yRad - 25))
                else:
                    print('Error: player is not facing a valid direction.')
                    running = False
            else:
                if self.facing == NORTH:
                    currentMap.blit(punchPoses[1], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == EAST:
                    currentMap.blit(punchPoses[3], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == SOUTH:
                    currentMap.blit(punchPoses[5], (self.x - self.xRad, self.y - self.yRad - 25))
                elif self.facing == WEST:
                    currentMap.blit(punchPoses[7], (self.x - self.xRad, self.y - self.yRad - 25))
                else:
                    print('Error: player is not facing a valid direction.')
                    running = False
        elif self.state == BEAM:
            if self.facing == NORTH:
                currentMap.blit(punchPoses[1], (self.x - self.xRad, self.y - self.yRad - 25))
            elif self.facing == EAST:
                currentMap.blit(punchPoses[3], (self.x - self.xRad, self.y - self.yRad - 25))
            elif self.facing == SOUTH:
                currentMap.blit(punchPoses[5], (self.x - self.xRad, self.y - self.yRad - 25))
            elif self.facing == WEST:
                currentMap.blit(punchPoses[7], (self.x - self.xRad, self.y - self.yRad - 25))
            else:
                print('Error: player is not facing a valid direction.')
                running = False
                
    
    def moveNorth(self):
        ## Ensures the player can actually move
        if self.state != FREE:
            return
        self.y -= self.speed

        self.facing = 0

        ## Collision stuffs
        for i in range(len(walls)):
            if collision.lineRect((walls[i].x, walls[i].y+walls[i].height), \
                                  (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                                  (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                  0, self.speed):
                self.y = walls[i].y + walls[i].height + self.yRad
                break
        else: # Camera movement only happens if there are no wall collisions
            global camYpos        
            if (self.y - self.yRad + camYpos <= camFollowRect[1] \
                and camYpos < 0):
                camYpos += self.speed
            
        # Checks if in wifi zone
        for o in objList:
            if isinstance(o, maps.Wifi):
                if math.sqrt((self.x-o.x)**2 + (self.y-o.y)**2) <= o.radius:
                    self.connected = True
                    break
                else:
                    self.connected = False

    def moveEast(self):
        if self.state != FREE:
            return        
        self.x += self.speed
        self.facing = 1
        for i in range(len(walls)):
            if collision.lineRect((walls[i].x, walls[i].y), (walls[i].x, walls[i].y+walls[i].height),\
                                  (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                  1, self.speed):
                self.x = walls[i].x - self.xRad
                break
        else:
            global camXpos
            if (self.x + self.xRad + camXpos >= camFollowRect[0] + camFollowRect[2] \
                and camXpos > -maplength + winlength):
                camXpos -= self.speed
        
        for o in objList:
            if isinstance(o, maps.Wifi):        
                if math.sqrt((self.x-o.x)**2 + (self.y-o.y)**2) <= o.radius:
                    self.connected = True
                    break
                else:
                    self.connected = False
                
    
    def moveSouth(self):
        if self.state != FREE:
            return        
        self.y += self.speed
        self.facing = 2
        for i in range(len(walls)):
            if collision.lineRect((walls[i].x, walls[i].y), (walls[i].x+walls[i].width, walls[i].y),\
                                  (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                  2, self.speed):
                self.y = walls[i].y - self.yRad
                break
        else:
            global camYpos
            if (self.y + self.yRad + camYpos >= camFollowRect[1] + camFollowRect[3] \
                and camYpos > -mapheight + winheight):
                camYpos -= self.speed
        for o in objList:
            if isinstance(o, maps.Wifi):
                if math.sqrt((self.x-o.x)**2 + (self.y-o.y)**2) <= o.radius:
                    self.connected = True
                    break
                else:
                    self.connected = False
                
    
    def moveWest(self):
        if self.state != FREE:
            return        
        self.x -= self.speed
        self.facing = 3
        for i in range(len(walls)):
            if collision.lineRect((walls[i].x+walls[i].width, walls[i].y), \
                                  (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                                  (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                  3, self.speed):
                self.x = walls[i].x + walls[i].width + self.xRad
                break
        else:
            global camXpos
            if (self.x - self.xRad + camXpos <= camFollowRect[0] \
                and camXpos < 0):
                camXpos += self.speed
        for o in objList:
            if isinstance(o, maps.Wifi):
                if math.sqrt((self.x-o.x)**2 + (self.y-o.y)**2) <= o.radius:
                    self.connected = True
                    break
                else:
                    self.connected = False
                
        
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
    
    def hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            print('oops you deaded yourself')
        else:
            self.animTimers['hurt'] = self.iFrames
    
    def punch(self):
        activeParticles.append(PunchParticle(self, self.connected))

    def shootBeam(self):
        activeParticles.append(BeamParticle(self, self.connected))
            
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
            if isinstance(p, PunchParticle):
                p.checkDamage(enemyList)
            elif isinstance(p, BeamParticle):
                if p.duration < 10:
                    p.checkDamage(enemyList)
        i += 1

def reloadLevel():
    '''
    Call after changing level
    '''
    global walls, bg, enemyList, objList, camXpos, camYpos, maplength, mapheight
    captain.x = maps.startpoints[level][0]
    captain.y = maps.startpoints[level][1]
    maplength, mapheight = maps.mapSizes[level] 
    walls = maps.loadWalls(level)
    bg = maps.loadBG(level)
    enemyList = maps.loadEnemies(level)
    objList = maps.loadObjects(level)
    camXpos, camYpos = maps.camStartpoints[level]    

## Main loop
gameState = MENU

captain = player(maps.startpoints[level])

walls = maps.loadWalls(level)
bg = maps.loadBG(level)
enemyList = maps.loadEnemies(level)
objList = maps.loadObjects(level)

activeParticles = [] ## Array of particle effects

debug = True
gameClock = pygame.time.Clock()
running = True
while running:
    gameClock.tick()
    pygame.time.delay(10) ## apparently this helps with inputs
    
    ## Update game state
    if gameState == MENU and menu.menuState == 'PLAY':
        gameState = PLAYING
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # what happens when X is pressed
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # what happens when space is pressed
                if gameState == MENU: # Remove this once menu button works
                    gameState = PLAYING
                else:
                    print('Space is unmapped ... ya dingus')
                
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): # left mouse button
            if gameState == PLAYING and captain.state == FREE:
                boop.play()
                captain.checkFacing()
                captain.punch()
            elif gameState == MENU:
                mpos = pygame.mouse.get_pos()
                for b in menu.activeButtons:
                    b.checkClick(mpos)
        
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3): # right mouse button
            if gameState == PLAYING and captain.state == FREE:
                kaboom.play()
                captain.checkFacing()
                captain.shootBeam()
     
    keys = pygame.key.get_pressed() # keys is a giant array of booleans
    if keys[pygame.K_d] and gameState == PLAYING:
        captain.moveEast()
        captain.isMoving = True
    if keys[pygame.K_a] and gameState == PLAYING:
        captain.moveWest()
        captain.isMoving = True
    if keys[pygame.K_w] and gameState == PLAYING:
        captain.moveNorth()
        captain.isMoving = True
    if keys[pygame.K_s] and gameState == PLAYING:
        captain.moveSouth()
        captain.isMoving = True
    ## Don't use elifs, or else diagonal mvmt won't be possible

    # Check if level needs to be changed
    if collision.rects((captain.x - captain.xRad, captain.y - captain.yRad, \
                        2*captain.xRad, 2*captain.yRad), maps.nextLevelTriggers[level]):
        level += 1
        reloadLevel()

    # Idle animation
    if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
        captain.isMoving = False
        if captain.animTimers['idle'] <= 0:
            captain.animTimers['idle'] = 60
        else:
            captain.animTimers['idle'] -= 1
    
    if gameState == PLAYING:
        currentMap.blit(bg, (0, 0)) # draws the level
        ## This background is the main source of lag    
        
        if debug:
            for i in range(len(walls)):
                walls[i].draw(currentMap)    
         
        for e in enemyList:
            if isinstance(e, enemies.Jelly):
                if e.state == FREE:
                    e.moveToward(captain, walls)
                    # Checks if a jelly hit the player
                    if captain.animTimers['hurt'] <= 0:
                        if collision.rects((captain.x - captain.xRad, captain.y - captain.yRad,\
                                           captain.xRad*2, captain.yRad*2), (e.x - e.xRad,\
                                           e.y - e.yRad, e.xRad*2, e.yRad*2)):
                            captain.hurt(1)
                e.draw(currentMap, debug)
        
        ## It looks a bit better if the player can't move or turn while punching
        if captain.state == PUNCH or captain.state == BEAM:
            captain.checkFacing()
        if captain.animTimers['hurt'] > 0:
            captain.animTimers['hurt'] -= 1
        
        if captain.animTimers['hurt']%4 < 2:
            captain.draw()    
            
        for o in objList:
            o.draw(currentMap, debug)
        
        drawParticles()  
        
        win.blit(currentMap, (camXpos, camYpos))

        win.blit(healthBattery[captain.health], (0, 0))
        
        ## Camera follow rect
        if debug:
            pygame.draw.rect(win, red, camFollowRect, 5)
        
        ## FPS display
        if debug:
            fpsText = font1.render(str(round(gameClock.get_fps())) + " FPS", False, black, white)
            win.blit(fpsText, (winlength - fpsText.get_size()[0], 0))
    
    elif gameState == MENU:
        menu.draw(win)
    
    pygame.display.update() # put this at the end of your main loop

pygame.quit() # put this at the end of all your pygame files
