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
coin_img = pygame.image.load("img/coin.png")
blue_player=pygame.image.load("img/blue_player.png")


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
    def __init__(self, image):
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = image
        self.value= randint(1,9)
        
        #Fetch the dimensions of the coin image.
        self.rect = self.image.get_rect()
    def x(self):
        return (self.rect.x)
    def y(self):
        return (self.rect.y)


# In[7]:


coin_list = pygame.sprite.Group()
 
# This is a list of every sprite. 
# All coins and the players as well.
all_sprites_list = pygame.sprite.Group()
coin_values=[]
for i in range(50):
    # This represents a coin
    coin = Coin(coin_img)
 
    # Set a random location for the coin
    coin.rect.x = randrange(800)
    coin.rect.y = randrange(600)
    
    #Set a random value for the coin
    coin.value= randint(1,10)
    
    # Add the coin to the list of objects
    coin_list.add(coin)
    all_sprites_list.add(coin)
    coin_values.append(coin.value)


# In[8]:


class my_dictionary(dict):  
  
    # __init__ function  
    def __init__(self):  
        self = dict()  
          
    # Function to add key:value  
    def add(self, key, value):  
        self[key] = value  


# In[9]:


value_coordinates = my_dictionary() 
value_max=10

coin_list_2 = coin_list

#Loop through all the coins. Find coins of highest value and add to dictionary value_coordinates in order of value. 
#Remove from coin_values.
while value_max >0:
    for coin in coin_list_2:
        #print(coin.value, coin.rect.x, coin.rect.y)
        if (coin.value==value_max):
            index = coin_values.index(coin.value)
            coin_values.pop(index)
            #print(coin_values)
            #coin_list_2.pop(coin)
            value_coordinates.add(coin.rect.x,coin.rect.y)
    
    value_max = value_max-1
      
#Create a list of tuples for each dictionary item
red_target_list = [(k, v) for k, v in value_coordinates.items()] 
index=0
list = red_target_list[index]
print(red_target_list)
x=0
y=1
print(list[x])
print(list[y])

index+=1
list = red_target_list[index]


print(list[x])
print(list[y])


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
        self._blue_surf = pygame.image.load("img/blue_player.png").convert()
        self._red_surf = pygame.image.load("red_player.png").convert()
        self._apple_surf = pygame.image.load("img/coin.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
            
    def on_loop(self):
        index=0
        list = red_target_list[index]
        #print(red_target_list)
        x1=0
        y1=1
        first=list[x1]
        second=list[y1]
        #list = red_target_list[index]
        #Here we set the target value for the player and computer
        #list = red_target_list[index]
        self.computer.target(self.apple.x, self.apple.y)
        self.player.target(first, second)
        self.player.update()
        self.computer.update()
            
        # does blue eat apple?
        for i in range(0,1):#self.player.length):
            if self.game.isCollision(first,second,self.player.x[i], self.player.y[i],44):
                index +=1
                list = red_target_list[index]
                print(index)
                print(first)
                print(second)
                #self.apple.x = randint(2,9) * 44
                #self.apple.y = randint(2,9) * 44
                #self.apple.value=randint(1,9)
                #player_score+=1
                #self.player.length = self.player.length + 1
                self.player.score = self.player.score + randint(0,5)

        # does red eat apple?
        for i in range(0,1):#self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,self.computer.x[i], self.computer.y[i],44):
                self.apple.x = randint(2,9) * 44
                self.apple.y = randint(2,9) * 44
                self.apple.value= randint(4,9)
                #print(index)
                #print(list[0])
                #print(list[1])
                
                self.computer.score=self.computer.score + self.apple.value
                
            #print(list[0])
            #print(list[1])
                #computer_score+=1
                #self.computer.length = self.computer.length + 1
                
                
        #for i in range(2,self.player.length):
            #if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                #print("You lose! Collision: ")
               # print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")" ) 
                #print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")" ) 
               # exit(0)
       
        pass  
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._blue_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        self.computer.draw(self._display_surf, self._red_surf)
        self.computer.show_score(self._display_surf,1, self.windowWidth, self.windowHeight)
        self.player.show_score(self._display_surf,2, self.windowWidth, self.windowHeight)
        all_sprites_list.draw(self._display_surf)
        pygame.display.flip()
   
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
                while (self.computer.score < 100 and self.player.score <100):
                    pygame.event.pump()
                    self.on_loop()
                    self.on_render()
                    time.sleep (50.0 / 1000.0);
                else:
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




