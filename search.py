from settings import agent
from settings import advesary

def get_piece_count(pieces):
    from collections import defaultdict
    count = defaultdict(lambda:0)
    for location, piece in pieces.items():
        type = piece.piece_type
        count[type] += 1
    # print(count)
    return count

class Node:
    def __init__(self, grid, player, depth):
        self.grid = grid
        self.player = player
        self.depth = depth
        self.agent_pieces = grid.get_pieces(agent)
        self.advesary_pieces = grid.get_pieces(advesary)
        self.agent_count = get_piece_count(self.agent_pieces)
        self.advesary_count = get_piece_count(self.advesary_pieces)

        self.children = []
        self.src = None
        self.dest = None
        self.move = ""

    def alphabeta(self, alpha, beta):
        from heuristics import h2
        from settings import d
        self.calculate_children()
        self.children.sort(key=lambda child: h2(child))

        if self.depth == 0 or self.depth == 3:
            return h2(self), -1

        a = alpha
        b = beta

        # higher is better for agent, lower is better for advesary
        choice = -1 if self.player == agent else 0

        if self.player == agent:
            value = float('-inf')
            for child in self.children:
                value = max(value, child.alphabeta(a, b)[0])
                a = max(a, value)
                if a >= b:
                    choice = child
                    break
            return value, choice
        else:
            value = float('inf')
            for child in self.children:
                value = min(value, child.alphabeta(a, b)[0])
                b = min(b, value)
                if b <= a:
                    choice = child
                    break
            return value, choice

    def calculate_children(self):
        # next grids is a map from every piece to neighbors
        next_grids = self.grid.get_next_grids(agent) if self.player == agent else self.grid.get_next_grids(advesary)
        self.children = []
        for piece, neighbors in next_grids.items():
            for neighbor in neighbors:
                import copy
                child_grid = copy.deepcopy(self.grid)
                src = (piece.row, piece.col)
                dest = neighbor
                # make sure dest is an ok square to move to
                from validate import Validate
                validator = Validate(child_grid)
                if not validator.valid_square(dest, agent):
                    continue

                child_grid.move(src, dest)
                child_node = Node(child_grid, advesary if self.player == agent else agent, self.depth + 1)
                self.children.append(child_node)
                child_node.move = "from " + str(src) + " to " + str(dest)

    def __repr__(self):
        return "Node- player:{} depth:{}\n".format(self.player, self.depth)
