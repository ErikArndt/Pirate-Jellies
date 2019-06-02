import pygame # I'll probably need it
import collision
import enemies

mapSizes = ['dummy', (1500, 1500), (1500, 1250), (1100, 1100)]
startpoints = ['dummy', (700, 1350), (100, 200), (550, 1050)]
camStartpoints = ['dummy', (-300, -900), (0, 0), (-150, -500)]
numLevels = 3


class Wifi:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.imageRad = 25
    
    def draw(self, m, debug=False):
        '''
        Requires currentMap as a parameter
        '''
        pygame.draw.ellipse(m, pygame.Color('blue'), (self.x-self.radius, self.y-self.radius, \
                                        self.radius*2, self.radius*2), 5)
        ## Placeholder for phone image
        if debug:
            pygame.draw.rect(m, pygame.Color('blue'), (self.x-self.imageRad, self.y-self.imageRad, \
                                                       self.imageRad*2, self.imageRad*2))


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
    ## No other levels atm
    
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
        walls.extend([collision.Wall(0, 0, 450, 200),
                      collision.Wall(0, 200, 150, 300),
                      collision.Wall(0, 700, 150, 300),
                      collision.Wall(0, 1000, 500, 100),
                      collision.Wall(650, 0, 450, 200),
                      collision.Wall(950, 200, 150, 300),
                      collision.Wall(950, 700, 150, 300),
                      collision.Wall(600, 1000, 500, 100),
                      collision.Wall(100, 600, 50, 100),
                      collision.Wall(950, 600, 50, 100)])
    ## No other levels atm
    
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
        objects.extend([Wifi(150, 1000, 300),
                        Wifi(950, 1000, 300)])
    
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
        elist.extend([enemies.Jelly(50, 650),
                      enemies.Jelly(1050, 600),
                      enemies.Jelly(300, 400),
                      enemies.Jelly(800, 400)])
    
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
