from __future__ import annotations

from collections import namedtuple
from typing import List, Optional, Set, Tuple

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

    def __init__(self, rows: int, cols: int) -> None:
        self._arr = [[0 for _ in range(cols)] for _ in range(rows)]

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

    def copy(self) -> List[List[object]]:
        return [row.copy() for row in self._arr]

    @classmethod
    def fromList(cls, array: List[List[object]]):
        rows = len(array)
        columns = len(array[0])
        new_array = cls(rows, columns)
        for i, j in ((x, y) for x in range(rows) for y in range(columns)):
            new_array[i, j] = array[i][j]
        return new_array


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
    board = Arr2D.fromList(board)
    return _FEN(board, *fields[1:])


class Board:
    board: List[List[Optional(piece.Piece)]]
    turn: str
    half_move: int
    fullmove: int
    pawn2move: Optional(Tuple[int, int])
    wht_king: piece.King
    blk_king: piece.King
    wht_rooks: Set[piece.Rook]
    blk_rooks: Set[piece.Rook]
    wht_pieces: Set[piece.Piece]
    blk_pieces: Set[piece.Piece]

    def __init__(self, starting_positing: str = BOARD_START_POS):
        self.board = Arr2D(8, 8)
        self.wht_rooks = set()
        self.blk_rooks = set()
        self.wht_pieces = set()
        self.blk_pieces = set()

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
                    if final_piece.color == piece.color.WHITE:
                        self.wht_king = final_piece
                    else:
                        self.blk_king = final_piece

                elif isinstance(final_piece, piece.Rook):
                    if final_piece.color == piece.color.WHITE:
                        self.wht_rooks.add(final_piece)
                    else:
                        self.blk_rooks.add(final_piece)

                if final_piece.color == piece.color.WHITE:
                    self.wht_pieces.add(final_piece)
                else:
                    self.blk_pieces.add(final_piece)

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
    FEN = "2kr4/ppp2p2/2p4p/8/3b4/5N1b/PP2QPq1/RN3R1K w - - 2 19"
    board = Board(FEN)
    import webbrowser
    # webbrowser.open(f'https://lichess.org/analysis/{FEN}')

    print(board)
    for i in range(8):
        for j in range(8):
            p = board.board[i, j]
            if p is None:
                continue
            print(p)
            if isinstance(p, piece.Piece):
                print(len(p.atacking_region(board)))
                print(p.atacking_region(board))


if __name__ == "__main__":
    main()
