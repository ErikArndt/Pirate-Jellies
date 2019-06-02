import pygame
import math

pygame.font.init()

## ****** Constants ********
MAIN = 0
OPTIONS = 1

## Fonts
technoL = pygame.font.Font('fonts/SUPERHERO.ttf', 96)
scribbleL = pygame.font.Font('fonts/Scriptonite.ttf', 120)
basicS = pygame.font.Font('fonts/Bangers.ttf', 24)

## *************************

## Sprite variable declarations
city = 0
hero = 0

def loadSprites(winDims):
    '''
    Call immediately after defining win. Consumes dimensions of win.
    '''
    global city
    city = pygame.image.load('images/PlaceholderMenuBG.png').convert()
    city = pygame.transform.scale(city, winDims)
    global hero
    hero = pygame.image.load('images/heroic_pose.png').convert_alpha()
    heroHeight = winDims[1] * 0.7 # Just a guess, might need to change
    heroLength = heroHeight * 0.4 # Preserves ratio of original image
    hero = pygame.transform.scale(hero, (round(heroLength), round(heroHeight)))

def draw(s):
    '''
    Blits the current menu state to the given surface s.
    '''
    global menuState
    x, y = s.get_size()
    if menuState == MAIN:
        s.blit(city, (0, 0))
        cap = scribbleL.render('Captain', False, pygame.Color('black'))
        # Screw math, I'm just gonna hard code these numbers.
        s.blit(cap, (100, 70))
        wf = technoL.render('WIFI', False, pygame.Color('black'))
        s.blit(wf, (200, 70 + cap.get_size()[1]))
        
        heroX = round(x * 0.6)
        heroYmin = round(y * 0.1)      
        if animTimers['MAINstart'] > 0: # Main intro animation
            ratio = (y - heroYmin) / 50
            heroY = round(heroYmin + animTimers['MAINstart']*ratio)
            animTimers['MAINstart'] -= 1
            if animTimers['MAINstart'] <= 0: # End of animation
                animTimers['MAIN'] = 360
        elif animTimers['MAIN'] > 0: # Main looping animation
            yDiff = 50 # experiment with this value
            heroYmax = heroYmin + yDiff 
            n = yDiff * math.cos(math.radians(animTimers['MAIN']))
            heroY = heroYmax - n
            if animTimers['MAIN'] == 1:
                animTimers['MAIN'] = 360
            else:
                animTimers['MAIN'] -= 1
        
        s.blit(hero, (heroX, heroY))

menuState = MAIN ## State at start of program
animTimers = {
    'MAINstart': 50,
    'MAIN': 0,
    'MAINplay': 0,
    'MAINtoOPTIONS': 0,
    'OPTIONStoMAIN': 0
}