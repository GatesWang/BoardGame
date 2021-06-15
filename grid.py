from piece import Piece
from settings import agent
from settings import advesary
from settings import pit
from settings import d

class Grid:
    def __init__(self):
        self.grid = [[None for col in range(d)] for row in range(d)]
        self.place_pieces()
        self.place_pits()

    def place_pieces(self):
        for col in range(d):
            piece_type = (col%3)+1
            self.grid[0][col] = Piece(piece_type, agent, row=0, col=col)
            self.grid[d-1][col] = Piece(piece_type, advesary, row=d-1, col=col)

    def place_pits(self):
        import random
        for row in range(1,d-1):
            cols = random.sample(range(0,d), int((d/3)-1))
            for col in cols:
                self.grid[row][col] = pit

    def print(self):
        output = self.grid.copy()
        # insert row labels
        labels = [i for i in range(d)]

        print(" ".join(["{:<10}".format(label) for label in labels]))
        for i, row in enumerate(output):
            print(str(i) + " " + " ".join(["{:<10}".format(str(ele)) for ele in row]))

        print()

    def __str__(self):
        output = self.grid.copy()
        # insert row labels
        labels = [i for i in range(d)]

        string = " ".join(["{:<10}".format(label) for label in labels]) + "\n"
        for i, row in enumerate(output):
            string += str(i) + " " + " ".join(["{:<10}".format(str(ele)) for ele in row]) + "\n"

        string+="\n"
        return string

    def has_empty_square(self, location):
        r,c = location
        square = self.grid[r][c]
        if square is None:
            return True
        return False

    def has_pit(self, location):
        r,c = location
        square = self.grid[r][c]
        if square == pit:
            return True
        return False

    def has_player_piece(self, player, location):
        r,c = location
        piece = self.grid[r][c]
        if isinstance(piece, Piece):
            if piece.player == player:
                return True
        return False

    def get_pieces(self, player):
        pieces = {}

        for i,row in enumerate(self.grid):
            for j,square in enumerate(row):
                if isinstance(square, Piece):
                    if square.player == player:
                        pieces[(i,j)] = square
        # print(pieces)
        return pieces

    def get_neighbors(self, square):
        r,c = square
        neighbors = []
        for i in range(-1,2):
            for j in range(-1,2):
                from validate import Validate
                validator = Validate(self)
                if (i!=0 or j!=0) and validator.valid_location((r+i, c+j)):
                    neighbors.append( (r+i,c+j) )
        return neighbors

    def move(self, src, dest):
        # assume that dest can be a few things
        # empty, pit, enemy wumpus, enemy hero, enemy mage
        r,c = src
        piece = self.grid[r][c]
        self.grid[r][c] = None

        r,c = dest
        piece.row = r
        piece.col = c
        square2 = self.grid[r][c]
        # move into a pit
        if square2 == pit:
            return
        # move to an empty square
        if square2 == None:
            self.grid[r][c] = piece
            return
        # dest is an enemy piece
        self.grid[r][c] = piece.attack(square2)

    def get_next_grids(self, player):
        # assume that turn = player
        # we want to return all moves possibly made by player
        all_moves = {}
        pieces = self.get_pieces(player)
        for location, piece in pieces.items():
            moves = self.get_neighbors(location)
            all_moves[piece] = moves

        return all_moves
