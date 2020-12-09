CSC 4444: Introduction to AI
Louisiana State University Fall 2020

Contributors: Shaun Jullens, Cadin Chung, Haley Tatum, David Zazulak, Ian Chen, Royden Lynch

Running the Program:

Be sure to be in the correct working directory of the project. The project can be executed with:
> python main.py

Please use
> python main.py -h
to see relevant flags for arguments that can be passed when running the program.

Some arguments will refer you to here to see acceptable definitions.

-f coinValueFunction
There are currently only two functions to determine coin values:
1) "random" -> randomly assign coin values
2) "geometric" -> assign coin values based on a geometric distribution, shifted by 1, with p=.25
Ex: Run a game with geometric distribution of coin values.
> python main.py -f "geometric"

-a agent
There are currently three agents that can play the game:
1) "closestcoin" -> djsktras
2) "density" -> a star
3) "greedy" -> greedy best first
Ex: Run a game with only the density and greedy based agents.
> python main.py -a "density" -a "greedy"

All arguments are optional. If no arguments are passed, one run of a default game will be executed.
This game will have 50 coins generated with random values, and all three agents will play.
Ex: Run a default game. Both of the following ways achieve the same result.
> python main.py
> python main.py -n 50 -f "random" -a "closestcoin" -a "density" -a "Greedy" -ww 1200 -wh 800