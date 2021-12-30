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

from collections import defaultdict, namedtuple
from typing import Callable, Optional, Tuple

import board

m_move = namedtuple('m_move', ['start_pos', 'end_pos'])
m_capture = namedtuple('m_capture', ['start_pos', 'end_pos'])
m_2pawnmove = namedtuple('m_2pawnmove', ['start_pos', 'end_pos'])
m_en_passent = namedtuple('m_en_passent', ['start_pos', 'end_pos', 'target_square'])
m_prom = namedtuple('m_prom', ['start_pos', 'end_pos', 'promoted_piece'])
m_prom_cap = namedtuple('m_prom_cap', ['start_pos', 'end_pos', 'promoted_piece'])
m_castle = namedtuple('m_castle', ['king_start_pos', 'rook_start_pos', 'king_end_pos', 'rook_end_pos'])


class color:
    WHITE = 'w'
    BLACK = 'b'


opponent_dict = {
    color.WHITE: color.BLACK,
    color.BLACK: color.WHITE
}

_file_labels = list('abcdefgh')


def is_coord_in_brd(coord: Tuple[int, int]):
    x, y = coord
    if 0 <= x <= 7 and 0 <= y <= 7:
        return True
    return False


def isValidMove(move, color, meta: board.Board):
    brd = meta.board.copy()

    if isinstance(move, (m_move, m_2pawnmove, m_prom)):
        brd[move.end_pos], brd[move.start_pos] = brd[move.start_pos], None
        enemy_p = meta.pieces_dict[getEnemy(color)]
        return meta.kings[color].coord not in getAtkReg(enemy_p, brd)

    elif isinstance(move, (m_capture, m_prom_cap)):
        dead_p: Piece = brd[move.end_pos]
        brd[move.end_pos], brd[move.start_pos] = brd[move.start_pos], None
        enemy_p = meta.pieces_dict[getEnemy(color)].copy()
        enemy_p.discard(dead_p)
        return meta.kings[color].coord not in getAtkReg(enemy_p, brd)

    elif isinstance(move, m_en_passent):
        dead_p = brd[move.target_square]
        brd[move.end_pos], brd[move.start_pos], brd[move.target_square] = brd[move.start_pos], None, None
        enemy_p = meta.pieces_dict[getEnemy(color)].copy()
        enemy_p.discard(dead_p)
        return meta.kings[color].coord not in getAtkReg(enemy_p, brd)


def getEnemy(col: str):
    return opponent_dict[col]


def getAtkReg(attacker_pieces: set[Piece], chess_board: board.Arr2D) -> set[Tuple[int, int]]:
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
    file = notation[0]
    rank = int(notation[1])
    return (8-rank, _file_labels.index(file.lower()))


class Piece:
    alg_notation: str = ''
    color: str
    coord: Tuple[int, int]
    moved: bool

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = True):
        self.color = color
        self.coord = coord
        self.moved = moved

    def atacking_region(self, chess_board: board.Arr2D) -> set[Tuple[int, int]]:
        pass

    def legal_moves(self, meta: board.Board) -> list[Tuple[int, int]]:
        raise NotImplemented

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

    def atacking_region(self, chess_board: board.Arr2D) -> set[Tuple[int, int]]:
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
            if len(dir_mov_list) == 0:
                continue
            move_in_direction = dir_mov_list[0]
            if isValidMove(move_in_direction, self.color, meta):
                moves.extend(dir_mov_list)
        return moves

    def legal_moves(self, meta: board.Board) -> list[Tuple[int, int]]:
        if self.isPinned(meta):
            moves = self.move_wout_check_with_pin(meta)
        else:
            moves = self.move_wout_check_no_pin(meta)
            moves = [move for ml in moves.values() for move in ml]
        if meta.check:
            moves = [m for m in moves if isValidMove(m, self.color, meta)]
        return moves


class Pawn(Piece):
    alg_notation = 'p'
    possible_proms = ['n', 'r', 'b', 'q']

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

    def move_wout_check_no_pin(self, meta: board.Board):
        # print(self.moved)
        moves = defaultdict(list)
        i, j = self.coord
        if self.color == color.WHITE:
            ahead = -1
        else:
            ahead = +1

        if (self.color == color.WHITE and i == 1) or (self.color == color.BLACK and i == 6):
            if isEmptySquare((i+ahead, j), meta.board):
                for prom in self.possible_proms:
                    moves[(i+ahead, j)].append(m_prom((i, j), (i+ahead, j), prom))
            for di, dj in [(ahead, +1), (ahead, -1)]:
                x, y = i+di, j+dj
                if is_coord_in_brd((x, y)) and not(isEmptySquare((x,y), meta.board)) and isEnemySquare(self, (x, y), meta.board):
                    for prom in self.possible_proms:
                        moves[(x, y)].append(m_prom_cap((i, j), (x, y), prom))
        else:
            if isEmptySquare((i+ahead, j), meta.board):
                moves[(i+ahead, j)].append(m_move((i, j), (i+ahead, j)))
            for di, dj in [(ahead, +1), (ahead, -1)]:
                x, y = i+di, j+dj
                if is_coord_in_brd((x, y)) and not(isEmptySquare((x, y), meta.board)) and isEnemySquare(self, (x, y), meta.board):
                    moves[(x, y)].append(m_capture((i, j), (x, y)))
            if (meta.pawn2move is not None) and meta.pawn2move[0] == i and abs(j - meta.pawn2move[1]) == 1:
                tx, ty = meta.pawn2move
                end_pos = (tx + ahead, ty)
                moves[end_pos].append(m_en_passent((i, j), end_pos, meta.pawn2move))

        if self.moved == False:
            two_step = ahead * 2
            if isEmptySquare((i+ahead, j), meta.board) and isEmptySquare((i+two_step, j), meta.board):
                moves[(i+two_step, j)].append(m_2pawnmove((i, j), (i+two_step, j)))

        return moves

    def move_wout_check_with_pin(self, meta: board.Board):
        moves = []
        for move_list in self.move_wout_check_no_pin(meta).values():
            if isValidMove(move_list[0], self.color, meta):
                moves.extend(move_list)
        return moves

    def legal_moves(self, meta: board.Board) -> list[Tuple[int, int]]:
        if self.isPinned(meta):
            moves = self.move_wout_check_with_pin(meta)
        else:
            moves = self.move_wout_check_no_pin(meta)
            moves = [move for ml in moves.values() for move in ml]
        if meta.check:
            moves = [m for m in moves if isValidMove(m, self.color, meta)]
        return moves


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

    def move_wout_check_with_pin(self, meta):
        return []

    def legal_moves(self, meta: board.Board) -> list[Tuple[int, int]]:
        if self.isPinned(meta):
            moves = self.move_wout_check_with_pin(meta)
        else:
            moves = self.move_wout_check_no_pin(meta)
        if meta.check:
            moves = [m for m in moves if isValidMove(m, self.color, meta)]
        return moves


class Rook(_DirSpecific):
    alg_notation = 'r'
    atk_direction: list[Tuple[int, int]] = [(+1, 0), (-1, 0), (0, +1), (0, -1)]

    def __init__(self, color: str, coord: Tuple[int, int], moved: bool = False):
        super().__init__(color, coord, moved=moved)


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
    wk_route = [alg_not_to_coords(i) for i in ['f1', 'g1']]
    wk_safe_route = wk_route
    wq_route = [alg_not_to_coords(i) for i in ['b1', 'c1', 'd1']]
    wq_safe_route = [alg_not_to_coords(i) for i in ['c1', 'd1']]
    bk_route = [alg_not_to_coords(i) for i in ['f8', 'g8']]
    bk_safe_route = bk_route
    bq_route = [alg_not_to_coords(i) for i in ['b8', 'c8', 'd8']]
    bq_safe_route = [alg_not_to_coords(i) for i in ['c8', 'd8']]

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

    def move_wout_check(self, meta: board.Board):
        moves, enemy_atck_region = self.move_with_check(meta)
        if self.moved == False:
            if self.color == color.WHITE:
                p_A1 = meta.board[A1]
                p_H1 = meta.board[H1]

                if isinstance(p_H1, Rook) and not(p_H1.moved):
                    if all(isEmptySquare(i, meta.board) for i in self.wk_route):
                        if all(i not in enemy_atck_region for i in self.wk_safe_route):
                            moves.append(m_castle(self.coord, H1, alg_not_to_coords('g1'), alg_not_to_coords('f1')))

                if isinstance(p_A1, Rook) and not(p_A1.moved):
                    if all(isEmptySquare(i, meta.board) for i in self.wq_route):
                        if all(i not in enemy_atck_region for i in self.wq_safe_route):
                            moves.append(m_castle(self.coord, A1, alg_not_to_coords('c1'), alg_not_to_coords('d1')))
            else:
                p_A8 = meta.board[A8]
                p_H8 = meta.board[H8]
                if isinstance(p_H8, Rook) and not(p_H8.moved):
                    if all(isEmptySquare(i, meta.board) for i in self.bk_route):
                        if all(i not in enemy_atck_region for i in self.bk_safe_route):
                            moves.append(m_castle(self.coord, H8, alg_not_to_coords('g8'), alg_not_to_coords('f8')))

                if isinstance(p_A8, Rook) and not(p_A8.moved):
                    if all(isEmptySquare(i, meta.board) for i in self.wq_route):
                        if all(i not in enemy_atck_region for i in self.wq_safe_route):
                            moves.append(m_castle(self.coord, A8, alg_not_to_coords('c8'), alg_not_to_coords('d8')))
        return moves

    def move_with_check(self, meta: board.Board) -> Tuple[list[Tuple[int, int]], set[Tuple[int, int]]]:
        enemy_atck_region = getAtkReg(meta.pieces_dict[getEnemy(self.color)], meta.board)
        i, j = self.coord
        moves = []
        for di, dj in self.atk_delta:
            x, y = i+di, j+dj
            if is_coord_in_brd((x, y)) and ((x, y) not in enemy_atck_region):
                if isEmptySquare((x, y), meta.board):
                    moves.append(m_move((i, j), (x, y)))
                elif isEnemySquare(self, (x, y), meta.board):
                    moves.append(m_capture((i, j), (x, y)))
        return moves, enemy_atck_region

    def legal_moves(self, meta: board.Board) -> list[Tuple[int, int]]:
        if meta.check:
            moves = self.move_with_check(meta)[0]
        else:
            moves = self.move_wout_check(meta)
        return moves


def isEmptySquare(coord: Tuple[int, int], board: board.Arr2D):
    return board[coord] is None


def isEnemySquare(p1: Piece, coord: Tuple[int, int], board: list[list[Optional[Piece]]]) -> bool:
    return p1.color != board[coord].color


piece_dict: dict[str, Callable] = {
    'p': Pawn,
    'b': Bishop,
    'n': Knight,
    'r': Rook,
    'q': Queen,
    'k': King,
}

H8 = alg_not_to_coords('h8')
A8 = alg_not_to_coords('a8')
H1 = alg_not_to_coords('h1')
A1 = alg_not_to_coords('a1')

default_rook_postion: dict[str, Tuple[int, int]] = {
    'k': H8,
    'q': A8,
    'K': H1,
    'Q': A1
}

if __name__ == "__main__":
    pass
