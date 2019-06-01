import math
import pygame
import collision
import functions

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
        
        self.speedCap = 5
        self.accel = 0.1
        self.xSpeed = 0
        self.ySpeed = 0
        self.xAccel = 0
        self.yAccel = 0
        
        self.state = FREE
        self.damage = 1
        self.health = 3
        self.animTimers = {
            'hurt': 0,
            'die': 100
        }
    
    def draw(self, m):
        '''
        Consumes the current map surface.
        '''
        if self.state == FREE:
            pygame.draw.rect(m, pygame.Color('yellow'), (self.x - self.xRad, self.y - self.yRad, \
                                                         self.xRad*2, self.yRad*2))
        elif self.state == HURT:
            pygame.draw.rect(m, (255, 255, 5 + 25*self.animTimers['hurt']), \
                             (self.x - self.xRad, self.y - self.yRad, self.xRad*2, self.yRad*2))
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
        angle = functions.angleTo(self.x, self.y, hero.x, hero.y)
        self.xAccel = self.accel * math.cos(math.radians(angle))
        self.yAccel = self.accel * math.sin(math.radians(angle))
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
            self.animTimers['hurt'] = 10
        return
    
    def die(self):
        '''
        Call when enemy health drops to 0 or lower. Plays death animation. 
        Currently does not remove enemy from enemies.
        '''
        self.state = DIE
