import math
import pygame
import functions
pygame.init()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

wallStart = (325, 300)
wallEnd =(325, 200)

circlePos = (450, 250)

sightColour = (0,0,0)

win = pygame.display.set_mode((500, 500))
running = True
while running:
    pygame.draw.rect(win, (255, 255, 255), (0, 0, 500, 500))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            x,y = event.pos
        if event.type == pygame.QUIT:
            running = False

##    if wallStart[0] != wallEnd[0]:
##        if x != circlePos[0]:
##            wallSlope = (wallEnd[1]-wallStart[1])/(wallEnd[0]-wallStart[0])
##            wallIntercept = wallStart[1] - wallStart[0]*wallSlope
##
##            sightSlope = (circlePos[1]-y)/(circlePos[0]-x)
##            sightIntercept = y - x*sightSlope
##
##            intersectX = (wallIntercept-sightIntercept)/(sightSlope-wallSlope)
##            if intersectX >= wallStart[0] and intersectX <= wallEnd[0] and intersectX >= x and intersectX <= circlePos[0]:
##                sightColour = red
##            else:
##                sightColour = green
##        else:
##            wallSlope = (wallEnd[1]-wallStart[1])/(wallEnd[0]-wallStart[0])
##            wallIntercept = wallStart[1] - wallStart[0]*wallSlope
##
##            if x < wallStart[0] or x > wallEnd[0]:
##                sightColour = green
##            else:
##                interceptY = wallIntercept + wallSlope*x
##                if interceptY >= y and interceptY <= circlePos[1]:
##                    sightColour = red
##                else:
##                    sightColour = green
##    else:
##        if x != circlePos[0]:
##            sightSlope = (circlePos[1]-y)/(circlePos[0]-x)
##            sightIntercept = y - x*sightSlope
##
            
##            if wallStart[0] >= circlePos[0] or wallStart[0] <= x:
##                sightColour = green
##            else:
##                interceptY = sightIntercept + sightSlope*wallStart[0]
##                if interceptY >= wallStart[1] and interceptY <= wallEnd[1]:
##                    sightColour = red
##                else:
##                    sightColour = green
##        else:
##            if x == wallStart[0]:
##                sightColour = red
##            else:
##                sightColour = green
    intersection = functions.linesCross(wallStart, wallEnd, (x,y), (circlePos[0], circlePos[1]), False)
    if intersection != (-1,-1):
        sightColour = red
    else:
        sightColour = green
        
        
    pygame.draw.rect(win, (0,255,0), (x-20, y-20, 40, 40))
    pygame.draw.ellipse(win, (0,0,255), (440, 240, 20, 20))
    pygame.draw.line(win, (0,0,0), wallStart, wallEnd, 1)
    pygame.draw.line(win, sightColour, (x, y), (450, 250), 2)
    pygame.draw.ellipse(win, red, (intersection[0]-5, intersection[1]-5, 10, 10), 0)
    pygame.display.update()
pygame.quit()
