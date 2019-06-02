import pygame

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, m):
        '''
        Requires the current map surface. Intended for debug mode only.
        '''
        pygame.draw.rect(m, pygame.Color('black'), (self.x, self.y, self.width, \
                                                    self.height), 0)
        


def rects(rect1, rect2):
    '''
    Tells you whether two rectangles overlap at any point.
    rect1 is the coordinates of the top left corner of the rectangle, as well 
    as its width and height, (x, y, width, height).
    The output is a boolean, True if the rectangles overlap.
    '''
    x1, y1, width1, height1 = rect1
    x2, y2, width2, height2 = rect2
    if x2 < x1+width1 and y2 <y1+height1 and x2 + width2 > x1 and y2 + height2 > y1:
        output = True
    else:
        output = False
    return output

def lineRect(edgeS, edgeE, rect, direction, speed):
    '''
    returns boolean, checks if rect (the player or some other object) is
    colliding with a line given by start and end points.
    direction is a number from 0-3, N E S W respectively
    speed is the speed of the rectangle moving into the line.
    speed used to determine which wall the rect is touching when near a corner
    requires: the line is either perfectly horizontal or perfectly vertical
    '''
    rectX, rectY, rectWidth, rectHeight = rect
    
    if direction == 0:
        if rectY >= edgeS[1] or rectY < edgeS[1]-speed*2:
            output = False
        elif edgeS[0] >= rectX+rectWidth or edgeE[0] <= rectX:
            output = False
        else:
            output = True

    if direction == 1:
        if rectX+rectWidth <= edgeS[0] or rectX+rectWidth > edgeS[0]+speed*2:
            output = False
        elif edgeS[1] >= rectY+rectHeight or edgeE[1] <= rectY:
            output = False
        else:
            output = True

    if direction == 2:
        if rectY+rectHeight <= edgeS[1] or rectY+rectHeight > edgeS[1]+speed*2:
            output = False
        elif edgeS[0] >= rectX+rectWidth or edgeE[0] <= rectX:
            output = False
        else:
            output = True

    if direction == 3:
        if rectX >= edgeS[0] or rectX < edgeS[0]-speed*2:
            output = False
        elif edgeS[1] >= rectY+rectHeight or edgeE[1] <= rectY:
            output = False
        else:
            output = True
    return output
