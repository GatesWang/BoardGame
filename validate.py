from settings import d
from settings import agent
from settings import advesary

class Validate:
    def __init__(self, grid):
        self.grid = grid

    # return true if the move is the proper distance
    def valid_move(self, src, dest):
        r1,c1 = src
        r2,c2 = dest
        d_r = abs(r1-r2)
        d_c = abs(c1-c2)
        if d_r>1 or d_c>1:
            return False
        return True

    # return true if location is in bounds
    def valid_location(self, location):
        r,c = location
        if r<0 or r>d-1:
            return False
        if c<0 or c>d-1:
            return False
        return True

    # return true if location has a player piece
    def valid_piece(self, location, player):
        return self.grid.has_player_piece(player=player, location=location)

    # return true if location is a valid square to move to for player
    def valid_square(self, location, player):
        opponent = agent if player == advesary else advesary
        capture = self.grid.has_player_piece(player=opponent, location=location)
        empty = self.grid.has_empty_square(location)
        is_pit = self.grid.has_pit(location)
        return (capture or empty or is_pit)

    def get_input(self):
        src = (-1, -1)
        dest = (-1, -1)

        while True:
            while True:
                print("Enter the location of the piece you want to move")
                r = input("row: ")
                c = input("col: ")
                src = (int(r),int(c))
                location_ok = self.valid_location(src)
                if not location_ok:
                    print("That is not inside the grid")
                    continue
                piece_ok = self.valid_piece(src, advesary)
                if not piece_ok:
                    print("That square does not contain a piece")
                    continue
                if location_ok and piece_ok:
                    break

            while True:
                print("Enter where you want to move to: ")
                r = input("row: ")
                c = input("col: ")
                dest = (int(r),int(c))
                location_ok = self.valid_location(dest)
                if not location_ok:
                    print("That is not inside the grid")
                    continue
                square_ok = self.valid_square(dest, advesary)
                if not square_ok:
                    print("That is not a valid destination")
                    continue
                if location_ok and square_ok:
                    break

            if self.valid_move(src, dest):
                break
            print("That is not a valid move")

        return src, dest
