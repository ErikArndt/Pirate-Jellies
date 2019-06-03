import math
import pygame
import collision
import functions
import random

FREE = 0
HURT = 1
DIE = 2

class Enemy:
    ## superclass for all enemy types
    def __init__(self, startingX, startingY):
        self.x = startingX
        self.y = startingY
        self.xRad = 0
        self.yRad = 0
        self.health = 1 # default value, different for specific enemies
    
    def draw(self):
        ## placeholder
        return

    def hurt(self):
        ## placeholder
        return
    
    def die(self):
        ## placeholder
        return

class Jelly(Enemy):
    def __init__(self, startingX, startingY):
        '''
        Enemies must be initialized with starting x and y coordinates.
        '''
        self.x = startingX
        self.y = startingY
        self.xRad = 20
        self.yRad = 20
        self.angle = 0
        
        self.speedCap = 5
        self.accel = 0.1
        self.xSpeed = 0
        self.ySpeed = 0
        self.xAccel = 0
        self.yAccel = 0
        
        self.state = FREE
        self.damage = 1
        self.health = 3
        self.iFrames = 30
        self.animTimers = {
            'hurt': 0,
            'die': 100
        }
    
    def draw(self, m, debug=False):
        '''
        Consumes the current map surface. Turns the jelly to face the hero, and
        draws the jelly on the given surface.
        '''
        ## hitbox
        if debug:
            pygame.draw.rect(m, pygame.Color('yellow'), (self.x - self.xRad, self.y - self.yRad, \
                                                         self.xRad*2, self.yRad*2))            
        
        if self.state == FREE:
            ## faces hero
            if self.angle >= 45 and self.angle <= 135: # South
                m.blit(jellySprites[2], (self.x - self.xRad, self.y - self.yRad))
            elif self.angle > 135 and self.angle < 225: # West
                m.blit(jellySprites[3], (self.x - self.xRad, self.y - self.yRad))
            elif self.angle >= 225 and self.angle <= 315: # North
                m.blit(jellySprites[0], (self.x - self.xRad, self.y - self.yRad))
            else: # East
                m.blit(jellySprites[1], (self.x - self.xRad, self.y - self.yRad))
            
        elif self.state == HURT:
            ## I'm gonna reuse the basic sprites 'cause I don't know what else to do
            if self.angle >= 45 and self.angle <= 135: # South
                m.blit(jellySprites[2], (self.x - self.xRad, self.y - self.yRad))
            elif self.angle > 135 and self.angle < 225: # West
                m.blit(jellySprites[3], (self.x - self.xRad, self.y - self.yRad))
            elif self.angle >= 225 and self.angle <= 315: # North
                m.blit(jellySprites[0], (self.x - self.xRad, self.y - self.yRad))
            else: # East
                m.blit(jellySprites[1], (self.x - self.xRad, self.y - self.yRad))
                
            ## Update the animations and/or state
            if self.animTimers['hurt'] <= 0:
                self.state = FREE
            else:
                self.animTimers['hurt'] -= 1
        
        elif self.state == DIE:
            pygame.draw.rect(m, pygame.Color('yellow'), (self.x - self.xRad, self.y - self.yRad, \
                                                         self.xRad*2, self.yRad*2))
            pygame.draw.line(m, pygame.Color('red'), (self.x - self.xRad, self.y - self.yRad), \
                             (self.x + self.xRad, self.y + self.yRad), 2)
            pygame.draw.line(m, pygame.Color('red'), (self.x - self.xRad, self.y + self.yRad), \
                             (self.x + self.xRad, self.y - self.yRad), 2)
            ## Update the animations and/or state
            if self.animTimers['die'] <= 0:
                ## remove the enemy from enemies ... somehow
                return
            else:
                self.animTimers['die'] -= 1
    
    def moveToward(self, hero, walls):
        '''
        Consumes a player and a wall array, and moves the enemy toward the given 
        player. Yes, this is actually physics.
        Note: This does not check the enemy's state to see if it is allowed to
        move or not.
        '''
        self.angle = functions.angleTo(self.x, self.y, hero.x, hero.y)
        self.xAccel = self.accel * math.cos(math.radians(self.angle))
        self.yAccel = self.accel * math.sin(math.radians(self.angle))
        self.xSpeed += self.xAccel
        self.ySpeed += self.yAccel
        
        ## cap the enemy's speed
        curSpeed = math.sqrt(self.xSpeed * self.xSpeed + self.ySpeed * self.ySpeed)
        if (curSpeed > self.speedCap):
            scaleFactor = curSpeed / self.speedCap
            self.xSpeed /= scaleFactor
            self.ySpeed /= scaleFactor
        
        self.x += self.xSpeed
        if self.xSpeed > 0:
            for i in range(len(walls)):
                if collision.lineRect((walls[i].x, walls[i].y), (walls[i].x, walls[i].y+walls[i].height),\
                                      (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 1, self.xSpeed):
                    self.x = walls[i].x - self.xRad
                    self.xSpeed = 0
                    break
        elif self.xSpeed < 0:
            for i in range(len(walls)):
                if collision.lineRect((walls[i].x+walls[i].width, walls[i].y), \
                                      (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                                      (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                      3, -self.xSpeed):
                    self.x = walls[i].x + walls[i].width + self.xRad
                    self.xSpeed = 0
                    break
        self.y += self.ySpeed
        if self.ySpeed < 0:
            for i in range(len(walls)):
                if collision.lineRect((walls[i].x, walls[i].y+walls[i].height), \
                                      (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                                      (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                      0, -self.ySpeed):
                    self.y = walls[i].y + walls[i].height + self.yRad
                    self.ySpeed = 0
                    break
        elif self.ySpeed > 0:
            for i in range(len(walls)):
                if collision.lineRect((walls[i].x, walls[i].y), (walls[i].x+walls[i].width, walls[i].y),\
                                      (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                      2, self.ySpeed):
                    self.y = walls[i].y - self.yRad
                    self.ySpeed = 0
                    break
            
        self.x = round(self.x)
        self.y = round(self.y)
    
    def hurt(self, damage):
        '''
        Call when enemy is damaged. Parameter is the amount of damage the enemy
        took.
        '''
        self.health -= damage
        if self.health <= 0:
            self.die()
        else:
            self.state = HURT
            self.animTimers['hurt'] = self.iFrames
        return
    
    def die(self):
        '''
        Call when enemy health drops to 0 or lower. Plays death animation. 
        Currently does not remove enemy from enemies.
        '''
        self.state = DIE

class PirateJelly(Enemy):
    def __init__(self, startingX, startingY, enemyList):
        '''
        Enemies must be initialized with starting x and y coordinates.
        '''
        self.x = startingX
        self.y = startingY
        self.xRad = 100
        self.yRad = 75
        self.angle = 0
        self.eList = enemyList
        
        self.speedCap = 2
        self.accel = 0.1
        self.xSpeed = 0
        self.ySpeed = 0
        self.xAccel = 0
        self.yAccel = 0
        
        self.state = FREE
        self.damage = 2
        self.health = 50
        self.iFrames = 20
        self.animTimers = {
            'hurt': 0,
            'die': 100
        }
    
    def draw(self, m, debug=False):
        '''
        Consumes the current map surface. Turns the jelly to face the hero, and
        draws the jelly on the given surface.
        '''
        ## hitbox
        if debug:
            pygame.draw.rect(m, pygame.Color('yellow'), (self.x - self.xRad, self.y - self.yRad, \
                                                         self.xRad*2, self.yRad*2))            
        
        if self.state == FREE:
            ## faces hero
            if self.angle >= 45 and self.angle <= 135: # South
                m.blit(pirateSprites[2], (self.x - self.xRad, self.y - self.yRad))
            elif self.angle > 135 and self.angle < 225: # West
                m.blit(pirateSprites[3], (self.x - self.xRad, self.y - self.yRad))
            elif self.angle >= 225 and self.angle <= 315: # North
                m.blit(pirateSprites[0], (self.x - self.xRad, self.y - self.yRad))
            else: # East
                m.blit(pirateSprites[1], (self.x - self.xRad, self.y - self.yRad))
            
        elif self.state == HURT:
            ## I'm gonna reuse the basic sprites 'cause I don't know what else to do
            if self.angle >= 45 and self.angle <= 135: # South
                m.blit(pirateSprites[2], (self.x - self.xRad, self.y - self.yRad))
            elif self.angle > 135 and self.angle < 225: # West
                m.blit(pirateSprites[3], (self.x - self.xRad, self.y - self.yRad))
            elif self.angle >= 225 and self.angle <= 315: # North
                m.blit(pirateSprites[0], (self.x - self.xRad, self.y - self.yRad))
            else: # East
                m.blit(pirateSprites[1], (self.x - self.xRad, self.y - self.yRad))
                
            ## Update the animations and/or state
            if self.animTimers['hurt'] <= 0:
                self.state = FREE
            else:
                self.animTimers['hurt'] -= 1
        
        elif self.state == DIE:
            pygame.draw.rect(m, pygame.Color('yellow'), (self.x - self.xRad, self.y - self.yRad, \
                                                         self.xRad*2, self.yRad*2))
            pygame.draw.line(m, pygame.Color('red'), (self.x - self.xRad, self.y - self.yRad), \
                             (self.x + self.xRad, self.y + self.yRad), 2)
            pygame.draw.line(m, pygame.Color('red'), (self.x - self.xRad, self.y + self.yRad), \
                             (self.x + self.xRad, self.y - self.yRad), 2)
            ## Update the animations and/or state
            if self.animTimers['die'] <= 0:
                ## remove the enemy from enemies ... somehow
                return
            else:
                self.animTimers['die'] -= 1
    
    def moveToward(self, hero, walls):
        '''
        Consumes a player and a wall array, and moves the enemy toward the given 
        player. Yes, this is actually physics.
        Note: This does not check the enemy's state to see if it is allowed to
        move or not.
        '''
        self.angle = functions.angleTo(self.x, self.y, hero.x, hero.y)
        self.xAccel = self.accel * math.cos(math.radians(self.angle))
        self.yAccel = self.accel * math.sin(math.radians(self.angle))
        self.xSpeed += self.xAccel
        self.ySpeed += self.yAccel
        
        ## cap the enemy's speed
        curSpeed = math.sqrt(self.xSpeed * self.xSpeed + self.ySpeed * self.ySpeed)
        if (curSpeed > self.speedCap):
            scaleFactor = curSpeed / self.speedCap
            self.xSpeed /= scaleFactor
            self.ySpeed /= scaleFactor
        
        self.x += self.xSpeed
        if self.xSpeed > 0:
            for i in range(len(walls)):
                if collision.lineRect((walls[i].x, walls[i].y), (walls[i].x, walls[i].y+walls[i].height),\
                                      (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), 1, self.xSpeed):
                    self.x = walls[i].x - self.xRad
                    self.xSpeed = 0
                    break
        elif self.xSpeed < 0:
            for i in range(len(walls)):
                if collision.lineRect((walls[i].x+walls[i].width, walls[i].y), \
                                      (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                                      (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                      3, -self.xSpeed):
                    self.x = walls[i].x + walls[i].width + self.xRad
                    self.xSpeed = 0
                    break
        self.y += self.ySpeed
        if self.ySpeed < 0:
            for i in range(len(walls)):
                if collision.lineRect((walls[i].x, walls[i].y+walls[i].height), \
                                      (walls[i].x+walls[i].width, walls[i].y+walls[i].height),\
                                      (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                      0, -self.ySpeed):
                    self.y = walls[i].y + walls[i].height + self.yRad
                    self.ySpeed = 0
                    break
        elif self.ySpeed > 0:
            for i in range(len(walls)):
                if collision.lineRect((walls[i].x, walls[i].y), (walls[i].x+walls[i].width, walls[i].y),\
                                      (self.x-self.xRad, self.y-self.yRad, self.xRad*2, self.yRad*2), \
                                      2, self.ySpeed):
                    self.y = walls[i].y - self.yRad
                    self.ySpeed = 0
                    break
            
        self.x = round(self.x)
        self.y = round(self.y)
    
    def hurt(self, damage):
        '''
        Call when enemy is damaged. Parameter is the amount of damage the enemy
        took.
        '''
        self.health -= damage
        if self.health <= 0:
            self.die()
        else:
            if self.health in [1,2,3,4,5,7,9,11,15,20,25,30]:
                self.eList.append(Jelly(random.randint(self.x-self.xRad, self.x+self.xRad), random.randint(self.y-self.yRad, self.y+self.yRad)))
            self.state = HURT
            self.animTimers['hurt'] = self.iFrames
        return
    
    def die(self):
        '''
        Call when enemy health drops to 0 or lower. Plays death animation. 
        Currently does not remove enemy from enemies.
        '''
        self.state = DIE

## ******************** Sprites *************

jellySprites = []

pirateSprites = []

def loadSprites():
    '''
    Call this immediately after defining win
    '''
    jellySprites.extend([pygame.image.load('images/jellyU.png').convert_alpha(),
                         pygame.image.load('images/jellyR.png').convert_alpha(),
                         pygame.image.load('images/jellyD.png').convert_alpha(),
                         pygame.image.load('images/jellyL.png').convert_alpha()])
    for i in range(len(jellySprites)):
        jellySprites[i] = pygame.transform.scale(jellySprites[i], (40, 40))
    pirateSprites.extend([pygame.image.load('images/pirate_jellyU.png').convert_alpha(),
                          pygame.image.load('images/pirate_jellyR.png').convert_alpha(),
                          pygame.image.load('images/pirate_jellyD.png').convert_alpha(),
                          pygame.image.load('images/pirate_jellyL.png').convert_alpha()])
    for i in range(len(pirateSprites)):
        pirateSprites[i] = pygame.transform.scale(pirateSprites[i], (200, 150))
