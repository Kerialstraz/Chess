from Piece import *

class Board:
    turn: int
    board: list[list[Piece]]
    white_king: Piece
    black_king: Piece
    white_pieces: list[Piece]
    black_pieces: list[Piece]

    def __init__(self):
        self.board = []
        self.turn = 1


    def initializeBoard(self):
        for row in range(0, 8):
            self.board.append([])
            for column in range(0, 8):
                if row is 1 or 6:
                    self.board[row].append(Pawn("Pawn", [row, column]))
                elif row is 0 or 7:
                    if column is 0:
                        self.board[row].append(Rook("Rook", [row, column]))
                    elif column is 1:
                        self.board[row].append(Knight("Knight", [row, column]))
                    elif column is 2:
                        self.board[row].append(Bishop("Bishop", [row, column]))
                    elif column is 3:
                        if row is 0:
                            self.board[row].append(King("King", [row, column]))
                        elif row is 7:
                            self.board[row].append(Queen("Queen", [row, column]))
                    elif column is 4:
                        if row is 0:
                            self.board[row].append(Queen("Queen", [row, column]))
                        elif row is 7:
                            self.board[row].append(King("King", [row, column]))
                    elif column is 5:
                        self.board[row].append(Bishop("Bishop", [row, column]))
                    elif column is 6:
                        self.board[row].append(Knight("Knight", [row, column]))
                    elif column is 7:
                        self.board[row].append(Rook("Rook", [row, column]))