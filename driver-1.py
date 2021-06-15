from settings import agent
from settings import advesary
from settings import d

from grid import Grid
from piece import Piece
from search import Node
from validate import Validate

grid = Grid()
grid.print()
validator = Validate(grid)
node = Node(grid, advesary, 0)
your_move = ""

def wait_for_adversary_move():
    global node
    global grid
    global validator
    global your_move
    validator = Validate(grid)
    src, dest = validator.get_input()
    grid.move(src, dest)
    your_move = "moved from {} to {}".format(src, dest)
    node = Node(grid, agent, 0)

def make_agent_move():
    global node
    global grid
    global your_move
    value, choice = node.alphabeta(float('-inf'), float('inf'))
    node = node.children[choice]
    grid = node.grid
    import os
    os.system("cls")
    print("you made a move")
    print(your_move)
    print("agent made a move")
    print(node.move)

def game_loop():
    # if all pieces are destroyed opponent wins
    # both have no pieces = draw
    turn = advesary
    agent_count = d
    advesary_count = d
    while agent_count>0 and advesary_count>0:
        if turn == advesary:
            wait_for_adversary_move()
            turn = agent
        else:
            make_agent_move()
            turn = advesary

        # update counts
        global grid
        agent_count = len(grid.get_pieces(agent))
        advesary_count = len(grid.get_pieces(advesary))
        grid.print()

    if agent_count > 0:
        print("agent won")
    elif advesary_count > 0:
        print("you won")
    else:
        print("draw")

game_loop()
