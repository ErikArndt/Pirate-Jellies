import math

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
                line2Slope = (line2E[1]-line2S[1])/(line2E[0]-line2S[0])
                line2Intcpt = line2S[1] - line2S[0]*line2Slope

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
                line2Slope = (line2E[1]-line2S[1])/(line2E[0]-line2S[0])
                line2Intcpt = line2S[1] - line2S[0]*line2Slope

                if line1S[0] >= line2E[0] or line1S[0] <= line2S[0]:
                    output = (-1, -1)
                else:
                    PoIY = line2Intcpt + line2Slope*line1S[0]
                    if PoIY >= line1S[1] and PoIY <= line1E[1]:
                        output = (line1S[0], PoIY)
                    else:
                        output = (-1, -1)
            else:
                if line2S[0] == line1S[0]:
                    output = (line1S[0], PoIY)
                else:
                    output = (-1, -1)
    
    return output



def rectIntersect(rect1, rect2):
    #Tells you whether two rectangles overlap at any point.
    #rect1 is the coordinates of the top left corner of the rectangle, as well as its width and height, (x, y, width, height).
    #The output is a boolean, True if the rectangles overlap.
    x1, y1, width1, height1 = rect1
    x2, y2, width2, height2 = rect2
    if ((x1 > x2 and x1 < x2+width2) or (x1+width1 > x2 and x1+width1 < x2+width2)) and ((y1 > y2 and y1 < y2+height2) or (y1+height1 > y2 and y1+height1 < y2+height2)):
        output = True
    else:
        output = False
    return output

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
