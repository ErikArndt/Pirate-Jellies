import math
import pygame
import functions
pygame.init()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

rect = (250, 250, 50, 70)

rectColour = (0,0,0)

win = pygame.display.set_mode((500, 500))
running = True
while running:
    pygame.draw.rect(win, (255, 255, 255), (0, 0, 500, 500))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            x,y = event.pos
        if event.type == pygame.QUIT:
            running = False

    if functions.rectIntersect((x-20, y-20, 40, 40), rect):
        rectColour = red
    else:
        rectColour = green
        
        
    pygame.draw.rect(win, (0,255,0), (x-20, y-20, 40, 40))
    pygame.draw.rect(win, rectColour, rect, 0)
    pygame.display.update()
pygame.quit()
