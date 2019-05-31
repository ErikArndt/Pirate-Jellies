import math

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
    
    