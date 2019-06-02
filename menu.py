import pygame
import math

pygame.font.init()

## ****** Constants ********
#MAIN = 0
#OPTIONS = 1
#PLAY = 2
# I actually don't use these, because I need them to be strings

## Fonts
technoL = pygame.font.Font('fonts/SUPERHERO.ttf', 96)
scribbleL = pygame.font.Font('fonts/Scriptonite.ttf', 120)
basicL = pygame.font.Font('fonts/Bangers.ttf', 60)

## Text
playText = basicL.render('Play', False, pygame.Color('black'))
opsText = basicL.render('Options', False, pygame.Color('black'))

## *************************

## Sprite variable declarations
city = 0
hero = 0

class Button:
    def __init__(self, rect, curState, toState):
        self.rect = rect
        self.curState = curState
        self.toState = toState
    
    def checkClick(self, mousePos):
        '''
        Consumes mouse coordinates and checks if the button is clicked. If so,
        it sets the animation timers accordingly.
        '''
        mouseX, mouseY = mousePos
        x, y, length, height = self.rect
        ## Checking if mouse is inside rect
        if (mouseX >= x and mouseX <= x + length) and \
           (mouseY >= y and mouseY <= y + height):
            transition = self.curState + 'to' + self.toState
            animTimers[self.curState] = 0
            animTimers[transition] = animLengths[transition]
            ## Inactivates all buttons
            activeButtons.clear()

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
    if menuState == 'MAIN':
        s.blit(city, (0, 0))
        cap = scribbleL.render('Captain', False, pygame.Color('black'))
        # Screw math, I'm just gonna hard code these numbers.
        s.blit(cap, (100, 70))
        wf = technoL.render('WIFI', False, pygame.Color('black'))
        s.blit(wf, (200, 70 + cap.get_size()[1]))
        
        ## Animations
        heroX = round(x * 0.6)
        heroYmin = round(y * 0.1)     
        
        if animTimers['MAINstart'] > 0: # Main intro animation
            ratio = (y - heroYmin) / animLengths['MAINstart']
            heroY = round(heroYmin + animTimers['MAINstart']*ratio)
            animTimers['MAINstart'] -= 1
            if animTimers['MAINstart'] <= 0: # End of animation
                animTimers['MAIN'] = animLengths['MAIN']
                ## add main buttons to active button list
                playButton = Button((200, 400, playText.get_size()[0], playText.get_size()[1]),\
                                    'MAIN', 'PLAY')
                activeButtons.append(playButton)
                opsButton = Button((200, 400 + playText.get_size()[1], \
                                    opsText.get_size()[0], opsText.get_size()[1]), \
                                   'MAIN', 'OPTIONS')
                ## I'm not gonna add opsButton to activeButtons until I actually
                ## make the options menu and decide whether it'll have transitions
                
        elif animTimers['MAIN'] > 0: # Main looping animation
            ## Button text
            s.blit(playText, (200, 400))
            s.blit(opsText, (200, 400 + playText.get_size()[1]))
            
            # Hero
            yDiff = 50 # experiment with this value
            heroYmax = heroYmin + yDiff 
            n = yDiff * math.cos(math.radians(animTimers['MAIN']))
            heroY = heroYmax - n
            
            if animTimers['MAIN'] == 1:
                animTimers['MAIN'] = animLengths['MAIN']
            else:
                animTimers['MAIN'] -= 1
                
        elif animTimers['MAINtoPLAY'] > 0:
            ## Still display the buttons
            s.blit(playText, (200, 400))
            s.blit(opsText, (200, 400 + playText.get_size()[1])) 
            
            # Hero flies up
            heroYstart = heroYmin + 25 # experiment?
            heroY = animTimers['MAINtoPLAY']*10 - (animLengths['MAINtoPLAY']*10 - heroYstart)
            
            animTimers['MAINtoPLAY'] -= 1
            if animTimers['MAINtoPLAY'] <= 0:
                menuState = 'PLAY'
        
        s.blit(hero, (heroX, heroY))
        
        
        

menuState = 'MAIN' ## State at start of program
animLengths = {
    'MAINstart': 50,
    'MAIN': 360,
    'MAINtoPLAY': 80,
    'MAINtoOPTIONS': 0,
    'OPTIONS': 0,
    'OPTIONStoMAIN': 0
}
animTimers = { # Only one of these should be nonzero at any given moment
    'MAINstart': 50,
    'MAIN': 0,
    'MAINtoPLAY': 0,
    'MAINtoOPTIONS': 0,
    'OPTIONS': 0,
    'OPTIONStoMAIN': 0
}
activeButtons = []