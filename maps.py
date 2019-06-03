import pygame # I'll probably need it
import collision
import enemies

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

mapSizes = ['dummy', (1500, 1500), (1500, 1250), (1200, 1100), (1200, 1300)]
startpoints = ['dummy', (700, 1350), (100, 200), (550, 1050), (600, 1200)]
camStartpoints = ['dummy', (-300, -900), (0, 0), (-150, -500), (-200, -700)]
nextLevelTriggers = ['dummy', (1400, 100, 100, 200), 
                     (1300, 0, 100, 100), (450, 0, 200, 100), (0, 0, 1, 1)]
numLevels = 4


class Wifi:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.imageXRad = 40
        self.imageYRad = 50
        
    
    def draw(self, m, debug=False):
        '''
        Requires currentMap as a parameter
        '''
        pygame.draw.ellipse(m, pygame.Color('blue'), (self.x-self.radius, self.y-self.radius, \
                                        self.radius*2, self.radius*2), 5)
        p = pygame.transform.scale(phone, (self.imageXRad*2, self.imageYRad*2))
        m.blit(p, (self.x-self.imageXRad, self.y-self.imageYRad))

def loadBG(levelID):
    '''
    Returns a surface consisting of the background image for the given level.
    Returns void if level is invalid.
    '''
    if levelID < 1 or levelID > numLevels:
        print("Error: level {} doesn't exist")
        return
    
    s = pygame.Surface(mapSizes[levelID])
    if levelID == 1: # level 1 BG
        s.fill(pygame.Color('white'))
        ## Grass
        g = pygame.transform.scale(grassTile, (100, 100))
        for i in range(13): # x values 200 to 1500
            for j in range(15): # y values 0 to 1500
                s.blit(g, (i*100 + 200, j*100)) 
        ## Houses
        h = pygame.transform.scale(house, (300, 300))
        s.blit(h, (250, 1200))
        for j in range(5): # y values from 0 to 1500
            s.blit(h, (-50, j*300))
        for j in range(4): # y values from 300 to 1500
            s.blit(h, (900, j*300 + 300))
            s.blit(h, (1200, j*300 + 300))
        ## Crates
        c = pygame.transform.scale(crate, (100, 100))
        for i in range(8): # x values from 850 to 1550
            s.blit(c, (850 + i*100, 0))
        s.blit(c, (550, 750))
        s.blit(c, (650, 800))
        s.blit(c, (750, 750))
        ## Rocks
        r = pygame.transform.scale(rock, (50, 50))
        for j in range(24): # y values from 300 to 1500
            s.blit(r, (850, 300 + j*50))
        s.blit(r, (550, 850))
        s.blit(r, (600, 850))
        s.blit(r, (650, 750))
        s.blit(r, (700, 750))
        s.blit(r, (750, 850))
        s.blit(r, (800, 850))
        s.blit(r, (550, 700))
    elif levelID == 2: # level 2 bg
        s.fill(pygame.Color('white'))
    elif levelID == 3: # level 3 bg
        s.fill(pygame.Color('white'))
    elif levelID == 4: # level 4 bg
        s.fill(pygame.Color('white'))
    
    return s

def loadWalls(levelID):
    '''
    Returns an array of walls, representing the collision for the level.
    '''
    walls = []
    if levelID < 1 or levelID > numLevels: # Only done 1 level so far
        print("Error: level {} doesn't exist")
        return walls
    
    ## Map boundaries
    walls.extend([collision.Wall(0, 0, mapSizes[levelID][0], 2),
                  collision.Wall(0, 0, 2, mapSizes[levelID][1]),
                  collision.Wall(mapSizes[levelID][0], 0, 2, mapSizes[levelID][1]),
                  collision.Wall(0, mapSizes[levelID][1], mapSizes[levelID][0], 2)])
    
    if levelID == 1: # level 1 Walls
        walls.extend([collision.Wall(0, 0, 250, 1500),
                      collision.Wall(250, 1200, 300, 300),
                      collision.Wall(550, 750, 300, 150),
                      collision.Wall(850, 300, 650, 1200),
                      collision.Wall(850, 0, 650, 100),
                      collision.Wall(550, 700, 50, 50)])
    elif levelID == 2: # level 2 Walls
        walls.extend([collision.Wall(0, 0, 500, 100),
                      collision.Wall(400, 100, 100, 200),
                      collision.Wall(500, 0, 800, 50),
                      collision.Wall(1200, 50, 100, 250),
                      collision.Wall(0, 300, 200, 200),
                      collision.Wall(0, 500, 500, 750),
                      collision.Wall(500, 1200, 7500, 50),
                      collision.Wall(1200, 500, 200, 700),
                      collision.Wall(1400, 0, 100, 1250),
                      collision.Wall(800, 250, 100, 300)])
    elif levelID == 3: # level 3 Walls
        walls.extend([collision.Wall(50, 0, 450, 200),
                      collision.Wall(50, 200, 150, 250),
                      collision.Wall(50, 700, 150, 300),
                      collision.Wall(50, 1000, 500, 100),
                      collision.Wall(700, 0, 450, 200),
                      collision.Wall(1000, 200, 150, 250),
                      collision.Wall(1000, 700, 150, 300),
                      collision.Wall(650, 1000, 500, 100),
                      collision.Wall(150, 600, 50, 100),
                      collision.Wall(1000, 600, 50, 100),
                      collision.Wall(0, 0, 50, 1100),
                      collision.Wall(1150, 0, 50, 1100)])
    elif levelID == 4: # level 4 Walls
        walls.extend([collision.Wall(0, 0, 100, 1300),
                      collision.Wall(1100, 0, 100, 1300),
                      collision.Wall(100, 0, 1000, 100),
                      collision.Wall(100, 100, 400, 200),
                      collision.Wall(700, 100, 400, 200),
                      collision.Wall(100, 1100, 400, 200),
                      collision.Wall(700, 1100, 400, 200)])
    
    return walls

def loadObjects(levelID):
    '''
    Returns a list of all objects (Wifi signals and enemies) for a given level.
    '''
    objects = []
    if levelID < 1 or levelID > numLevels: # Only done 1 level so far
        print("Error: level {} doesn't exist")
        return objects
    
    if levelID == 1: # Level 1 Objects
        ## Wifi signals
        objects.extend([Wifi(550, 400, 200)])
    elif levelID == 2: # level 2 objects
        objects.extend([Wifi(850, 1000, 200)])
    elif levelID == 3: # level 3 objects
        objects.extend([Wifi(200, 1000, 300),
                        Wifi(1000, 1000, 300)])
    elif levelID == 4: # level 4 objects
        objects.extend([Wifi(600, 200, 200),
                        Wifi(100, 300, 150),
                        Wifi(1100, 300, 150)])
    
    return objects

def loadEnemies(levelID):
    '''
    Returns a list of all enemies for a given level.
    '''
    elist = []
    if levelID < 1 or levelID > numLevels: # Only done 1 level so far
        print("Error: level {} doesn't exist")
        return elist
    
    if levelID == 1: # level 1 enemies
        ## Jellies
        elist.extend([enemies.Jelly(700, 300)])
    elif levelID == 2: # level 2 enemies
        elist.extend([enemies.Jelly(900, 100),
                      enemies.Jelly(1350, 200)])
    elif levelID == 3: # level 3 enemies
        elist.extend([enemies.Jelly(100, 650),
                      enemies.Jelly(1100, 600),
                      enemies.Jelly(350, 400),
                      enemies.Jelly(850, 400)])
    elif levelID == 4: # level 4 enemies
        elist.extend([enemies.PirateJelly(600, 200, elist)])
    return elist

## **************** Sprites *************
## Variable declarations
house = 0;
rock = 0;
crate = 0;
grassTile = 0;
concreteTile = 0;

def loadSprites():
    '''
    Call this immediately after defining win
    '''
    ## Need to be declared global, because they're not inside an array
    global house
    house = pygame.image.load('images/house.png').convert_alpha()
    global rock
    rock = pygame.image.load('images/rock.png').convert_alpha()
    global crate
    crate = pygame.image.load('images/crate.png').convert_alpha()
    global grassTile
    grassTile = pygame.image.load('images/grass.png').convert_alpha()
    global concreteTile
    concreteTile = pygame.image.load('images/concrete.png').convert_alpha()
    global phone
    phone = pygame.image.load('images/phone.png').convert_alpha()
