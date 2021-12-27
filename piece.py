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

from collections import namedtuple
from typing import Dict, Optional, Set, Tuple

import board

m_move = namedtuple('move', ['start_pos', 'end_pos'])
m_capture = namedtuple('capture', ['start_pos', 'end_pos'])


class color:
    WHITE = 'w'
    BLACK = 'b'


opponent_dict = {
    color.WHITE: color.BLACK,
    color.BLACK: color.WHITE
}

_file_labels = list('abcdefgh')


def isValidMove():
    pass


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

    def move_wout_check_no_pin(self, meta: board.Board) -> dict[Tuple[int, int], list[m_move | m_capture]]:
        moves: dict[Tuple[int, int], list[m_move | m_capture]] = {}
        brd = meta.board
        for direction in self.atk_direction:
            moves[direction] = []
            i, j = self.coord
            di, dj = direction
            while True:
                i += di
                j += dj
                if 0 <= i <= 7 and 0 <= j <= 7:
                    if isEmptySquare((i, j), brd):
                        moves[direction].append(m_move(self.coord, (i, j)))
                    elif isEnemySquare(self, (i, j), brd):
                        moves[direction].append(m_capture(self.coord, (i, j)))
                        break
                    else:
                        break
                else:
                    break
        return moves

    def move_wout_check_with_pin(self, meta: board.Board) -> list[Tuple[int, int]]:
        moves_wout_pin = self.move_wout_check_no_pin(meta)
        moves = []
        for dir_mov_list in moves_wout_pin.values():
            dir_mov_list


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
    atk_direction: list[Tuple[int, int]] = [(+1, 0), (-1, 0), (0, +1), (0, -1)]

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class Knight(Piece):
    alg_notation = 'n'
    atk_delta: list[Tuple[int, int]] = [(-2, +1), (-2, -1), (+2, +1), (+2, -1), (+1, -2), (-1, -2), (+1, +2), (-1, +2)]

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)

    def atacking_region(self, chess_board: board.Arr2D) -> set[Tuple[int, int]]:
        atck_region = set()
        for delta in self.atk_delta:
            i, j = self.coord
            di, dj = delta
            i += di
            j += dj
            if 0 <= i <= 7 and 0 <= j <= 7:
                atck_region.add((i, j))
        return atck_region

    def move_wout_check_no_pin(self, meta: board.Board) -> list[Tuple[int, int]]:
        moves = []
        brd = meta.board
        for delta in self.atk_delta:
            i, j = self.coord
            di, dj = delta
            i += di
            j += dj
            if 0 <= i <= 7 and 0 <= j <= 7:
                if isEmptySquare((i, j), brd):
                    moves.append(m_move(self.coord, (i, j)))
                elif isEnemySquare(self, (i, j), brd):
                    moves.append(m_capture(self.coord, (i, j)))
        return moves

    def move_wout_check_with_pin(self):
        return []

    def legal_moves():
        pass


class Bishop(_DirSpecific):
    alg_notation = 'b'
    atk_direction: list[Tuple[int, int]] = [(+1, +1), (-1, -1), (+1, -1), (-1, +1)]

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class Queen(_DirSpecific):
    alg_notation = 'q'
    atk_direction: list[Tuple[int, int]] = list(Rook.atk_direction) + list(Bishop.atk_direction)

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


class King(Piece):
    alg_notation = 'k'
    atk_delta: list[Tuple[int, int]] = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]

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


def isEmptySquare(coord: Tuple[int, int], board: board.Arr2D):
    return board[coord] is None


def isEnemySquare(p1: Piece, coord: Tuple[int, int], board: list[list[Optional(Piece)]]):
    return p1.color != board[coord].color


piece_dict: dict[str, callable] = {
    'p': Pawn,
    'b': Bishop,
    'n': Knight,
    'r': Rook,
    'q': Queen,
    'k': King,
}

default_rook_postion: dict[str, Tuple[int, int]] = {
    'k': alg_not_to_coords('h8'),
    'q': alg_not_to_coords('a8'),
    'K': alg_not_to_coords('h1'),
    'Q': alg_not_to_coords('a1'),
}

if __name__ == "__main__":
    pass
