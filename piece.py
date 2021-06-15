from settings import piece_types
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class Piece:
    def __init__(self, piece_type, player, row, col):
        self.piece_type = piece_type
        self.player = player
        self.row = row
        self.col = col
    # pit = destroyed
    # hero > wumpus
    # mage > hero
    # wumpus > mage
    # in other words 2>1 3>2 1>3
    # same piece = both destroyed
    def attack(self, other):
        type1 = self.piece_type
        type2 = other.piece_type
        if type1 == type2:
            return None

        wumpus = (type1==1 or type2==1)
        hero = (type1==2 or type2==2)
        mage = (type1==3 or type2==3)
        
        if hero and wumpus: # hero wins
            return self if type1==2 else other
        if mage and hero: # mage wins
            return self if type1==3 else other
        if mage and wumpus: # wumpus wins
            return self if type1==1 else other

    def __repr__(self):
        return piece_types[self.piece_type] + "-" + str(self.player)
    def __str__(self):
        return piece_types[self.piece_type] + "-" + str(self.player)
