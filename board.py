from __future__ import annotations

from collections import namedtuple
from typing import Optional, Tuple

import piece


class InvalidFEN(Exception):
    pass


BOARD_START_POS = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0'
_FEN = namedtuple('FEN', ['board', 'turn', 'castle', 'pawn2move', 'halfmove', 'fullmove'])
_EMPTY_CHAR = '·'


class Arr2D:
    '''
    Class to maintain 2D arrays.
    Has custom getitem and setitem methods to allow tuples for indexing.
    '''

    def __init__(self, arr) -> None:
        self._arr = arr

    def __getitem__(self, index: tuple) -> object:
        r, c = index
        return self._arr[r][c]

    def __setitem__(self, index: tuple, val: object) -> None:
        r, c = index
        self._arr[r][c] = val

    def __str__(self) -> str:
        return '\n'.join(str(row) for row in self._arr)

    def __iter__(self):
        return iter(self._arr)

    def copy(self) -> Arr2D:
        return Arr2D([row.copy() for row in self._arr])

    @classmethod
    def fromSize(cls, rows: int, cols: int):
        return cls([[0 for _ in range(cols)] for _ in range(rows)])


def FEN_parser(FENstring: str) -> _FEN:
    fields = FENstring.split()
    fields = fields + (['-'] * (6 - len(fields)))
    rows = fields[0].split('/')
    board = []

    for row_string in rows:
        row = []
        for char in row_string:
            if char.isdigit():
                row.extend([_EMPTY_CHAR for _ in range(int(char))])
            else:
                row.append(char)
        board.append(row)
    board = Arr2D(board)
    return _FEN(board, *fields[1:])


class Board:
    board: Arr2D
    turn: str
    half_move: int
    fullmove: int
    pawn2move: Optional(Tuple[int, int])
    kings: dict[str, piece.King]
    pieces_dict: dict[str, set[piece.Piece]]
    check: bool

    def __init__(self, starting_positing: str = BOARD_START_POS):
        self.board = Arr2D.fromSize(8, 8)
        self.pieces_dict = {piece.color.WHITE: set(), piece.color.BLACK: set()}
        self.kings = {}

        self.load_board_from_FEN(starting_positing)

    def load_board_from_FEN(self, fenstring: str):
        parsed_fen = FEN_parser(fenstring)

        if parsed_fen.turn == '-':
            self.turn = piece.color.WHITE
        elif parsed_fen.turn.lower() == 'w':
            self.turn = piece.color.WHITE
        elif parsed_fen.turn.lower() == 'b':
            self.turn = piece.color.BLACK
        else:
            raise InvalidFEN("Turn only takes arguments: '-', 'w', 'b'}")

        if parsed_fen.halfmove == '-':
            self.half_move = 0
        elif parsed_fen.halfmove.isnumeric():
            self.half_move = int(parsed_fen.halfmove)
        else:
            raise InvalidFEN("halfmove should either be int or '-'")

        if parsed_fen.fullmove == '-':
            self.fullmove = 0
        elif parsed_fen.fullmove.isnumeric():
            self.fullmove = int(parsed_fen.fullmove)
        else:
            raise InvalidFEN("fullmove should either be int or '-'")

        if parsed_fen.pawn2move == '-':
            self.pawn2move = None
        else:
            self.pawn2move = piece.alg_not_to_coords(parsed_fen.pawn2move)

        for row, col in ((x, y) for x in range(8) for y in range(8)):
            p: str = parsed_fen.board[row, col]
            if p == _EMPTY_CHAR:
                self.board[row, col] = None
            else:
                if p.isupper():
                    color = piece.color.WHITE
                else:
                    color = piece.color.BLACK

                coords = (row, col)

                if p.lower() == 'p':
                    if (color == piece.color.WHITE) and row == 6:
                        has_moved = False
                    if (color == piece.color.BLACK) and row == 1:
                        has_moved = False
                    else:
                        has_moved = True
                elif p.lower() == 'r':
                    has_moved = True
                else:
                    has_moved = False
                final_piece: piece.Piece = piece.piece_dict[p.lower()](color, coords, has_moved)
                self.board[row, col] = final_piece

                if isinstance(final_piece, piece.King):
                    self.kings[color] = final_piece

                self.pieces_dict[color].add(final_piece)

        for char in parsed_fen.castle:
            if char == '-':
                continue
            elif char in piece.default_rook_postion:
                coord = piece.default_rook_postion[char]
                if char.isupper():
                    color = piece.color.WHITE
                else:
                    color = piece.color.BLACK
                p = self.board[coord]
                assert isinstance(p, piece.Rook) and p.color == color
                p.moved = False
            else:
                raise InvalidFEN('Invalid character in castle field')

    def __repr__(self) -> str:
        brd = []
        for ind, row in enumerate(self.board):
            rw = []
            for piece_atsq in row:
                if piece_atsq is not None:
                    piece_repr = piece_atsq.alg_notation
                    if piece_atsq.color == piece.color.WHITE:
                        piece_repr = piece_repr.upper()
                else:
                    piece_repr = _EMPTY_CHAR
                rw.append(piece_repr)
            brd.append([str(ind)] + rw + [' '])
        fullstring = ['  0 1 2 3 4 5 6 7', '\n'.join(('|'.join(row) for row in brd)), ' '+'¯'*17]
        return '\n'.join(fullstring)

    def __str__(self) -> str:
        brd = []
        for row in self.board:
            rw = []
            for piece_atsq in row:
                if piece_atsq is not None:
                    piece_repr = piece_atsq.alg_notation
                    if piece_atsq.color == piece.color.WHITE:
                        piece_repr = piece_repr.upper()
                else:
                    piece_repr = _EMPTY_CHAR
                rw.append(piece_repr)
            brd.append([' '] + rw + [' '])
        fullstring = [' '+'ˍ'*17, '\n'.join(('|'.join(row) for row in brd)), ' '+'¯'*17]
        return '\n'.join(fullstring)


def main():
    FEN = '5k2/p1p2pp1/7p/2n5/8/BP3P2/P1P3PP/1K6 b - - 1 1'
    board = Board(FEN)
    board.check = False
    import webbrowser

    # webbrowser.open(f'https://lichess.org/analysis/{FEN}')
    print(repr(board))
    for i in range(8):
        for j in range(8):
            p = board.board[i, j]
            if p is None:
                continue
            if isinstance(p, piece.Piece):
                print(board)
                print(p)
                print(p.legal_moves(board))


if __name__ == "__main__":
    main()
