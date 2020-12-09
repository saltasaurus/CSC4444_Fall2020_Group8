
from pygame.locals import *

import pygame
import random
import time
import numpy as np

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

    def __init__(self, numCoins, coinValueFunction, agents, windowWidth, windowHeight):
        # internal
        self._running       = None

        # settings
        self.numCoins           = numCoins
        self.coinValueFunction  = coinValueFunction
        self.agents             = agents
        self.windowWidth        = windowWidth
        self.windowHeight       = windowHeight

        # sprites
        self.coins = []
        self.agents = agents

        # display
        self._display_surf  = None
    
    def initialize_coins(self):
        # compute geometric
        p = 0.25 # pval -> must change internally
        g = np.random.geometric(p, size=self.numCoins) - 1
        # initialize coins
        for i in range(self.numCoins):
            x = random.randrange(0,self.windowWidth,40)
            y = random.randrange(0,self.windowHeight,40)
            # randomly selected values
            if self.coinValueFunction == "random":
                value = random.randint(1, 7)
            # geometric distribution of values
            elif self.coinValueFunction == "geometric":
                value = g[i]
            # safety catch incorrect argument
            else:
                raise Exception("Unrecognized coin value function.")
            self.coins.append(Coin(x, y, value))
    
    def parse_agents(self):
        agentsTemp = self.agents
        self.agents = {}
        # iterate through agents
        for agent in agentsTemp:
            # pick a random spawn location
            x = random.randrange(0,self.windowWidth,40)
            y = random.randrange(0,self.windowHeight,40)
            # initialize agent
            if agent == "closestcoin":
                self.agents[agent] = ClosestCoinAgent(8, 2, self.coins)
                continue
            if agent == "density":
                self.agents[agent] = DensityAgent(9, 2, self.coins)
                continue
            if agent == "greedy":
                self.agents[agent] = GreedyAgent(10, 2, self.coins)
                continue 


    def on_init(self):
        # initialize pygame
        pygame.init()
        self.font = pygame.font.SysFont('consalas', 20)
        self._running = True

        # initialize coins
        self.initialize_coins()

        # initialize agents
        self.parse_agents()

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
                        # if this was the last coin, then game over
                        if len(self.coins) == 0:
                            self._running = False
                            continue
                    agent.setTarget(self.coins)
    
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

        # separate game logs from final to make it pretty
        print("############################################")

        # show final scores and find winner
        print("Final Scores: ")
        winner_key = None
        winner = None
        winner_score = -1
        for key, agent in self.agents.items():
            print(key + "("+agent.color+") | Score: " + str(agent.score))
            if agent.score > winner_score:
                winner_key = key
                winner = agent
                winner_score = agent.score
        # log winner and rest of the scores
        print(winner_key + "("+winner.color+") wins with a score of " + str(winner.score) + "!")

        # cleanup
        self.on_cleanup()