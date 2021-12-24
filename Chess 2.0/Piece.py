class Piece:
    name: str
    color: str
    coord: tuple[int, int]
    bHas_moved: bool # Used for castling and Pawn movement
    def __init__(self, name: str, coord: tuple[int, int]):
        self.name = name
        self.coord = coord
        self.bHas_moved = False

class Pawn(Piece):
    pass

class Rook(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Queen(Piece):
    pass

class King(Piece):
    pass
