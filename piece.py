from __future__ import annotations

from typing import Dict, Tuple


class color:
    WHITE = 'w'
    BLACK = 'b'


_file_labels = list('abcdefgh')


def alg_not_square(coord: Tuple[int, int]) -> str:
    '''
    Square coordinates to algebric notation.
    '''
    row, col = coord
    rank = 8-row
    file = _file_labels[col]
    return f'{file}{rank}'


def alg_not_to_coords(notation: str) -> Tuple[int, int]:
    '''
    Algebric notation to square coordinates.
    '''
    file, rank = notation
    rank = int(rank)
    return (8-rank, _file_labels.index(file.lower()))


class Piece:
    alg_notation: str = ''
    color: str
    coord: Tuple[int, int]
    moved: bool

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        self.color = color
        self.coord = coord
        self.moved = moved

    def atacking_region():
        pass

    def possible_moves():
        raise NotImplementedError

    def legal_moves():
        raise NotImplementedError

    def __repr__(self) -> str:
        return f'{self.color.upper()}{type(self).__name__} at {self.coord}'

    def __str__(self) -> str:
        return f'{self.color.upper()}{type(self).__name__} at {alg_not_square(self.coord)}'


class Pawn(Piece):
    alg_notation = 'p'

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class Rook(Piece):
    alg_notation = 'r'
    atk_direction: Tuple[Tuple[int, int]] = ((+1, 0), (-1, 0), (0, +1), (0, -1))

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class Knight(Piece):
    alg_notation = 'n'
    atk_delta: Tuple[Tuple[int, int]] = ((-2, +1), (-2, -1), (+2, +1), (+2, -1), (+1, -2), (-1, -2), (+1, +2), (-1, +2))

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class Bishop(Piece):
    alg_notation = 'b'
    atk_direction: Tuple[Tuple[int, int]] = ((+1, +1), (-1, -1), (+1, -1), (-1, +1))

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class Queen(Piece):
    alg_notation = 'q'
    atk_direction: Tuple[Tuple[int, int]] = tuple(list(Rook.atk_direction) + list(Bishop.atk_direction))

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class King(Piece):
    alg_notation = 'k'
    atk_delta: Tuple[Tuple[int, int]] = ((i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0))

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


def isEnemy(p1: Piece, p2: Piece) -> bool:
    return p1.color != p2.color


piece_dict: Dict[str, callable] = {
    'p': Pawn,
    'b': Bishop,
    'n': Knight,
    'r': Rook,
    'q': Queen,
    'k': King,
}

default_rook_postion: Dict[str, Tuple[int, int]] = {
    'k': alg_not_to_coords('h8'),
    'q': alg_not_to_coords('a8'),
    'K': alg_not_to_coords('h1'),
    'Q': alg_not_to_coords('a1'),
}

if __name__ == "__main__":
    pass
