
from pygame.locals import *

import pygame
import random
import time

from agents import ClosestCoinAgent, DensityAgent, GreedyAgent


# Colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

# Load Images
coin_img = pygame.image.load("images/coin.png")


"""
    Coin Object
"""
class Coin():
    
    def __init__(self, x, y, value):
        self.img = coin_img
        self._surface = None
        self.x = x
        self.y = y
        self.value = value

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))


"""
    Main Game Object
"""
class Game:

    def __init__(self, numCoins, windowWidth=1200, windowHeight=800):
        # internal
        self._running       = None

        # settings
        self.numCoins     = numCoins
        self.windowWidth  = windowWidth
        self.windowHeight = windowHeight

        # sprites
        self.coins = []
        self.agents = {
            "Blue":     None,
            "Red":      None,
            "Green":    None
        }

        # display
        self._display_surf  = None

    def on_init(self):
        # initialize pygame
        pygame.init()
        self.font = pygame.font.SysFont('consalas', 20)
        self._running = True

        # initialize coins
        for _ in range(self.numCoins):
            x = random.randrange(0,self.windowWidth,40)
            y = random.randrange(0,self.windowHeight,40)
            value = random.randint(1, 7)
            self.coins.append(Coin(x, y, value))

        # initialize agents
        self.agents["Blue"]  = ClosestCoinAgent(8, 2, self.coins)
        self.agents["Red"]   = DensityAgent(9, 2, self.coins)
        self.agents["Green"] = GreedyAgent(10, 2, self.coins)

        # initialize window / surfaces
        pygame.display.set_caption("CSC 4444 - AI Pathfinding Algorithms")
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        self._coin_surface = coin_img.convert()
        for _, agent in self.agents.items():
            agent._surface = agent.img.convert()


    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
            
    def on_loop(self):
        # update 
        for _, agent in self.agents.items():
            agent.setTarget(self.coins)
        # update target direction for each agent
        for _, agent in self.agents.items():
            agent.target()
        # update location of each agent
        for _, agent in self.agents.items():
            agent.update()
        # check for collection of coins
        for coin in self.coins:
            for key, agent in self.agents.items():
                if agent.x == coin.x and agent.y == coin.y:
                    agent.score += coin.value
                    print(key + " collected a coin with a value of " + str(coin.value) + "!")
                    if coin in self.coins:
                        self.coins.remove(coin)
                    agent.setTarget(self.coins)
        # check if last coin was collected
        if not len(self.coins) > 1:
            self._running = False
    
    def on_render(self):
        # render bg
        self._display_surf.fill(BLACK)
        # render coins
        for coin in self.coins:
            coin.draw(self._display_surf)
        # render agents
        for _, agent in self.agents.items():
            agent.draw(self._display_surf, agent._surface)
        # render scores
        i=1
        for _, agent in self.agents.items():
            agent.show_score(self._display_surf, i, self.windowWidth, self.windowHeight, WHITE, self.font)
            i+=1
        # update display
        pygame.display.flip()
   
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        # check for init failure
        if self.on_init() == False:
            self._running = False
 
        # main loop
        while self._running:
            # ends loop if user quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
            pygame.event.pump()
            self.on_loop()
            self.on_render()
            time.sleep (50.0 / 1000.0)
            #    #else:

        # find winner
        winner = self.agents["Blue"]
        if self.agents["Red"].score > winner.score:
            winner = self.agents["Red"]
            if self.agents["Green"].score > winner.score:
                winner = self.agents["Green"]
        elif self.agents["Green"].score > winner.score:
            winner = self.agents["Green"]
        # log winner
        print(winner.color + " wins with a score of " + str(winner.score) + "!")

        # cleanup
        self.on_cleanup()