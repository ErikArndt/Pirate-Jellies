import pygame
import math
import functions

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
basicS = pygame.font.Font('fonts/Bangers.ttf', 24)

## Text
playText = basicL.render('Play', False, pygame.Color('black'))
storyText = basicL.render('Story', False, pygame.Color('black'))
backText = basicL.render('Back', False, pygame.Color('black'))

storyString = "One day, Pirates attacked. Except they weren't any pirates. " \
    + "They were pirate jellies! They decimated the main router of the peaceful city of Hot Spot, " \
    + "destroying the city's wifi connectivity and mildly inconveniencing the "\
    + "populace. How awful! Luckily, the city's brave hero Captain Wifi is here to "\
    + "bring those dastardly jellies to justice! Use the last remaining wifi hotspots"\
    + " to power up Captain Wifi and save the day!"

## *************************

## Sprite variable declarations
city = 0
hero = 0
byte = 0

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
            if self.curState != 'MAIN':
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
    global byte
    byte = pygame.image.load('images/its_ya_boi.png').convert_alpha()
    byte = pygame.transform.scale(byte, (150, 150))

def draw(s):
    '''
    Blits the current menu state to the given surface s.
    '''
    global menuState
    cap = scribbleL.render('Captain', False, pygame.Color('black'))
    wf = technoL.render('WIFI', False, pygame.Color('black'))    
    x, y = s.get_size()
    
    if menuState == 'MAIN':
        s.blit(city, (0, 0))
        
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
                storyButton = Button((200, 400 + storyText.get_size()[1], \
                                      storyText.get_size()[0], storyText.get_size()[1]), \
                                     'MAIN', 'STORY')
                activeButtons.append(storyButton)
        
        elif animTimers['MAINtoPLAY'] > 0:
            s.blit(cap, (100, 70))
            s.blit(wf, (200, 70 + cap.get_size()[1]))            
            
            ## Still display the buttons
            s.blit(playText, (200, 400))
            s.blit(storyText, (200, 400 + playText.get_size()[1])) 
            
            # Hero flies up
            heroYstart = heroYmin + 25 # experiment?
            heroY = animTimers['MAINtoPLAY']*10 - (animLengths['MAINtoPLAY']*10 - heroYstart)
            
            animTimers['MAINtoPLAY'] -= 1
            if animTimers['MAINtoPLAY'] <= 0:
                menuState = 'PLAY'        
        
        elif animTimers['MAIN'] > 0: # Main looping animation
            if animTimers['STORY'] > 0:
                functions.drawText(s, storyString, pygame.Color('black'), (50, 50, 350, 400), \
                         basicS, True)
                s.blit(byte, (50, 450))
                s.blit(backText, (200, 450))
                
            elif animTimers['MAINtoSTORY'] > 0:
                progress = animTimers['MAINtoSTORY']*10
                s.blit(cap, (100, progress - 530))
                s.blit(wf, (200, progress - 530 + cap.get_size()[1]))
                functions.drawText(s, storyString, pygame.Color('black'), (50, progress + 50, 350, 400), \
                         basicS)
                s.blit(byte, (50, progress + 450))
                
                animTimers['MAINtoSTORY'] -= 1
                if animTimers['MAINtoSTORY'] <= 0: ## End of animation
                    animTimers['STORY'] = 1
                    backButton = Button((200, 450, backText.get_size()[0], backText.get_size()[1]), \
                                        'STORY', 'MAIN')
                    activeButtons.append(backButton)                    
            
            elif animTimers['STORYtoMAIN'] > 0:
                progress = 600 - animTimers['STORYtoMAIN']*10
                s.blit(cap, (100, progress - 530))
                s.blit(wf, (200, progress - 530 + cap.get_size()[1]))
                functions.drawText(s, storyString, pygame.Color('black'), (50, progress + 50, 350, 400), \
                         basicS)
                s.blit(byte, (50, progress + 450))
                
                animTimers['STORYtoMAIN'] -= 1
                if animTimers['STORYtoMAIN'] <= 0:
                    ## add main buttons to active button list
                    playButton = Button((200, 400, playText.get_size()[0], playText.get_size()[1]),\
                                        'MAIN', 'PLAY')
                    activeButtons.append(playButton)
                    storyButton = Button((200, 400 + storyText.get_size()[1], \
                                          storyText.get_size()[0], storyText.get_size()[1]), \
                                         'MAIN', 'STORY')
                    activeButtons.append(storyButton)                    
                
            else: # Actually on the main menu
                s.blit(cap, (100, 70))
                s.blit(wf, (200, 70 + cap.get_size()[1]))                
                
                ## Button text
                s.blit(playText, (200, 400))
                s.blit(storyText, (200, 400 + playText.get_size()[1]))
            
            # Hero
            yDiff = 50 # experiment with this value
            heroYmax = heroYmin + yDiff 
            n = yDiff * math.cos(math.radians(animTimers['MAIN']))
            heroY = heroYmax - n
            
            if animTimers['MAIN'] == 1:
                animTimers['MAIN'] = animLengths['MAIN']
            else:
                animTimers['MAIN'] -= 1
        
        s.blit(hero, (heroX, heroY))
        
    
        

menuState = 'MAIN' ## State at start of program
animLengths = {
    'MAINstart': 50,
    'MAIN': 360,
    'MAINtoPLAY': 80,
    'MAINtoSTORY': 60,
    'STORY': 0,
    'STORYtoMAIN': 60
}
animTimers = {  # MAIN will continue cycling on the Story tab
    'MAINstart': 50,
    'MAIN': 0,
    'MAINtoPLAY': 0,
    'MAINtoSTORY': 0,
    'STORY': 0,
    'STORYtoMAIN': 0
}
activeButtons = []