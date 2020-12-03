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

red_player = pygame.image.load("red_player.png")
coin_img = pygame.image.load("coin.png")
blue_player=pygame.image.load("blue_player.png")


# In[5]:


#Coins
class Apple():
    x = 0
    y = 0
    step = 44
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y))


# In[6]:


class Coin(pygame.sprite.Sprite):
    score=0
    def __init__(self):
 
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = coin_img
        self.value= randint(1,9)
        
        #Fetch the dimensions of the coin image.
        self.rect = self.image.get_rect()
    def x(self):
        return (self.rect.x)
    def y(self):
        return (self.rect.y)
    def draw(self, surface):
        surface.blit(self.image,(self.rect.x,self.rect.y))
    


# In[7]:

coins = []
 
# This is a list of every sprite. 
# All coins and the players as well.
for i in range(50):
    # This represents a coin
    coin = Coin()
 
    # Set a random location for the coin
    coin.rect.x = randrange(0,800,44)
    coin.rect.y = randrange(0,600,44)
    
    #Set a random value for the coin
    coin.value= randint(1,10)
    
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

# In[10]:


#Blue Player
class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 0
    score=0
 
    updateCountMax = 2
    updateCount = 0
    
    def __init__(self, length):
        self.length = length
        for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
        self.targetCoin = getMostValuableCoin()

       # initial positions, no collision.
        self.x[0] = 2*44
        self.y[0] = 2*44

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0
    
    def show_score(self, surface,choice, width, height):
        score=self.score
        score_font = pygame.font.SysFont('consalas', 20)
        score_surface = score_font.render('Blue Score : ' + str(score), True, white)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (width/10, 15)
        else:
            score_rect.midtop = (width/2, height/1.25)
        surface.blit(score_surface, score_rect)
    # pygame.display.flip(

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
        dx = self.targetCoin.x()
        dy = self.targetCoin.y()
        if self.x[0]> dx:
            self.moveLeft()

        if self.x[0]< dx:
            self.moveRight()

        if self.x[0] == dx:
            if self.y[0] < dy:
                self.moveDown()

            if self.y[0] > dy:
                self.moveUp()

    def setTarget(self,target):
        self.targetCoin = target

    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i]))


# In[11]:


#Red Player
class Computer:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 0
    score=0
 
    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)

       # initial positions, no collision.
       self.x[0] = 1*44
       self.y[0] = 4*44

    def update(self):
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0

    def show_score(self, surface,choice, width, height):
        score=self.score
        score_font = pygame.font.SysFont('consalas', 20)
        score_surface = score_font.render('Red Score : ' + str(score), True, white)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (width/10, 15)
        else:
            score_rect.midtop = (width/2, height/1.25)
        surface.blit(score_surface, score_rect)
    # pygame.display.flip(
    
    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3 
    
    def target(self,dx,dy):
        if self.x[0]> dx:
            self.moveLeft()

        if self.x[0]< dx:
            self.moveRight()

        if self.x[0] == dx:
            if self.y[0] < dy:
                self.moveDown()

            if self.y[0] > dy:
                self.moveUp()

    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 


# In[12]:


class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False


# In[ ]:





# In[13]:


class App:

    windowWidth = 800
    windowHeight = 600
    player = 0
    #apple = 0
    index=0
    


    def __init__(self):
        self._running = True
        self._display_surf = None
        self._blue_surf = None
        self._red_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(1)
        #for i in range 10:
        self.apple = Apple(8,5)
        self.computer = Computer(1)

    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._blue_surf = pygame.image.load("blue_player.png").convert()
        self._red_surf = pygame.image.load("red_player.png").convert()
        self._apple_surf = pygame.image.load("coin.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
            
    def on_loop(self):

        self.computer.target(self.apple.x, self.apple.y)
        self.player.target()
        self.player.update()
        self.computer.update()
            
        # does blue eat apple?
        for i in range(0,1):#self.player.length):
            if self.game.isCollision(self.player.targetCoin.x(),self.player.targetCoin.y(),self.player.x[i], self.player.y[i],44):
                print("Coin collected!")
                coins.remove(self.player.targetCoin)
                self.player.setTarget(getMostValuableCoin())
                self.player.score = self.player.score + self.player.targetCoin.value

        # does red eat apple?
        for i in range(0,1):#self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.computer.x[i], self.computer.y[i],44):
                self.apple.x = randint(2,9) * 44
                self.apple.y = randint(2,9) * 44
                self.apple.value= randint(4,9)
                self.computer.score=self.computer.score + self.apple.value
       
        pass  
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._blue_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.computer.draw(self._display_surf, self._red_surf)
        self.computer.show_score(self._display_surf,1, self.windowWidth, self.windowHeight)
        self.player.show_score(self._display_surf,2, self.windowWidth, self.windowHeight)
        for coin in coins:
            coin.draw(self._display_surf)
        #all_sprites_list.draw(self._display_surf)
        pygame.display.flip()
   
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while self._running and self.computer.score < 100 and self.player.score <100:
            # ends loop if user quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            pygame.event.pump()
            self.on_loop()
            self.on_render()
            time.sleep (50.0 / 1000.0)
                #else:
        print("You lose! Collision: ")
        print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")" ) 
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




