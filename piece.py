'''
- Piece
    - _DirSpecific
        - Bishop
        - Rook
        - Queen
    - King
    - Knight
    - Pawn
'''

from __future__ import annotations

from typing import Dict, List, Set, Tuple

import board


class color:
    WHITE = 'w'
    BLACK = 'b'


opponent_dict = {
    color.WHITE: color.BLACK,
    color.BLACK: color.WHITE
}

_file_labels = list('abcdefgh')


def getEnemy(col: str):
    return opponent_dict[col]


def getAtkReg(attacker_pieces: Set, chess_board: board.Arr2D) -> Set[Tuple[int, int]]:
    '''
    Return the atack region of the {color} color.
    '''
    return set.union(*[p.atacking_region(chess_board) for p in attacker_pieces])


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

    def atacking_region(self, chess_board: board.Arr2D) -> Set[Tuple[int, int]]:
        pass

    def possible_moves():
        raise NotImplementedError

    def legal_moves():
        raise NotImplementedError

    def isPinned(self, meta: board.Board) -> bool:
        brd_without_me = meta.board.copy()
        brd_without_me[self.coord] = None
        enemy_pieces = meta.pieces_dict[getEnemy(self.color)]
        my_king_coords = meta.kings[self.color].coord
        return (my_king_coords in getAtkReg(enemy_pieces, brd_without_me))

    def __repr__(self) -> str:
        return f'{self.color.upper()}{type(self).__name__} at {self.coord}'

    def __str__(self) -> str:
        return f'{self.color.upper()}{type(self).__name__} at {alg_not_square(self.coord)}'


class _DirSpecific(Piece):

    def atacking_region(self, chess_board: board.Arr2D) -> Set[Tuple[int, int]]:
        atck_region = set()
        for direction in self.atk_direction:
            i, j = self.coord
            di, dj = direction
            while True:
                i += di
                j += dj
                if 0 <= i <= 7 and 0 <= j <= 7:
                    p = chess_board[i, j]
                    if p is None:
                        atck_region.add((i, j))
                    else:
                        atck_region.add((i, j))
                        break
                else:
                    break
        return atck_region


class Pawn(Piece):
    alg_notation = 'p'

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)

    def atacking_region(self, chess_board):
        if self.color == color.WHITE:
            atk_delta = ((-1, -1), (-1, +1))
        else:
            atk_delta = ((+1, -1), (+1, +1))
        atck_region = set()
        for di, dj in atk_delta:
            i, j = self.coord
            i += di
            j += dj
            if 0 <= i <= 7 and 0 <= j <= 7:
                atck_region.add((i, j))
        return atck_region


class Rook(_DirSpecific):
    alg_notation = 'r'
    atk_direction: List[Tuple[int, int]] = [(+1, 0), (-1, 0), (0, +1), (0, -1)]

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class Knight(Piece):
    alg_notation = 'n'
    atk_delta: List[Tuple[int, int]] = [(-2, +1), (-2, -1), (+2, +1), (+2, -1), (+1, -2), (-1, -2), (+1, +2), (-1, +2)]

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)

    def atacking_region(self, chess_board: board.Arr2D) -> Set[Tuple[int, int]]:
        atck_region = set()
        for delta in self.atk_delta:
            i, j = self.coord
            di, dj = delta
            i += di
            j += dj
            if 0 <= i <= 7 and 0 <= j <= 7:
                atck_region.add((i, j))
        return atck_region


class Bishop(_DirSpecific):
    alg_notation = 'b'
    atk_direction: List[Tuple[int, int]] = [(+1, +1), (-1, -1), (+1, -1), (-1, +1)]

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class Queen(_DirSpecific):
    alg_notation = 'q'
    atk_direction: List[Tuple[int, int]] = list(Rook.atk_direction) + list(Bishop.atk_direction)

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class King(Piece):
    alg_notation = 'k'
    atk_delta: List[Tuple[int, int]] = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)

    def atacking_region(self, chess_board: board.Arr2D) -> Set[Tuple[int, int]]:
        atck_region = set()
        for delta in self.atk_delta:
            i, j = self.coord
            di, dj = delta
            i += di
            j += dj
            if 0 <= i <= 7 and 0 <= j <= 7:
                atck_region.add((i, j))
        return atck_region


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
