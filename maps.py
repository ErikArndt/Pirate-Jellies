import pygame # I'll probably need it
import collision

mapSizes = ['dummy', (1500, 1500)]
numLevels = 1

def loadBG(level):
    '''
    Returns a surface consisting of the background image for the given level.
    Returns void if level is invalid.
    '''
    if level < 1 or level > numLevels:
        print("Error: level {} doesn't exist")
        return
    
    s = pygame.Surface(mapSizes[level])
    if level == 1:
        s.fill(pygame.Color('white'))
    ## TODO - touch up Sarah's tiles and turn this into a proper level background.
    return s

def loadWalls(level):
    '''
    Returns an array of walls, representing the collision for the level.
    '''
    walls = []
    if level < 1 or level > numLevels: # Only done 1 level so far
        print("Error: level {} doesn't exist")
        return walls
    
    ## Map boundaries
    walls.extend([collision.Wall(0, 0, mapSizes[level][0], 2),
                  collision.Wall(0, 0, 2, mapSizes[level][1]),
                  collision.Wall(mapSizes[level][0], 0, 2, mapSizes[level][1]),
                  collision.Wall(0, mapSizes[level][1], mapSizes[level][0], 2)])
    
    if level == 1:
        walls.extend([collision.Wall(0, 0, 250, 1500),
                      collision.Wall(250, 1200, 300, 300),
                      collision.Wall(550, 750, 300, 150),
                      collision.Wall(850, 300, 650, 1200),
                      collision.Wall(850, 0, 650, 100)])
    
    return walls