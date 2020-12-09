import abc
import pygame


# Load Static Images
RED_AGENT_R_IMG     = pygame.image.load("images/red_player.png")
RED_AGENT_L_IMG     = pygame.transform.flip(RED_AGENT_R_IMG, True, False)

BLUE_AGENT_R_IMG     = pygame.image.load("images/blue_player.png")
BLUE_AGENT_L_IMG     = pygame.transform.flip(BLUE_AGENT_R_IMG, True, False)

GREEN_AGENT_R_IMG     = pygame.image.load("images/green_player.png")
GREEN_AGENT_L_IMG     = pygame.transform.flip(GREEN_AGENT_R_IMG, True, False)


"""
    General Helper Functions
"""
# find distance between an agent an a coin
def getDistanceBetween(agent, coin):
    return ((abs(agent.x - coin.x) ** 2 + abs(agent.y - coin.y) ** 2) ** .5) / 10


"""
    Generic Agent Object
"""
class Agent:
    
    # universal step size for any agent
    step = 10

    def __init__(self, color, initial_x, initial_y):
        # initial positions, no collision.
        self.color = color
        self.l_img = None
        self.r_img = None
        self.surface = None
        self.x = initial_x*40
        self.y = initial_y*40
        self.score = 0
        self.direction = 0
        self.targetCoin = None

    def update(self):
        # update position of origin point
        if self.direction == 0:
            self.x = self.x + self.step
        elif self.direction == 1:
            self.x = self.x - self.step
        elif self.direction == 2:
            self.y = self.y - self.step
        elif self.direction == 3:
            self.y = self.y + self.step
    
    def show_score(self, surface, choice, width, height, color, font):

        score_surf = font.render(self.color + " Score: " + str(self.score), True, color)
        score_rect = score_surf.get_rect()

        if choice == 1:
            score_rect.midtop = (width - width/10, 15)
        elif choice == 2:
            score_rect.midtop = (width - width/10, 30)
        else:
            score_rect.midtop = (width - width/10, 45)

        surface.blit(score_surf, score_rect)

    def moveRight(self):
        self.direction = 0
        self._surface = self.r_img.convert_alpha()

    def moveLeft(self):
        self.direction = 1
        self._surface = self.l_img.convert_alpha()

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3 

    # coin dx and dy
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

    @abc.abstractmethod
    def setTarget(self):
        """Set next coin for targeting by agent."""
        return

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


"""
    Agent 1 - Closest Coin Agent
    (Blue)
"""
class ClosestCoinAgent(Agent):

    def __init__(self, x, y, initial_coins):
        super().__init__("Blue", x, y)
        self.r_img = BLUE_AGENT_R_IMG
        self.l_img = BLUE_AGENT_L_IMG
        self._surface = None
        self.targetCoin = self.getClosestCoin(initial_coins)
    
    def setTarget(self, coins):
        self.targetCoin = self.getClosestCoin(coins)

    """
        Brain
    """
    def getClosestCoin(self, coins):
        closestCoin = coins[0]
        smallestDistance = getDistanceBetween(self, closestCoin)
        for coin in coins:
            dist = getDistanceBetween(self, coin)
            if (dist < smallestDistance):
                smallestDistance = dist
                closestCoin = coin
        return closestCoin



"""
    Agent 2 - Density Agent
    (Red)
"""
class DensityAgent(Agent):

    def __init__(self, x, y, initial_coins):
        super().__init__("Red", x, y)
        self.r_img = RED_AGENT_R_IMG
        self.l_img = RED_AGENT_L_IMG
        self._surface = None
        self.targetCoin = self.getBestCoin(initial_coins)

    def setTarget(self, coins):
        self.targetCoin = self.getBestCoin(coins)
    
    """
        Brain
    """
    def getBestCoin(self, coins): # combines distance based-approach of blue ghost with a heuristic based on a coin's proximity to other coins
        bestCoin = coins[0]
        smallestCost = getDistanceBetween(self, bestCoin)
        distanceWeight = 0.2 # used to weight each attribute (distance and density)
        densityWeight = 1.0
        for coin in coins: # finds the 'best' (aka lowest cost) coin
            currentDistance = getDistanceBetween(self, coin) * distanceWeight # distance (g)
            currentDensity = self.getDensity(coin, coins, 50) * densityWeight # heuristic (h)
            currentCost = currentDistance + currentDensity # cost (f)
            if(currentCost < smallestCost):
                smallestCost = currentCost
                bestCoin = coin
        return bestCoin

    def getDensity(self, coin, coins, distance):
        nearbyCoins = len(coins) # since we want to return a lower value for coins with lots of coins nearby, nearbyCoins starts at the total # of coins 
        for coin2 in coins: # for each coin, checks if that coin is within the given distance
            if(getDistanceBetween(coin, coin2) < distance):
                nearbyCoins-=1 # subtracts one for each coin that is nearby
        return nearbyCoins # this results in the function returning a high value for isolated coins, and a low value for coins in dense areas


"""
    Agent 3 - Greedy Agent
    (Green)
"""
class GreedyAgent(Agent):

    def __init__(self, x, y, initial_coins):
        super().__init__("Green", x, y)
        self.r_img = GREEN_AGENT_R_IMG
        self.l_img = GREEN_AGENT_L_IMG
        self._surface = None
        self.targetCoin = self.getMostValuableCoin(initial_coins)

    def setTarget(self, coins):
        self.targetCoin = self.getMostValuableCoin(coins)
    
    """
        Brain
    """
    def getMostValuableCoin(self, coins):
        mvc = coins[0]
        for coin in coins:
            if coin.value > mvc.value:
                mvc = coin
            elif coin.value == mvc.value:
                # compare distance and target the closer one
                prevDist = getDistanceBetween(self, mvc)
                newDist = getDistanceBetween(self, coin)
                if newDist < prevDist:
                    mvc = coin
        return mvc