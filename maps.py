import pygame # I'll probably need it
import collision

mapSizes = ['dummy', (1500, 1500)]
numLevels = 1

class Level:
    def __init__(self, ID):
        self.ID = ID # This should be unique
        self.walls = [] # doesn't include border walls
        self.startpoint = (0, 0) # overwrite this
        self.bg = 0 # replace with surface
    
    def set_startpoint(self, x, y):
        '''
        This is just a default - the player will not always start here
        '''
        self.startpoint = (x, y)
    
    def set_walls(self, wlist):
        self.walls = wlist
    
    def set_bg(self, surface):
        self.bg = surface

def loadBG(levelID):
    '''
    Returns a surface consisting of the background image for the given level.
    Returns void if level is invalid.
    '''
    if levelID < 1 or levelID > numLevels:
        print("Error: level {} doesn't exist")
        return
    
    if levelID == 1:
        return l1.bg
    ## No other levels atm

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
    
    if levelID == 1:
        walls.extend(l1.walls)
    ## No other levels atm
    
    return walls

## ************* The actual levels ****************

l1 = Level(1)
l1.set_startpoint(700, 1350)
l1.set_walls([collision.Wall(0, 0, 250, 1500),
              collision.Wall(250, 1200, 300, 300),
              collision.Wall(550, 750, 300, 150),
              collision.Wall(850, 300, 650, 1200),
              collision.Wall(850, 0, 650, 100)])
s = pygame.Surface(mapSizes[1])
s.fill(pygame.Color('white'))
l1.set_bg(s)