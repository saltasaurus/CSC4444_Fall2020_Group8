import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import argparse

from game import Game

if __name__ == "__main__" :

    # prog start logging
    print("############################################")
    print("# CSC 4444                                 #")
    print("# Coin Collection Game                     #")
    print("# For Developing AI Pathfinding Algorithms #")
    print("############################################")

    # arg parser
    parser = argparse.ArgumentParser(description="Play the game with artificial intelligence.")

    # add arguments
    parser.add_argument("-n", metavar="", type=int, help="the number of coins to generate in the game", default=50)
    parser.add_argument("-f", metavar="", type=str, help="the function by which to determine coin values, see README for list of acceptable functions", default="random")
    parser.add_argument("-a", metavar="", type=str, help="ai agent to play the game, see README for list of acceptable agents", action="append")
    parser.add_argument("-ww", metavar="", type=int, help="width of the window", default=1200)
    parser.add_argument("-wh", metavar="", type=int, help="height of the window", default=800)

    # parse arguments
    args = parser.parse_args()
    numCoins            = args.n
    coinValueFunction   = args.f
    agents              = args.a
    width               = args.ww
    height              = args.wh

    # safety check for argument validity
    if numCoins < 10:
        raise Exception("Illegal Argument Exception: numCoins cannot be less than 10.")
    if coinValueFunction not in ["random", "geometric"]:
        raise Exception("Illegal Argument Exception: coinValueFunction not recognized. See README for acceptable functions.")
    if agents == None:
        agents = ["closestcoin", "density", "greedy"]
    if len(agents) < 1:
        raise Exception("Illegal Argument Exception: there must be at least one agent.")
    for agent in agents:
        if agent not in ["closestcoin", "density", "greedy"]:
            raise Exception("Illegal Argument Exception: agent not recognized. See README for acceptable agents.")
    if width <= 0 or height <= 0:
        raise Exception("Illegal Argument Exception: window width or height cannot be less than or equal to 0.")

    # execute game
    game = Game(numCoins=numCoins, coinValueFunction=coinValueFunction, agents=agents, windowWidth=width, windowHeight=height)
    game.on_execute()

    # prog end logging
    print("############################################")
    print("# Thanks for executing!                    #")
    print("############################################")