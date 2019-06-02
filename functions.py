import math
import pygame

#Not in use
def linesCross (line1S, line1E, line2S, line2E, ray):
    #Gives you the point of intersection for two line segments, or one line segment and a ray.
    #The output is given as a set of coordinates (x, y)
    #If there is no intersection, it will output (-1, -1)
    #line1S is the starting coordinates for the first line, given as (x, y). line1E is the ending coordinates, and so on.
    #ray is a boolean. If true, then line 1 is a ray, and will continue on infinitely past its ending coordinates
    if line1S[0] > line1E[0]:
        line1S, line1E = line1E, line1S
    if line2S[0] > line2E[0]:
        line2S, line2E = line2E, line2S
        
    if line1S[0] == line1E[0] and line1S[1] > line1E[1]:
        line1S, line1E = line1E, line1S
    if line2S[0] == line2E[0] and line2S[1] > line2E[1]:
        line2S, line2E = line2E, line2S
    
    if line1S[0] != line1E[0]:
        line1Slope = (line1E[1]-line1S[1])/(line1E[0]-line1S[0])
        line1Intcpt = line1S[1] - line1S[0]*line1Slope
    if line2S[0] != line2E[0]:
        line2Slope = (line2E[1]-line2S[1])/(line2E[0]-line2S[0])
        line2Intcpt = line2S[1] - line2S[0]*line2Slope

    if line1S[0] != line1E[0]:
        if line2S[0] != line2E[0]:
            if line2Slope == line1Slope:
                return (-1, -1)
            PoIX = (line1Intcpt-line2Intcpt)/(line2Slope-line1Slope)
            if ray:
                if PoIX >= line1S[0] and PoIX >= line2S[0] and PoIX <= line2E[0]:
                    output = (PoIX, line1Slope*PoIX + line1Intcpt)
                else:
                    output = (-1, -1)
            else:
                if PoIX >= line1S[0] and PoIX <= line1E[0] and PoIX >= line2S[0] and PoIX <= line2E[0]:
                    output = (PoIX, line1Slope*PoIX + line1Intcpt)
                else:
                    output = (-1, -1)
        else:
            if ray:
                if line2S[0] < line1S[0]:
                    output = (-1, -1)
                else:
                    PoIY = line1Intcpt + line1Slope*line2S[0]
                    if PoIY >= line2S[1] and PoIY <= line2E[1]:
                        output = (line2S[0], PoIY)
                    else:
                        output = (-1, -1)
            else:
                if line2S[0] < line1S[0] or line2S[0] > line1E[0]:
                    output = (-1, -1)
                else:
                    PoIY = line1Intcpt + line1Slope*line2S[0]
                    if PoIY >= line2S[1] and PoIY <= line2E[1]:
                        output = (line2S[0], PoIY)
                    else:
                        output = (-1, -1)

    else:
        if ray:
            if line2S[0] != line2E[0]:
                if line1S[0] >= line2E[0] or line1S[0] <= line2S[0]:
                    output = (-1, -1)
                else:
                    PoIY = line2Intcpt + line2Slope*line1S[0]
                    if PoIY >= line1S[1]:
                        output = (line1S[0], PoIY)
                    else:
                        output = (-1, -1)
            else:
                if line2S[0] == line1S[0]:
                    output = (line1S[0], PoIY)
                else:
                    output = (-1, -1)
        else:
            if line2S[0] != line2E[0]:
                if line1S[0] >= line2E[0] or line1S[0] <= line2S[0]:
                    output = (-1, -1)
                else:
                    PoIY = line2Intcpt + line2Slope*line1S[0]
                    if PoIY >= line1S[1] and PoIY <= line1E[1]:
                        output = (line1S[0], PoIY)
                    else:
                        output = (-1, -1)
            else:
                output = (-1, -1)
    
    return output

def checkRectWithLine(lineS, lineE, rect, ray=False):
    '''
    Returns the point where a line first intersects with a rectangle.
    lineS is the starting coordinates of the lines (x,y), and lineE is the end coordinates.
    The output is the first collision travelling from start to end.
    rect is the coordinates of the top left corner, and the widht/height (x, y, width, height)
    ray is a boolean, if True the line will continue past its end coordinates.
    '''
    rectX, rectY, width, height = rect

    if lineS[0] < rectX:
        temp = linesCross(lineS, lineE, (rectX, rectY), (rectX, rectY+height), ray)
        if temp != (-1, -1):
            return(temp)
    else:
        temp = linesCross(lineS, lineE, (rectX+width, rectY), (rectX+width, rectY+height), ray)
        if temp != (-1, -1):
            return(temp)
    if lineS[1] < rectY:
        temp = linesCross(lineS, lineE, (rectX, rectY), (rectX+width, rectY), ray)
        if temp != (-1, -1):
            return(temp)
    else:
        temp = linesCross(lineS, lineE, (rectX, rectY+height), (rectX+width, rectY+height), ray)
        if temp != (-1, -1):
            return(temp)
    return(-1, -1)
        

def angleTo(x1, y1, x2, y2):
    '''
    Returns the angle from the first set of coordinates to the second
    set of coordinates. 0 is east, 90 is south, 180 is west, 270 is north.
    Note: returns 0 if the coordinates are identical
    Coordinates go from the northwest corner (0, 0) and count southeast.
    Theoretically, there shouldn't be negative coordinates.
    '''
    xDiff = x2 - x1
    yDiff = y2 - y1
    ## special case for if angle is vertical
    if xDiff == 0:
        if yDiff > 0:
            return 270
        else:
            return 90
    else:            
        absRatio = abs(yDiff) / abs(xDiff)
        absAngle = math.degrees(math.atan(absRatio))
        
        if (xDiff > 0 and yDiff < 0): ## Northeast
            return 360 - absAngle
        elif xDiff > 0: ## East or Southeast
            return absAngle
        elif (xDiff < 0 and yDiff < 0): ## Northwest
            return 180 + absAngle
        else: ## West or Southwest
            return 180 - absAngle


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    '''
    draw some text into an area of a surface
    automatically wraps words
    returns any text that didn't get blitted
    
    drawText: pygame surface, string, rgb value, rect, pygame font -> string
    '''
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text