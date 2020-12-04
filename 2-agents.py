#!/usr/bin/env python
# coding: utf-8

# In[3]:


from pygame.locals import *
from random import randint, randrange
import pygame
import time
import sys
import os


# In[4]:



white = 255,255,255
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

red_player = pygame.image.load("images/red_player.png")
coin_img = pygame.image.load("images/coin.png")
blue_player=pygame.image.load("images/blue_player.png")


class Coin():
    score=0
    def __init__(self,x,y):
        self.image = coin_img
        self.value= 1
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.image,(self.x,self.y))
    


# In[7]:

coins = []
windowWidth = 1200
windowHeight = 800
 
# This is a list of every sprite. 
# All coins and the players as well.
for i in range(50):
    # This represents a coin
    coin = Coin(randrange(0,windowWidth,40),randrange(0,windowHeight,40))    
    
    # Add the coin to the list of objects
    coins.append(coin)

def getMostValuableCoin():
    mvc = coins[0]
    for coin in coins:
        if coin.value > mvc.value:
            mvc = coin
            if mvc.value == 10:
                return mvc
    print(mvc.value)
    return mvc

def getClosestCoin(player):
    closestCoin = coins[0]
    smallestDistance = getDistanceBetween(player, closestCoin)
    for coin in coins:
        currentDistance = getDistanceBetween(player, coin)
        if(currentDistance < smallestDistance):
            smallestDistance = currentDistance
            closestCoin = coin
    return closestCoin

def getBestCoin(player): # combines distance based-approach of blue ghost with a heuristic based on a coin's proximity to other coins
    bestCoin = coins[0]
    smallestCost = getDistanceBetween(player, bestCoin)
    distanceWeight = 0.2 # used to weight each attribute (distance and density)
    densityWeight = 1.0
    for coin in coins: # finds the 'best' (aka lowest cost) coin
        currentDistance = getDistanceBetween(player, coin) * distanceWeight # distance (g)
        currentDensity = getDensity(coin,50) * densityWeight # heuristic (h)
        currentCost = currentDistance + currentDensity # cost (f)
        if(currentCost < smallestCost):
            smallestCost = currentCost
            bestCoin = coin
    return bestCoin

def getDistanceBetween(player, coin):
    return ((abs(player.x - coin.x) ** 2 + abs(player.y - coin.y) ** 2) ** .5) / 10

def getDensity(coin,distance):
    nearbyCoins = len(coins) # since we want to return a lower value for coins with lots of coins nearby, nearbyCoins starts at the total # of coins 
    for coin2 in coins: # for each coin, checks if that coin is within the given distance
        if(getDistanceBetween(coin,coin2) < distance):
            nearbyCoins-=1 # subtracts one for each coin that is nearby
    return nearbyCoins # this results in the function returning a high value for isolated coins, and a low value for coins in dense areas

# In[10]:


#Blue Player
class Player:
    
    step = 10

    def __init__(self,x,y):
       # initial positions, no collision.
        self.x = x*40
        self.y = y*40
        self.score = 0
        self.direction = 0
        self.targetCoin = getClosestCoin(self)

    def update(self):
        # update position of head of snake
        if self.direction == 0:
            self.x = self.x + self.step
        elif self.direction == 1:
            self.x = self.x - self.step
        elif self.direction == 2:
            self.y = self.y - self.step
        elif self.direction == 3:
            self.y = self.y + self.step
    
    def show_score(self, surface,choice, width, height):
        score=self.score
        score_font = pygame.font.SysFont('consalas', 20)
        score_surface = score_font.render('Blue Score : ' + str(score), True, white)
        score_rect = score_surface.get_rect()
        choice = 1
        if choice == 1:
            score_rect.midtop = (width - width/10, 15)
        else:
            score_rect.midtop = (width/2, height/1.25)
        surface.blit(score_surface, score_rect)

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3 

    #coin dx and dy
    def target(self):
        dx = self.targetCoin.x
        dy = self.targetCoin.y
        if self.x > dx:
            self.moveLeft()

        if self.x < dx:
            self.moveRight()

        if self.x == dx:
            if self.y < dy:
                self.moveDown()

            if self.y > dy:
                self.moveUp()

    def setTarget(self):
        self.targetCoin = getClosestCoin(self)

    def draw(self, surface, image):
        surface.blit(image,(self.x,self.y))

class SmartPlayer(Player):
    def __init__(self,x,y):
        super().__init__(x,y)
    def setTarget(self):
        self.targetCoin = getBestCoin(self)
    def show_score(self, surface,choice, width, height):
        score=self.score
        score_font = pygame.font.SysFont('consalas', 20)
        score_surface = score_font.render('Red Score : ' + str(score), True, white)
        score_rect = score_surface.get_rect()
        choice = 0
        if choice == 1:
            score_rect.midtop = (width - width/10, 15)
        else:
            score_rect.midtop = (width/10, 15)
        surface.blit(score_surface, score_rect)

# In[13]:


class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._blue_surf = None
        self._red_surf = None
        self._apple_surf = None
        self.player = Player(8,2)
        self.computer = SmartPlayer(9,2)

    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((windowWidth,windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._blue_surf = pygame.image.load("images/blue_player.png").convert()
        self._red_surf = pygame.image.load("images/red_player.png").convert()
        self._apple_surf = pygame.image.load("images/coin.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
            
    def on_loop(self):

        self.computer.target()
        self.player.target()
        self.player.update()
        self.computer.update()
            
        # does blue eat apple?
        if self.player.x == self.player.targetCoin.x and self.player.y == self.player.targetCoin.y:
            self.player.score = self.player.score + self.player.targetCoin.value
            if self.player.x == self.computer.x and self.player.y == self.computer.y:
                self.computer.score = self.computer.score + self.computer.targetCoin.value
            if(len(coins) > 1):
                print("Coin collected!")
                coins.remove(self.player.targetCoin)
                self.player.setTarget()
                self.computer.setTarget()
            else:
                self._running = False

        # does red eat apple?
        if self.computer.x == self.computer.targetCoin.x and self.computer.y == self.computer.targetCoin.y:
            self.computer.score = self.computer.score + self.computer.targetCoin.value
            if(len(coins) > 1):
                print("Coin collected!")
                coins.remove(self.computer.targetCoin)
                self.player.setTarget()
                self.computer.setTarget()
            else:
                self._running = False
       
        pass  
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        for coin in coins:
            coin.draw(self._display_surf)
        self.player.draw(self._display_surf, self._blue_surf)
        self.computer.draw(self._display_surf, self._red_surf)
        self.computer.show_score(self._display_surf,1, windowWidth, windowHeight)
        self.player.show_score(self._display_surf,2, windowWidth, windowHeight)
        pygame.display.flip()
   
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while self._running and self.computer.score < 1000 and self.player.score < 1000:
            # ends loop if user quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            pygame.event.pump()
            self.on_loop()
            self.on_render()
            time.sleep (50.0 / 1000.0)
                #else:
        if self.player.score > self.computer.score:
            print("Blue player wins! " + str(self.player.score) + " : " + str(self.computer.score))
        elif self.player.score < self.computer.score:
            print("Red player wins! " + str(self.computer.score) + " : " + str(self.player.score))
        else:
            print("Tie! " + str(self.player.score) + " : " + str(self.computer.score))
        exit(0)
        self.on_cleanup()


# In[ ]:





# In[ ]:




#The cell below will execute the program and start the game.
# In[ ]:


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()


# In[ ]:


quit()


# In[ ]:




