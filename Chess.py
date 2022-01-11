import random
import time
from tkinter import *
from dataclasses import dataclass, field, is_dataclass
from typing import *
import copy
from tkinter import messagebox
import math

# Used to clump together number-pairs
class Vector2D():
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

# Stores information about the Owner or Player of the piece
class Owner():
    __player: int
    __color: str
    __is_AI: bool

    def __init__(self, player: int, color: str, is_AI: bool):
        self.__player = player
        self.__color = color
        self.__is_AI = is_AI

    def getColor(self):
        return self.__color

    def getPlayer(self):
        return self.__player

# Stores information about the chess piece itself with no regards to the actual player
class Piece():
    __owner: Owner
    __piece_kind: str # Example "Pawn"
    __hasMoved: bool # Is used to determine if a pawn can jump two fields 
    __id: int # Only relevant once when drawing the fields

    def __init__(self, piece_kind: str, owner: Owner):
        self.__piece_kind = piece_kind
        self.__owner = owner
        self.__hasMoved = False
        self.__id = None

    def getKind(self):
        return self.__piece_kind

    def setKind(self, kind: str):
        self.__piece_kind = kind

    def getOwner(self) -> Owner:
        return self.__owner

    def setOwner(self, owner: Owner):
        self.__owner = owner

    def getHasMoved(self) -> bool:
        return self.__hasMoved

    def setHasMoved(self, moved: bool):
        self.__hasMoved = moved
        
    def getId(self) -> int:
        return self.__id
        
    def setId(self, id: int):
        self.__id = id

class Field():
    __name: str # Example A7
    __coordinates: Vector2D # Top-left corner of the square
    __dimension: Vector2D # The x and y span originating from the coordinates
    __piece: Piece # The piece currently on the field, None if there is none
    __row_position: int
    __column_position: int
    __board_id: str # Only relevant once when drawing the fields

    def __init__(self, coordinates: Vector2D, dimension: Vector2D, name: str, row: int, column: int):
        self.__coordinates = coordinates
        self.__dimension = dimension
        self.__name = name
        self.__piece = None
        self.__row_position = row
        self.__column_position = column

    def adjustCoords(self, coor: Vector2D):
        self.__coordinates = coor

    def adjustDimension(self, dimension: Vector2D):
        self.__dimension = dimension

    def getCoords(self):
        return self.__coordinates

    def getDimension(self):
        return self.__dimension

    def getName(self):
        return self.__name

    def setName(self, name: str):
        self.__name = name

    # Calculates the center of the field to determine where to draw the piece
    def getCenter(self):
        x_difference = self.__dimension.x - self.__coordinates.x
        y_difference = self.__dimension.y - self.__coordinates.y
        return Vector2D(self.__coordinates.x + x_difference/2, self.__coordinates.y + y_difference/2)

    def setPiece(self, piece: Piece):
        self.__piece = piece

    def getPiece(self):
        if not(self.__piece == None):
            return self.__piece
        else:
            return Piece("None", Owner(0, "None", False))

    def getPlayer(self):
        if not(self.__piece == None):
            return self.__piece.__owner.__player
        else:
            return Piece("None", Owner(0, "None", False))

    def hasPiece(self):
        if self.__piece == None:
            return False
        else:
            return True

    def getRow(self):
        return self.__row_position

    def setRow(self, row: int):
        self.__row_position = row

    def getColumn(self):
        return self.__column_position

    def setColumn(self, column: int):
        self.__column_position = column

    def getId(self):
        return self.__board_id

    def setId(self, id: int):
        self.__board_id = id

    def info(self):
        print(self.__name + ": piece=" + self.getPiece().getKind())


# Used to store past game states for a move-back-in-time-mechanic
class MoveRecord():
    __starting_move: Field
    __ending_move: Field
    __turn: int
    __field_snapshot: list # A copy of the game-board
    __current_player: int

    def __init__(self, starting_move: Field, ending_move: Field, turn: int, current_field_state: list, player: int):
        self.__starting_move = starting_move
        self.__ending_move = ending_move
        self.__turn = turn
        self.__field_snapshot = current_field_state
        self.__current_player = player

    def getFieldSnapshot(self) -> list:
        return self.__field_snapshot

    def getTurn(self) -> int:
        return self.__turn

    def getCurrentPlayer(self) -> int:
        return self.__current_player

    def info(self):
        print("Starting-Move=" + self.__starting_move.getName() + ";Piece=" + self.__starting_move.getPiece().getKind() + " -> " + "Ending-Move=" + self.__ending_move.getName() + ";Piece=" + self.__ending_move.getPiece().getKind() + " | at turn " + str(self.__turn))

class Move():
    __piece: Piece
    __origin_field: Field
    __field_to_move_to: Field
    __evaluation: int
    __move_depth: int

    def __init__(self, origin_field: Field, piece: Piece, field_to_move_to: Field, evaluation: int, move_depth: int = 0):
        self.__piece = piece
        self.__origin_field = origin_field
        self.__field_to_move_to = field_to_move_to
        self.__evaluation = evaluation
        self.__move_depth = move_depth

    def getMoveField(self):
        return self.__field_to_move_to

    def getOriginField(self):
        return self.__origin_field

    def getMove_depth(self):
        return self.__move_depth

    def getPiece(self):
        return self.__piece


class AI():
    __board: list
    __search_depth: int
    __ai_player: int
    __ai_pieces: list
    __player_pieces: list
    __color: str

    def __init__(self, board: list, depth: int, player: int, color: str):
        self.__board = board
        self.__search_depth = depth
        self.__ai_player = player
        self.__ai_pieces = getAllPlayerField(player)
        self.__color = color
        if player == 1:
            self.__player_pieces = getAllPlayerField(2)
        else:
            self.__player_pieces = getAllPlayerField(1)


    def getColor(self):
        return self.__color





    # def bestMove(self) -> Vector2D:
    #     bHasValidMoves = False
    #     while not bHasValidMoves:
    #         evaluation = 0
    #         piece_array = []
    #         counter = 0
    #
    #         for piece in self.__ai_pieces: # ai_pieces has a collection of each field that contains the pieces that belong to the ai
    #             ai_possible_moves = getValidMoves(piece) # gets all valid moves for a piece as a list containing the possible fields as strings
    #             piece_array.append(Vector2D(piece, []))
    #             if ai_possible_moves:
    #                 for move in ai_possible_moves:
    #                     move_to_check = getFieldByName(move) # since ai_possible_moves is a list of strings, I have to get the Field object by searching for it with its name
    #                     if piece.getPiece().getKind() == "Pawn":
    #                         if PAWN[move_to_check.getRow()][move_to_check.getColumn()] >= evaluation: # PAWN is the pawn_value_table, I check the row/column of the move with the same position in the
    #                                                                                                 # table and look for the move with the highest evaluation
    #                             evaluation = PAWN[move_to_check.getRow()][move_to_check.getColumn()]
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         elif PAWN[move_to_check.getRow()][move_to_check.getColumn()] == evaluation:
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         if move_to_check.getPiece().getOwner().getPlayer() is not piece.getPiece().getOwner().getPlayer(): # Checks if he can take a piece
    #                             if move_to_check.getPiece().getKind() == "Pawn":
    #                                 if PawnValue >= evaluation:
    #                                     piece_array[counter].y = [Vector2D(move_to_check, evaluation)]
    #                             elif move_to_check.getPiece().getKind() == "Knight":
    #                                 if KnightValue >= evaluation:
    #                                     piece_array[counter].y = [Vector2D(move_to_check, evaluation)]
    #                             elif move_to_check.getPiece().getKind() == "Bishop":
    #                                 if BishopValue >= evaluation:
    #                                     piece_array[counter].y = [Vector2D(move_to_check, evaluation)]
    #                             elif move_to_check.getPiece().getKind() == "Rook":
    #                                 if RookValue >= evaluation:
    #                                     piece_array[counter].y = [Vector2D(move_to_check, evaluation)]
    #                             elif move_to_check.getPiece().getKind() == "Queen":
    #                                 if QueenValue >= evaluation:
    #                                     piece_array[counter].y = [Vector2D(move_to_check, evaluation)]
    #                             elif move_to_check.getPiece().getKind() == "King":
    #                                 if KingValue >= evaluation:
    #                                     piece_array[counter].y = [Vector2D(move_to_check, evaluation)]
    #                     if piece.getPiece().getKind() == "Knight":
    #                         if KNIGHT[move_to_check.getRow()][move_to_check.getColumn()] > evaluation:
    #                             evaluation = KNIGHT[move_to_check.getRow()][move_to_check.getColumn()]
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         elif KNIGHT[move_to_check.getRow()][move_to_check.getColumn()] == evaluation:
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         if move_to_check.getPiece().getOwner().getPlayer() is not piece.getPiece().getOwner().getPlayer():
    #                             if move_to_check.getPiece().getKind() == "Pawn":
    #                                 if PawnValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Knight":
    #                                 if KnightValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Bishop":
    #                                 if BishopValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Rook":
    #                                 if RookValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Queen":
    #                                 if QueenValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "King":
    #                                 if KingValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                     if piece.getPiece().getKind() == "Bishop":
    #                         if BISHOP[move_to_check.getRow()][move_to_check.getColumn()] > evaluation:
    #                             evaluation = BISHOP[move_to_check.getRow()][move_to_check.getColumn()]
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         elif BISHOP[move_to_check.getRow()][move_to_check.getColumn()] == evaluation:
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         if move_to_check.getPiece().getOwner().getPlayer() is not piece.getPiece().getOwner().getPlayer():
    #                             if move_to_check.getPiece().getKind() == "Pawn":
    #                                 if PawnValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Knight":
    #                                 if KnightValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Bishop":
    #                                 if BishopValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Rook":
    #                                 if RookValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Queen":
    #                                 if QueenValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "King":
    #                                 if KingValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                     if piece.getPiece().getKind() == "Rook":
    #                         if ROOK[move_to_check.getRow()][move_to_check.getColumn()] > evaluation:
    #                             evaluation = ROOK[move_to_check.getRow()][move_to_check.getColumn()]
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         elif ROOK[move_to_check.getRow()][move_to_check.getColumn()] == evaluation:
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         if move_to_check.getPiece().getOwner().getPlayer() is not piece.getPiece().getOwner().getPlayer():
    #                             if move_to_check.getPiece().getKind() == "Pawn":
    #                                 if PawnValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Knight":
    #                                 if KnightValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Bishop":
    #                                 if BishopValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Rook":
    #                                 if RookValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Queen":
    #                                 if QueenValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "King":
    #                                 if KingValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                     if piece.getPiece().getKind() == "Queen":
    #                         if QUEEN[move_to_check.getRow()][move_to_check.getColumn()] > evaluation:
    #                             evaluation = QUEEN[move_to_check.getRow()][move_to_check.getColumn()]
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         elif QUEEN[move_to_check.getRow()][move_to_check.getColumn()] == evaluation:
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         if move_to_check.getPiece().getOwner().getPlayer() is not piece.getPiece().getOwner().getPlayer():
    #                             if move_to_check.getPiece().getKind() == "Pawn":
    #                                 if PawnValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Knight":
    #                                 if KnightValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Bishop":
    #                                 if BishopValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Rook":
    #                                 if RookValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Queen":
    #                                 if QueenValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "King":
    #                                 if KingValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                     if piece.getPiece().getKind() == "King":
    #                         if KING[move_to_check.getRow()][move_to_check.getColumn()] > evaluation:
    #                             evaluation = KING[move_to_check.getRow()][move_to_check.getColumn()]
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         elif KING[move_to_check.getRow()][move_to_check.getColumn()] == evaluation:
    #                             piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                         if move_to_check.getPiece().getOwner().getPlayer() is not piece.getPiece().getOwner().getPlayer():
    #                             if move_to_check.getPiece().getKind() == "Pawn":
    #                                 if PawnValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Knight":
    #                                 if KnightValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Bishop":
    #                                 if BishopValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Rook":
    #                                 if RookValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "Queen":
    #                                 if QueenValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #                             elif move_to_check.getPiece().getKind() == "King":
    #                                 if KingValue >= evaluation:
    #                                     piece_array[counter].y.append(Vector2D(move_to_check, evaluation))
    #             counter = counter + 1
    #         total_evaluation = 0
    #         for piece_pair in piece_array: # Goes through each Vector2D(piece, Vector2D(move, eva))
    #             for move in piece_pair.y: # Goes through each move, eva pair to search for the highest evaluation out of all the moves
    #                 if move.y >= total_evaluation:
    #                     total_evaluation = move.y
    #         potential_moves = []
    #         for piece_pair in piece_array: # Goes through each Vector2D(piece, Vector2D(move, eva)) again, now with the maximum evaluation found
    #             for move in piece_pair.y:
    #                 if move.y == total_evaluation: # Adds each move with the maximum evaluation found into a list
    #                     potential_moves.append(piece_pair)
    #
    #         chosen_pair = random.choice(potential_moves) # Selects a random Vector2D(piece, Vector2D(move, eva))
    #         complete_move = Vector2D(chosen_pair.x, chosen_pair.y[0].x)
    #         return complete_move




PawnValue = 10
KnightValue = 30
BishopValue = 30
RookValue = 50
QueenValue = 90
KingValue = 100

# AI Piece Table
PAWN = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

KNIGHT = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

BISHOP = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

ROOK = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]

QUEEN = [
    [-20, -10, -10, -5, -5, -10, -10, -20,],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

KING = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]


# Creates the main window
root = Tk()
root.minsize(1000, 800)
root.title("Chess by Tobias Seipenbusch")

# Configures the spacing and priority of spacing for the individual labels and buttons
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=5)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=5)
root.columnconfigure(5, weight=1)
root.columnconfigure(6, weight=1)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=7)


# Globals used throughout the program (should have put them into a GameState class or something)
boardFields = [] # The board itself
board_id = []
hasPieceSelected = False
possible_moves = []
click_history = []
move_history = []
turn = 1
historylist_length = 0
promotion_piece = "None"

isBoard_initialized = False

tracked_pawn_fields_1 = []
tracked_pawn_fields_2 = []

piece_capture_history = []

debug_mode = False

castle = False
player_1_king_check = False
player_2_king_check = False


# Fonts and colors
font_1 = ("Arial", 16)
field_letters = ("Arial", 12, "bold")
listbox_font = ("Arial", 12)
chessboard_color = "#060c0d"
white_color_substitute = "#f5f5ff"
window_color = "#001314"
light_field_color = "#00eeff"
dark_field_color = "#183638"
line_width = 4
bg_color_if_check_true = "#4900d1"
fg_color_if_check_true = "White"
fg_color_if_check_false = "#302840"

player_1_color = "White"
player_2_color = "Black"
current_player = 1

is_player_1_AI = False
is_player_2_AI = True
player_1_AI = None
player_2_AI = None

AI_piece_capture = False

lettering_bib = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
}

numbering_bib = {
    0: 8,
    1: 7,
    2: 6,
    3: 5,
    4: 4,
    5: 3,
    6: 2,
    7: 1,
}


# The widgets
root.configure(background=window_color)
chessboard = Canvas(root, background=chessboard_color, borderwidth=0, highlightthickness=3, highlightbackground=light_field_color)
chessboard_displacement = 60
player_1_field = Label(root, text="Player 1", anchor=W, background="#EBEBEB", font=font_1, height=0)
player_2_field = Label(root, text="Player 2", anchor=W, background="#EBEBEB", font=font_1, height=0)
if is_player_1_AI:
    player_1_thinking_field = Label(root, text="Thinking...", background=window_color, font=font_1, fg=fg_color_if_check_false, height=0)
if is_player_2_AI:
    player_2_thinking_field = Label(root, text="Thinking...", background=window_color, font=font_1, fg=fg_color_if_check_false, height=0)
player_1_check_field = Label(root, text="Check", background=chessboard_color, font=font_1, height=0, foreground=fg_color_if_check_false)
player_2_check_field = Label(root, text="Check", background=chessboard_color, font=font_1, height=0, foreground=fg_color_if_check_false)
move_history_label = Label(root, text="History", anchor=W, background=window_color, foreground=light_field_color,font=font_1, height=0)
move_history_field = Listbox(root, background=window_color, foreground=light_field_color, font=listbox_font, width=30, height=20, exportselection=0, borderwidth=0, highlightthickness=0)
menu_button = Menubutton(root, text="Menü", font=field_letters, background=light_field_color, relief=FLAT , borderwidth=0, activebackground="#2cff29", activeforeground="#ff21f8")
player_color_menu = Menu(menu_button)
color_choice = Checkbutton()
menu_button.config(menu=player_color_menu)
player_color_menu.config()

chessboard.grid(row=2, column=1, columnspan=6, sticky=NSEW)
player_1_field.grid(row=1, column=1, sticky=NSEW)
player_2_field.grid(row=1, column=4, sticky=NSEW)
if is_player_1_AI:
    player_1_thinking_field.grid(row=1, column=3, sticky=NSEW)
if is_player_2_AI:
    player_2_thinking_field.grid(row=1, column=6, sticky=NSEW)
player_1_check_field.grid(row=1, column=2, sticky=NSEW)
player_2_check_field.grid(row=1, column=5, sticky=NSEW)
move_history_label.grid(row=1, column=0, sticky=NSEW)
move_history_field.grid(row=2, column=0, rowspan=2, sticky=NSEW)
menu_button.grid(row=0, column=0, sticky=W)


def getWindowDimension():
    return Vector2D(root.winfo_width(), root.winfo_height())


# Is called when the window changes size to keep everything adjusted
def drawWindow(event=None):
    adjustBoardFields(chessboard_displacement)
    drawChessboard(chessboard_displacement)
    drawPieces()
    root.update()

# draws the lines of the chessboard on the canvas to act as a playing field, displacement is the distance between canvas edge and playing field
def drawChessboard(displacement: int):
    chessboard.delete("all")
    chessboard.create_rectangle(displacement/2, displacement/2, chessboard.winfo_width()-displacement/2, chessboard.winfo_height()-displacement/2, width=line_width, fill="white")
    drawChessboardRectangles()
    for n in range(1, 8):
        chessboard.create_line((chessboard.winfo_width()-displacement)/8*n+displacement/2, displacement/2, (chessboard.winfo_width()-displacement)/8*n+displacement/2, chessboard.winfo_height()-displacement/2, width=line_width)
        chessboard.create_line(displacement/2, (chessboard.winfo_height()-displacement)/8*n+displacement/2, chessboard.winfo_width()-displacement/2, (chessboard.winfo_height()-displacement)/8*n+displacement/2, width=line_width)
        #print(str(chessboard.winfo_width()) + " - " + str(chessboard.winfo_height()))
    for n in range(0, 8):
        chessboard.create_text((chessboard.winfo_width()-displacement)/8*n+(chessboard.winfo_width()-displacement)/16+displacement/2, displacement/4, text=lettering_bib[n], font=field_letters, fill=light_field_color)
        chessboard.create_text(displacement/4, (chessboard.winfo_height()-displacement)/8*n+(chessboard.winfo_height()-displacement)/16+displacement/2, text=numbering_bib[n], font=field_letters, fill=light_field_color)
        chessboard.create_text((chessboard.winfo_width()-displacement)/8*n+(chessboard.winfo_width()-displacement)/16+displacement/2, (chessboard.winfo_height()-displacement)+displacement*(3/4), text=lettering_bib[n], font=field_letters, fill=light_field_color)
        chessboard.create_text((chessboard.winfo_width()-displacement)+displacement*(3/4), (chessboard.winfo_height()-displacement)/8*n+(chessboard.winfo_height()-displacement)/16+displacement/2, text=numbering_bib[n], font=field_letters, fill=light_field_color)
    

# draws the chessboard colored rectangles on the field
def drawChessboardRectangles():
    black_field = True
    field_value = 0
    for row in range(len(boardFields)):
        for field in boardFields[row]:
            if black_field:
                id = chessboard.create_rectangle(field.getCoords().x + line_width/2, field.getCoords().y + line_width/2, field.getDimension().x - line_width/2, field.getDimension().y - line_width/2, width=0, fill=dark_field_color, activefill="#1419a6")
                field.setId(id)
                chessboard.addtag_withtag("Black", id)
                field_value += 1
                if field_value % 8 == 0:
                    field_value = 0
                else:
                    black_field = False
            elif not(black_field):
                id = chessboard.create_rectangle(field.getCoords().x + line_width/2, field.getCoords().y + line_width/2, field.getDimension().x - line_width/2, field.getDimension().y - line_width/2, width=0, fill=light_field_color, activefill="#1419a6")
                field.setId(id)
                chessboard.addtag_withtag("White", id)
                field_value += 1
                if field_value % 8 == 0:
                    field_value = 0
                else:
                    black_field = True

def drawPieces():
    for row in range(0, len(boardFields)):
        for column in range(0, len(boardFields[row])):
            drawPiece(boardFields[row][column], 1)


def drawPiece(field: Field, dimension: float):
    if field.getPiece() == None:
        return
    piece_kind = field.getPiece().getKind()
    piece_color = field.getPiece().getOwner().getColor()
    size = dimension
    r = 30 * size
    line_width = 3
    x = field.getCenter().x
    y = field.getCenter().y

    white_base_fill = "#ff21f8"
    white_secondary_outline_fill = "#631717"
    white_base_outline_fill = "Black"
    white_secondary_fill = "#ff2121"
    white_crown_fill = "#2cff29"

    black_base_fill = "#2cff29"
    black_secondary_outline_fill = "#1c450c"
    black_base_outline_fill = "Black"
    black_secondary_fill = "#ffc800"
    black_crown_fill = "#ff21f8"

    if piece_kind == "Pawn":
        skalar = size * 0.7

        if piece_color == "White":
            # Creates the base of the piece
            chessboard.create_oval(x - r * skalar, y - r * skalar, x + r * skalar, y + r * skalar, width=line_width, outline=white_base_outline_fill, fill=white_base_fill)
        else:
            # Creates the base of the piece
            chessboard.create_oval(x - r * skalar, y - r * skalar, x + r * skalar, y + r * skalar, width=line_width, outline=black_base_outline_fill, fill=black_base_fill)
    elif piece_kind == "Knight":
        if piece_color == "White":
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=white_base_outline_fill, fill=white_base_fill)
            # Creates the oval representing the horse
            chessboard.create_oval(x - r/2, y - r, x + r/2, y + r, width=line_width, outline=white_secondary_outline_fill, fill=white_secondary_fill)
        else:
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=black_base_outline_fill, fill=black_base_fill)
            # Creates the oval representing the horse
            chessboard.create_oval(x - r/2, y - r, x + r/2, y + r, width=line_width, outline=black_secondary_outline_fill, fill=black_secondary_fill)

    elif piece_kind == "Bishop":
        skalar_tip = size * 0.25

        if piece_color == "White":
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=white_base_outline_fill, fill=white_base_fill)
            # Creates the circle representing the tip
            chessboard.create_oval(x - r * skalar_tip, y - r * skalar_tip, x + r * skalar_tip, y + r * skalar_tip, width=line_width, outline=white_secondary_outline_fill, fill=white_secondary_fill)
        else:
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=black_base_outline_fill, fill=black_base_fill)
            # Creates the circle representing the tip
            chessboard.create_oval(x - r * skalar_tip, y - r * skalar_tip, x + r * skalar_tip, y + r * skalar_tip, width=line_width, outline=black_secondary_outline_fill, fill=black_secondary_fill)   

    elif piece_kind == "Rook":
        skalar_top = size * 0.8

        if piece_color == "White":
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=white_base_outline_fill, fill=white_base_fill)
            # Creates the circle representing the tip of the tower
            chessboard.create_oval(x - r * skalar_top, y - r * skalar_top, x + r * skalar_top, y + r * skalar_top, width=line_width, outline=white_secondary_outline_fill, fill=white_secondary_fill)  
        else:
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=black_base_outline_fill, fill=black_base_fill)
            # Creates the circle representing the tip of the tower
            chessboard.create_oval(x - r * skalar_top, y - r * skalar_top, x + r * skalar_top, y + r * skalar_top, width=line_width, outline=black_secondary_outline_fill, fill=black_secondary_fill)  

    elif piece_kind == "Queen":
        skalar_crown_circle = size * 0.8
        skalar_inner_circle = size * 0.25

        if piece_color == "White":
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=white_base_outline_fill, fill=white_base_fill)
            # Creates the circle representing the crown
            chessboard.create_oval(x - r * skalar_crown_circle, y - r * skalar_crown_circle, x + r * skalar_crown_circle, y + r * skalar_crown_circle, width=line_width, outline=white_secondary_outline_fill, fill=white_secondary_fill)  
            # Creates the circle representing the tip of the crown
            chessboard.create_oval(x - r * skalar_inner_circle, y - r * skalar_inner_circle, x + r * skalar_inner_circle, y + r * skalar_inner_circle, width=line_width, outline=white_secondary_outline_fill, fill=white_crown_fill)
        else:
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=black_base_outline_fill, fill=black_base_fill)
            # Creates the circle representing the crown
            chessboard.create_oval(x - r * skalar_crown_circle, y - r * skalar_crown_circle, x + r * skalar_crown_circle, y + r * skalar_crown_circle, width=line_width, outline=black_secondary_outline_fill, fill=black_secondary_fill)  
            # Creates the circle representing the tip of the crown
            chessboard.create_oval(x - r * skalar_inner_circle, y - r * skalar_inner_circle, x + r * skalar_inner_circle, y + r * skalar_inner_circle, width=line_width, outline=black_secondary_outline_fill, fill=black_crown_fill)

    elif piece_kind == "King":
        cross_size = 22 * size
        skalar_crown_circle = size * 0.7
        skalar_inner_circle = size * 0.5

        if piece_color == "White":
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=white_base_outline_fill, fill=white_base_fill)
            # Creates the circle representing the crown
            chessboard.create_oval(x - r * skalar_crown_circle, y - r * skalar_crown_circle, x + r * skalar_crown_circle, y + r * skalar_crown_circle, width=line_width, outline=white_secondary_outline_fill, fill=white_secondary_fill)
            # Creates the circle representing the tip of the crown 
            chessboard.create_oval(x - r * skalar_inner_circle, y - r * skalar_inner_circle, x - r * skalar_inner_circle, y - r * skalar_inner_circle, width=line_width, outline=white_secondary_outline_fill, fill=white_crown_fill)
            # Creates the cross
            chessboard.create_line(x - cross_size, y - cross_size, x + cross_size, y + cross_size, width=line_width, fill=white_crown_fill)
            chessboard.create_line(x - cross_size, y + cross_size, x + cross_size, y - cross_size, width=line_width, fill=white_crown_fill)
        else:
            # Creates the base of the piece
            chessboard.create_oval(x - r, y - r, x + r, y + r, width=line_width, outline=black_base_outline_fill, fill=black_base_fill)
            # Creates the circle representing the crown
            chessboard.create_oval(x - r * skalar_crown_circle, y - r * skalar_crown_circle, x + r * skalar_crown_circle, y + r * skalar_crown_circle, width=line_width, outline=black_secondary_outline_fill, fill=black_secondary_fill)
            # Creates the circle representing the tip of the crown 
            chessboard.create_oval(x - r * skalar_inner_circle, y - r * skalar_inner_circle, x - r * skalar_inner_circle, y - r * skalar_inner_circle, width=line_width, outline=black_secondary_outline_fill, fill=black_crown_fill)
            # Creates the cross
            chessboard.create_line(x - cross_size, y - cross_size, x + cross_size, y + cross_size, width=line_width, fill=black_crown_fill)
            chessboard.create_line(x - cross_size, y + cross_size, x + cross_size, y - cross_size, width=line_width, fill=black_crown_fill)

def determineFirstPlayer():
    global current_player
    if player_1_color == "White":
        current_player = 1
        player_1_field.configure(text="Player 1 | White", background=light_field_color, foreground="Black")
        player_2_field.configure(text="Player 2 | Black", background=dark_field_color, foreground=white_color_substitute)
    elif player_2_color == "White":
        current_player = 2
        player_2_field.configure(text="Player 2 | White", background=light_field_color, foreground="Black")
        player_1_field.configure(text="Player 1 | Black", background=dark_field_color, foreground=white_color_substitute)

# Initializes the playing field with invisible squares stored in boardFields[] which are above the playing field, meant for detecting clicks and initializing pieces
def initializeBoard():
    determineFirstPlayer()
    for row in range(0, 8): 
        boardFields.append([])
        for column in range(0, 8):
            square_name = getPlayingFieldName(row, column)
            boardFields[row].append(Field(Vector2D(0, 0), Vector2D(0, 0), square_name, row, column))
    initializePieces()
    if isAI(1):
        global player_1_AI
        player_1_AI = AI(boardFields, 2, 1, player_1_color)
        print("Player 1 AI has been created")
    if isAI(2):
        global player_2_AI
        player_2_AI = AI(boardFields, 2, 2, player_2_color)
        print("Player 2 AI has been created")
         
def adjustBoardFields(displacement: int):
    adjustBoardFieldsPosition(displacement)
    adjustBoardFieldsDimension(chessboard.winfo_width()-displacement, chessboard.winfo_height()-displacement)


# Adjusts the Coordinates of the playfield squares
def adjustBoardFieldsPosition(displacement: int):
    for row in range(0, len(boardFields)):
        y_coord = (chessboard.winfo_height()-displacement)/8*(7-row)+displacement/2
        for column in range(0, len(boardFields[row])):
            x_coord = (chessboard.winfo_width()-displacement)/8*(column)+displacement/2
            boardFields[row][column].adjustCoords(Vector2D(x_coord, y_coord))

# Adjusts the length/Dimension of the playfield squares
def adjustBoardFieldsDimension(playfield_x_width: int, playfield_y_height: int):
    field_x_width = playfield_x_width / 8
    field_y_width = playfield_y_height / 8
    for row in range(0, len(boardFields)):
        for column in range(0, len(boardFields[row])):
            boardFields[row][column].adjustDimension(Vector2D(field_x_width + boardFields[row][column].getCoords().x, field_y_width + boardFields[row][column].getCoords().y))
            #boardFields[row][column].info()

# Creates the initial position of all the pieces
def initializePieces():
    initializePawns()
    initializeKnights()
    initializeBishops()
    initializeRooks()
    initializeQueens()
    initializeKings()
    return

def initializePawns():
    # Player 1 Pawns
    if is_player_1_AI:
        getFieldByName("A2").setPiece(Piece("Pawn", Owner(1, player_1_color, True)))
        getFieldByName("B2").setPiece(Piece("Pawn", Owner(1, player_1_color, True)))
        getFieldByName("C2").setPiece(Piece("Pawn", Owner(1, player_1_color, True)))
        getFieldByName("D2").setPiece(Piece("Pawn", Owner(1, player_1_color, True)))
        getFieldByName("E2").setPiece(Piece("Pawn", Owner(1, player_1_color, True)))
        getFieldByName("F2").setPiece(Piece("Pawn", Owner(1, player_1_color, True)))
        getFieldByName("G2").setPiece(Piece("Pawn", Owner(1, player_1_color, True)))
        getFieldByName("H2").setPiece(Piece("Pawn", Owner(1, player_1_color, True)))
    else:
        getFieldByName("A2").setPiece(Piece("Pawn", Owner(1, player_1_color, False)))
        getFieldByName("B2").setPiece(Piece("Pawn", Owner(1, player_1_color, False)))
        getFieldByName("C2").setPiece(Piece("Pawn", Owner(1, player_1_color, False)))
        getFieldByName("D2").setPiece(Piece("Pawn", Owner(1, player_1_color, False)))
        getFieldByName("E2").setPiece(Piece("Pawn", Owner(1, player_1_color, False)))
        getFieldByName("F2").setPiece(Piece("Pawn", Owner(1, player_1_color, False)))
        getFieldByName("G2").setPiece(Piece("Pawn", Owner(1, player_1_color, False)))
        getFieldByName("H2").setPiece(Piece("Pawn", Owner(1, player_1_color, False)))
    # Player 2 Pawns
    if is_player_2_AI:
        getFieldByName("A7").setPiece(Piece("Pawn", Owner(2, player_2_color, True)))
        getFieldByName("B7").setPiece(Piece("Pawn", Owner(2, player_2_color, True)))
        getFieldByName("C7").setPiece(Piece("Pawn", Owner(2, player_2_color, True)))
        getFieldByName("D7").setPiece(Piece("Pawn", Owner(2, player_2_color, True)))
        getFieldByName("E7").setPiece(Piece("Pawn", Owner(2, player_2_color, True)))
        getFieldByName("F7").setPiece(Piece("Pawn", Owner(2, player_2_color, True)))
        getFieldByName("G7").setPiece(Piece("Pawn", Owner(2, player_2_color, True)))
        getFieldByName("H7").setPiece(Piece("Pawn", Owner(2, player_2_color, True)))
    else:
        getFieldByName("A7").setPiece(Piece("Pawn", Owner(2, player_2_color, False)))
        getFieldByName("B7").setPiece(Piece("Pawn", Owner(2, player_2_color, False)))
        getFieldByName("C7").setPiece(Piece("Pawn", Owner(2, player_2_color, False)))
        getFieldByName("D7").setPiece(Piece("Pawn", Owner(2, player_2_color, False)))
        getFieldByName("E7").setPiece(Piece("Pawn", Owner(2, player_2_color, False)))
        getFieldByName("F7").setPiece(Piece("Pawn", Owner(2, player_2_color, False)))
        getFieldByName("G7").setPiece(Piece("Pawn", Owner(2, player_2_color, False)))
        getFieldByName("H7").setPiece(Piece("Pawn", Owner(2, player_2_color, False)))

def initializeRooks():
    # Player 1 Rooks
    if is_player_1_AI:
        getFieldByName("A1").setPiece(Piece("Rook", Owner(1, player_1_color, True)))
        getFieldByName("H1").setPiece(Piece("Rook", Owner(1, player_1_color, True)))
    else:
        getFieldByName("A1").setPiece(Piece("Rook", Owner(1, player_1_color, False)))
        getFieldByName("H1").setPiece(Piece("Rook", Owner(1, player_1_color, False)))
    # Player 2 Rooks
    if is_player_2_AI:
        getFieldByName("A8").setPiece(Piece("Rook", Owner(2, player_2_color, True)))
        getFieldByName("H8").setPiece(Piece("Rook", Owner(2, player_2_color, True)))
    else:
        getFieldByName("A8").setPiece(Piece("Rook", Owner(2, player_2_color, False)))
        getFieldByName("H8").setPiece(Piece("Rook", Owner(2, player_2_color, False)))

def initializeKnights():
    # Player 1 Knights
    if is_player_1_AI:
        getFieldByName("B1").setPiece(Piece("Knight", Owner(1, player_1_color, True)))
        getFieldByName("G1").setPiece(Piece("Knight", Owner(1, player_1_color, True)))
    else:
        getFieldByName("B1").setPiece(Piece("Knight", Owner(1, player_1_color, False)))
        getFieldByName("G1").setPiece(Piece("Knight", Owner(1, player_1_color, False)))
    # Player 2 Knights
    if is_player_2_AI:
        getFieldByName("B8").setPiece(Piece("Knight", Owner(2, player_2_color, True)))
        getFieldByName("G8").setPiece(Piece("Knight", Owner(2, player_2_color, True)))
    else:
        getFieldByName("B8").setPiece(Piece("Knight", Owner(2, player_2_color, False)))
        getFieldByName("G8").setPiece(Piece("Knight", Owner(2, player_2_color, False)))

def initializeBishops():
    # Player 1 Bishops
    if is_player_1_AI:
        getFieldByName("C1").setPiece(Piece("Bishop", Owner(1, player_1_color, True)))
        getFieldByName("F1").setPiece(Piece("Bishop", Owner(1, player_1_color, True)))
    else:
        getFieldByName("C1").setPiece(Piece("Bishop", Owner(1, player_1_color, False)))
        getFieldByName("F1").setPiece(Piece("Bishop", Owner(1, player_1_color, False)))
    # Player 2 Bishops
    if is_player_2_AI:
        getFieldByName("C8").setPiece(Piece("Bishop", Owner(2, player_2_color, True)))
        getFieldByName("F8").setPiece(Piece("Bishop", Owner(2, player_2_color, True)))
    else:
        getFieldByName("C8").setPiece(Piece("Bishop", Owner(2, player_2_color, False)))
        getFieldByName("F8").setPiece(Piece("Bishop", Owner(2, player_2_color, False)))

def initializeQueens():
    # Player 1 Queen
    if is_player_1_AI:
        getFieldByName("D1").setPiece(Piece("Queen", Owner(1, player_1_color, True)))
    else:
        getFieldByName("D1").setPiece(Piece("Queen", Owner(1, player_1_color, False)))
    # Player 2 Queen
    if is_player_2_AI:
        getFieldByName("E8").setPiece(Piece("Queen", Owner(2, player_2_color, True)))
    else:
        getFieldByName("E8").setPiece(Piece("Queen", Owner(2, player_2_color, False)))

def initializeKings():
    # Player 1 King
    if is_player_1_AI:
        getFieldByName("E1").setPiece(Piece("King", Owner(1, player_1_color, True)))
    else:
        getFieldByName("E1").setPiece(Piece("King", Owner(1, player_1_color, False)))
    # Player 2 King+
    if is_player_2_AI:
        getFieldByName("D8").setPiece(Piece("King", Owner(2, player_2_color, True)))
    else:
        getFieldByName("D8").setPiece(Piece("King", Owner(2, player_2_color, False)))

# Return the combination of letter+number in order to assisn a chesslike notation to each Field() in boardFields[] inizialized by initializeBoardFields()
def getPlayingFieldName(row: int, column: int):
    letter = getPlayingFieldLetter(column)
    number = getPlayingFieldNumber(row)
    return letter+number

# Assigns each column a corresponding letter
def getPlayingFieldLetter(column: int):
    if column == 0:
        return 'A'
    elif column == 1:
        return 'B'
    elif column == 2:
        return 'C'
    elif column == 3:
        return 'D'
    elif column == 4:
        return 'E'
    elif column == 5:
        return 'F'
    elif column == 6:
        return 'G'
    elif column == 7:
        return 'H'

# Assigns each row a corresponding number
def getPlayingFieldNumber(row: int):
    if row == 0:
        return '1'
    elif row == 1:
        return '2'
    elif row == 2:
        return '3'
    elif row == 3:
        return '4'
    elif row == 4:
        return '5'
    elif row == 5:
        return '6'
    elif row == 6:
        return '7'
    elif row == 7:
        return '8'

# Enables you to find a square by a given namen, example G6
def getFieldByName(name: str) -> Field:
    for row in range(len(boardFields)):
        for column in range(len(boardFields[row])):
            if boardFields[row][column].getName() == name:
                return boardFields[row][column]

def getAllPlayerField(player: int) -> list:
    all_fields = []
    for row in range(0, len(boardFields)):
        for column in range(0, len(boardFields[row])):
            if boardFields[row][column].getPiece().getOwner().getPlayer() == player:
                all_fields.append(boardFields[row][column])
    return all_fields

def getFieldsByColor(color: str) -> list:
    fields = []
    for row in range(0, len(boardFields)):
        for column in range(0, len(boardFields[row])):
            if boardFields[row][column].getPiece().getOwner().getColor() == color:
                fields.append(boardFields[row][column])
    return fields


# Determines the playfield square that got clicked on
def getFieldClicked(click_coords) -> Field:
    for row in range(0, len(boardFields)):
        for column in range(0, len(boardFields[row])):
            if isInbetween(click_coords.x, boardFields[row][column].getCoords().x, boardFields[row][column].getDimension().x):
                if isInbetween(click_coords.y, boardFields[row][column].getCoords().y, boardFields[row][column].getDimension().y):
                    print("--------------------------------------------------------------------------")
                    print("Clicked in: " + boardFields[row][column].getName() + " | Piece: " + boardFields[row][column].getPiece().getKind())
                    return boardFields[row][column]

# Checks if n is between x and y
def isInbetween(n: float, x: float, y: float):
    if x > y:
        if n < x and n > y:
            return True
        else:
            return False
    elif x < y:
        if n > x and n < y:
            return True
        else:
            return False

def move(event):
    if isAI(current_player):
        time.sleep(0.25)
        global boardFields
        if current_player == 1:
            ai_move = minimax(-math.inf, math.inf, True, player_1_AI.getColor(), 2)
            movePiece(ai_move[0].getOriginField(), ai_move[0].getMoveField().getName())
            nextPlayer()
        elif current_player == 2:
            ai_move = minimax(-math.inf, math.inf, True, player_2_AI.getColor(), 2)
            movePiece(ai_move[0].getOriginField(), ai_move[0].getMoveField().getName())
            nextPlayer()
        return
    else:
        field_clicked = getFieldClicked(event)
        global hasPieceSelected
        global possible_moves
        isOutside_of_possible_moves = False

        # Checkt ob ein Feld geklickt wurde
        if not (field_clicked == None):
            # Checks if the field the user clicked in has a piece and if the user has already selected a piece
            if field_clicked.hasPiece() and hasPieceSelected == False and current_player == field_clicked.getPiece().getOwner().getPlayer():
                if hasValidMoves(field_clicked):
                    click_history.append(field_clicked)
                    possible_moves = getValidMoves(field_clicked)
                    if possible_moves:
                        print("Possible Moves: " + str(possible_moves))
                        highlightMoves(possible_moves, True)
                        hasPieceSelected = True
                        return

            if possible_moves:
                for possible_field in range(0, len(possible_moves)):
                    if field_clicked.getName() == possible_moves[possible_field]:
                        click_history.append(field_clicked)
                        movePiece(click_history[len(click_history) - 2], possible_moves[possible_field])
                        possible_moves.clear()
                        hasPieceSelected = False
                        nextPlayer()
                    else:
                        isOutside_of_possible_moves = True

            if hasPieceSelected == True and isOutside_of_possible_moves == True:
                # Goes through all possible moves and checks if the current click is one of the possible moves, if not, deselect
                for name in possible_moves:
                    if not (field_clicked.getName() == name):
                        highlightMoves(possible_moves, False)
                        hasPieceSelected = False
                        possible_moves = []

def isAI(player: int):
    if player == 1 and is_player_1_AI:
        return True
    elif player == 2 and is_player_2_AI:
        return True
    else:
        return False

def hasValidMoves(origin_field: Field) -> bool:
    piece = origin_field.getPiece()
    if piece.getKind() == "Pawn":
        if hasValidPawnMoves(origin_field):
            return True
        else:
            return False
    if piece.getKind() == "Rook":
        return True
    if piece.getKind() == "Knight":
        return True
    if piece.getKind() == "Bishop":
        return True
    if piece.getKind() == "Queen":
        return True
    if piece.getKind() == "King":
        return True



def hasValidPawnMoves(origin_field: Field) -> bool:
    player = origin_field.getPiece().getOwner().getPlayer()
    piece_row = origin_field.getRow()
    if player == 1:
        # Checks if the pawn is at the last row of the field, at which a pawn has no moves
        if piece_row == 7:
            return False
        return True
    if player == 2:
        # Checks if the pawn is at the first row of the field, at which a pawn has no moves
        if piece_row == 0:
            return False
        return True



def minimax(alpha: int, beta: int, maximizing_player: bool, maximizing_color: str, depth: int):
    if depth == 0:
        return None, evaluate(maximizing_color)

    global tracked_pawn_fields_1
    global tracked_pawn_fields_2
    global AI_piece_capture
    global boardFields
    global piece_capture_history

    if maximizing_player:
        moves = getAllMovesByColor(maximizing_color)
        best_move = random.choice(moves)
    else:
        if maximizing_color == "Black":
            moves = getAllMovesByColor("White")
            best_move = random.choice(moves)
        else:
            moves = getAllMovesByColor("Black")
            best_move = random.choice(moves)


    if maximizing_player:
        max_eval = -math.inf
        for viable_move in moves:
            board_copy = copy.deepcopy(boardFields)
            movePiece(viable_move.getOriginField(), viable_move.getMoveField().getName(), depth, True)
            #tracked_pawn_fields_1 = []
            #tracked_pawn_fields_2 = []
            current_evaluation = minimax(alpha, beta, False, maximizing_color, depth-1)[1]
            #alpha = max(alpha, max_eval)
            #movePiece(viable_move.getMoveField(), viable_move.getOriginField().getName(), depth, True)
            boardFields = board_copy
            if current_evaluation > max_eval:
                max_eval = current_evaluation
                best_move = viable_move
            #if beta <= alpha:
                #break
        return best_move, int(max_eval)
    else:
        min_eval = math.inf
        for viable_move in moves:
            board_copy = copy.deepcopy(boardFields)
            movePiece(viable_move.getOriginField(), viable_move.getMoveField().getName(), depth, True)
            #tracked_pawn_fields_1 = []
            #tracked_pawn_fields_2 = []
            current_evaluation = minimax(alpha, beta, True, maximizing_color, depth-1)[1]
            #beta = min(beta, min_eval)
            #movePiece(viable_move.getMoveField(), viable_move.getOriginField().getName(), depth, True)
            boardFields = board_copy
            if current_evaluation < min_eval:
                min_eval = current_evaluation
                best_move = viable_move
            #if beta <= alpha:
                #break
        return best_move, int(min_eval)



def getValidMoves(origin_field: Field) -> list:
    if debug_mode == True:
        valid_moves = []
        for row in boardFields:
            for column in row:
                valid_moves.append(column.getName())
        valid_moves.remove(origin_field.getName())
        return valid_moves

    if origin_field.getPiece().getOwner().getPlayer() == 1 and player_1_king_check == True:
        if origin_field.getPiece().getKind() == "King":
            return getValidKingMoves(origin_field)
        else:
            return []
    elif origin_field.getPiece().getOwner().getPlayer() == 2 and player_2_king_check == True:
        if origin_field.getPiece().getKind() == "King":
            return getValidKingMoves(origin_field)
        else:
            return []

    piece_kind = origin_field.getPiece().getKind()
    if piece_kind == "Pawn":
        return getValidPawnMoves(origin_field)
    if piece_kind == "Rook":
        return getValidRookMoves(origin_field)
    if piece_kind == "Knight":
        return getValidKnightMoves(origin_field)
    if piece_kind == "Bishop":
        return getValidBishopMoves(origin_field)
    if piece_kind == "Queen":
        return getValidQueenMoves(origin_field)
    if piece_kind == "King":
        return getValidKingMoves(origin_field)



def checkIfKingCheck(field_of_king_to_check: Field) -> bool:
    if field_of_king_to_check.getPiece().getOwner().getPlayer() == 1:
        player = 2
    else:
        player = 1
    enemy_fields = getAllPlayerField(player)
    enemy_moves = []
    for field in enemy_fields:
        moves = getValidMoves(field)
        if field.getPiece().getKind() == "Pawn":
            moves = moves + getTheoreticallyPossiblePawnMoves(field)
            if current_player == 2:
                if containsFieldName(moves, boardFields[field.getRow()-1][field.getColumn()].getName()):
                    moves.remove(boardFields[field.getRow()-1][field.getColumn()].getName())
                    if boardFields[field.getRow()][field.getColumn()].getPiece().getHasMoved() == False:
                        if containsFieldName(moves, boardFields[field.getRow()-2][field.getColumn()].getName()):
                            moves.remove(boardFields[field.getRow()-2][field.getColumn()].getName())
            elif current_player == 1:
                if containsFieldName(moves, boardFields[field.getRow()+1][field.getColumn()].getName()):
                    moves.remove(boardFields[field.getRow()+1][field.getColumn()].getName())
                    if boardFields[field.getRow()][field.getColumn()].getPiece().getHasMoved() == False:
                        if containsFieldName(moves, boardFields[field.getRow()+2][field.getColumn()].getName()):
                            moves.remove(boardFields[field.getRow()+2][field.getColumn()].getName())
        for name in moves:
            enemy_moves.append(name)
    if containsFieldName(enemy_moves, field_of_king_to_check.getName()):
            return True
    else:
            return False


def is_surrounded_by_allies(field_to_check: Field) -> bool:
    if field_to_check.getRow() - 1 >= 0:
        if boardFields[field_to_check.getRow() - 1][field_to_check.getColumn()].hasPiece() and not(boardFields[field_to_check.getRow() - 1][field_to_check.getColumn()].getPiece().getOwner().getPlayer() == field_to_check.getPiece().getOwner().getPlayer()):
            return False
        if field_to_check.getColumn() - 1 >= 0:
            if boardFields[field_to_check.getRow() - 1][field_to_check.getColumn() - 1].hasPiece() and not(boardFields[field_to_check.getRow() - 1][field_to_check.getColumn() - 1].getPiece().getOwner().getPlayer() == field_to_check.getPiece().getOwner().getPlayer()):
                return False
        if field_to_check.getColumn() + 1 <= 7:
            if boardFields[field_to_check.getRow() - 1][field_to_check.getColumn() + 1].hasPiece() and not(boardFields[field_to_check.getRow() - 1][field_to_check.getColumn() + 1].getPiece().getOwner().getPlayer() == field_to_check.getPiece().getOwner().getPlayer()):
                return False

    if field_to_check.getRow() + 1 <= 7:
        if boardFields[field_to_check.getRow() + 1][field_to_check.getColumn()].hasPiece() and not(boardFields[field_to_check.getRow() + 1][field_to_check.getColumn()].getPiece().getOwner().getPlayer() == field_to_check.getPiece().getOwner().getPlayer()):
            return False
        if field_to_check.getColumn() - 1 >= 0:
            if boardFields[field_to_check.getRow() + 1][field_to_check.getColumn() - 1].hasPiece() and not(boardFields[field_to_check.getRow() + 1][field_to_check.getColumn() - 1].getPiece().getOwner().getPlayer() == field_to_check.getPiece().getOwner().getPlayer()):
                return False
        if field_to_check.getColumn() + 1 <= 7:
            if boardFields[field_to_check.getRow() + 1][field_to_check.getColumn() + 1].hasPiece() and not(boardFields[field_to_check.getRow() + 1][field_to_check.getColumn() + 1].getPiece().getOwner().getPlayer() == field_to_check.getPiece().getOwner().getPlayer()):
                return False

    if field_to_check.getColumn() - 1 >= 0:
        if boardFields[field_to_check.getRow()][field_to_check.getColumn() - 1].hasPiece() and not(boardFields[field_to_check.getRow()][field_to_check.getColumn() - 1].getPiece().getOwner().getPlayer() == field_to_check.getPiece().getOwner().getPlayer()):
            return False
    if field_to_check.getColumn() + 1 <= 7:
        if boardFields[field_to_check.getRow()][field_to_check.getColumn() + 1].hasPiece() and not(boardFields[field_to_check.getRow()][field_to_check.getColumn() + 1].getPiece().getOwner().getPlayer() == field_to_check.getPiece().getOwner().getPlayer()):
            return False
    return True


def evaluate(maximizing_color: str) -> int:
    print("Evaluation the board. Maximizing color: " + maximizing_color)
    if maximizing_color == "White":
        calculated_score = calculateBoardScore("White") - calculateBoardScore("Black")
        print("The calculated board score for " + maximizing_color + " is " + str(calculated_score))
        return calculated_score
    else:
        calculated_score = calculateBoardScore("Black") - calculateBoardScore("White")
        print("The calculated board score for " + maximizing_color + " is " + str(calculated_score))
        return calculated_score


def calculateBoardScore(color: str) -> int:
    print("Calculating board score for " + color + "...")
    fields_to_sum = getFieldsByColor(color)
    total_sum = 0
    for field in fields_to_sum:
        if field.getPiece().getKind() == "Pawn":
            total_sum = total_sum + PawnValue
        elif field.getPiece().getKind() == "Knight":
            total_sum = total_sum + KnightValue
        elif field.getPiece().getKind() == "Rook":
            total_sum = total_sum + RookValue
        elif field.getPiece().getKind() == "Bishop":
            total_sum = total_sum + BishopValue
        elif field.getPiece().getKind() == "Queen":
            total_sum = total_sum + QueenValue
        elif field.getPiece().getKind() == "King":
            total_sum = total_sum + KingValue
    print("Calculated board score for " + color + " is " + str(total_sum))
    return total_sum

def getAllMovesOnBoard():
    moves = []
    for row in range(0, len(boardFields)):
        for column in range(0, len(boardFields[row])):
            if boardFields[row][column].hasPiece():
                piece_moves = getValidMoves(boardFields[row][column])
                if piece_moves:
                    for move in piece_moves:
                        moves.append(transformValidMovesIntoMoveClass(boardFields[row][column], getFieldByName(move), None))
    return moves

def getAllMovesByColor(color: str):
    moves = []
    for row in range(0, len(boardFields)):
        for column in range(0, len(boardFields[row])):
            if boardFields[row][column].hasPiece() and boardFields[row][column].getPiece().getOwner().getColor() == color:
                piece_moves = getValidMoves(boardFields[row][column])
                if piece_moves:
                    for move in piece_moves:
                        moves.append(transformValidMovesIntoMoveClass(boardFields[row][column], getFieldByName(move), None))
    return moves

def transformValidMovesIntoMoveClass(origin_field: Field, field_to_move_to: Field, depth):
    return Move(origin_field, origin_field.getPiece(), field_to_move_to, 0, depth)


def findPiecesByKind(kind: str) -> list:
    kinds = []
    for row in range(0, len(boardFields)):
        for column in range(0, len(boardFields[row])):
            if boardFields[row][column].getPiece().getKind() == kind:
                kinds.append(boardFields[row][column].getName())
    return kinds


def getValidPawnMoves(origin_field: Field) -> list:
    player = origin_field.getPiece().getOwner().getPlayer()
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = []
    if player == 1:
        if not(boardFields[piece_row+1][piece_column].hasPiece()):
            valid_moves.append(boardFields[piece_row+1][piece_column].getName())
            if piece_row == 1:
                if not(boardFields[piece_row+2][piece_column].hasPiece()):
                    valid_moves.append(boardFields[piece_row+2][piece_column].getName())

        if piece_column == 0:
            if boardFields[piece_row+1][piece_column+1].hasPiece() or containsFieldName(tracked_pawn_fields_2, boardFields[piece_row+1][piece_column+1].getName()):
                if not(boardFields[piece_row+1][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                    valid_moves.append(boardFields[piece_row+1][piece_column+1].getName())
        elif piece_column == 7:
            if boardFields[piece_row+1][piece_column-1].hasPiece() or containsFieldName(tracked_pawn_fields_2, boardFields[piece_row+1][piece_column-1].getName()):
                if not(boardFields[piece_row+1][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                    valid_moves.append(boardFields[piece_row+1][piece_column-1].getName())
        else:
            if boardFields[piece_row+1][piece_column-1].hasPiece() or containsFieldName(tracked_pawn_fields_2, boardFields[piece_row+1][piece_column-1].getName()):
                if not(boardFields[piece_row+1][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                    valid_moves.append(boardFields[piece_row+1][piece_column-1].getName())
            if boardFields[piece_row+1][piece_column+1].hasPiece() or containsFieldName(tracked_pawn_fields_2, boardFields[piece_row+1][piece_column+1].getName()):
                if not(boardFields[piece_row+1][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                    valid_moves.append(boardFields[piece_row+1][piece_column+1].getName())
    elif player == 2:
        if not(boardFields[piece_row-1][piece_column].hasPiece()):
            valid_moves.append(boardFields[piece_row-1][piece_column].getName())
            if piece_row == 6:
                if not(boardFields[piece_row-2][piece_column].hasPiece()):
                    valid_moves.append(boardFields[piece_row-2][piece_column].getName())

        if piece_column == 0:
            if boardFields[piece_row-1][piece_column+1].hasPiece() or containsFieldName(tracked_pawn_fields_1, boardFields[piece_row-1][piece_column+1].getName()):
                if not(boardFields[piece_row-1][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                    valid_moves.append(boardFields[piece_row-1][piece_column+1].getName())
        elif piece_column == 7:
            if boardFields[piece_row-1][piece_column-1].hasPiece() or containsFieldName(tracked_pawn_fields_1, boardFields[piece_row-1][piece_column-1].getName()):
                if not(boardFields[piece_row-1][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                    valid_moves.append(boardFields[piece_row-1][piece_column-1].getName())
        else:
            if boardFields[piece_row-1][piece_column-1].hasPiece() or containsFieldName(tracked_pawn_fields_1, boardFields[piece_row-1][piece_column-1].getName()):
                if not(boardFields[piece_row-1][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                    valid_moves.append(boardFields[piece_row-1][piece_column-1].getName())
            if boardFields[piece_row-1][piece_column+1].hasPiece() or containsFieldName(tracked_pawn_fields_1, boardFields[piece_row-1][piece_column+1].getName()):
                if not(boardFields[piece_row-1][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                    valid_moves.append(boardFields[piece_row-1][piece_column+1].getName())


    return valid_moves


def getTheoreticallyPossiblePawnMoves(origin_field: Field) -> list:
    player = origin_field.getPiece().getOwner().getPlayer()
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    possible_moves = []
    if player == 1:
        if not(piece_column == 0):
            possible_moves.append(boardFields[piece_row+1][piece_column-1].getName())
        if not(piece_column == 7):
            possible_moves.append(boardFields[piece_row+1][piece_column+1].getName())
    elif player == 2:
        if not(piece_column == 0):
            possible_moves.append(boardFields[piece_row-1][piece_column-1].getName())
        if not(piece_column == 7):
            possible_moves.append(boardFields[piece_row-1][piece_column+1].getName())
    return possible_moves


def getValidRookMoves(origin_field: Field) -> list:
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = []
    for row_in_positiv_x in range(piece_row+1, len(boardFields)):
        if boardFields[row_in_positiv_x][piece_column].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
            break
        else:
            valid_moves.append(boardFields[row_in_positiv_x][piece_column].getName())
            if boardFields[row_in_positiv_x][piece_column].hasPiece():
                break
    for row_in_negative_x in range(piece_row-1, -1, -1):
        if boardFields[row_in_negative_x][piece_column].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
            break
        else:
            valid_moves.append(boardFields[row_in_negative_x][piece_column].getName())
            if boardFields[row_in_negative_x][piece_column].hasPiece():
                break
    for column_in_positiv_x in range(piece_column+1, len(boardFields[piece_row])):
        if boardFields[piece_row][column_in_positiv_x].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
            break
        else:
             valid_moves.append(boardFields[piece_row][column_in_positiv_x].getName())
             if boardFields[piece_row][column_in_positiv_x].hasPiece():
                break
    for column_in_negative_x in range(piece_column-1, -1, -1):
        if boardFields[piece_row][column_in_negative_x].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
            break
        else:
            valid_moves.append(boardFields[piece_row][column_in_negative_x].getName())
            if boardFields[piece_row][column_in_negative_x].hasPiece():
                break
    return valid_moves

def getValidKnightMoves(origin_field: Field) -> list:
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = []
    if not(piece_row + 2 > 7):
        if not(piece_column + 1 > 7):
            if not(boardFields[piece_row+2][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                valid_moves.append(boardFields[piece_row+2][piece_column+1].getName())
    if not(piece_row + 2 > 7):
        if not(piece_column - 1 < 0):
            if not(boardFields[piece_row+2][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                valid_moves.append(boardFields[piece_row+2][piece_column-1].getName())
    if not(piece_row + 1 > 7):
        if not(piece_column + 2 > 7):
            if not(boardFields[piece_row+1][piece_column+2].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                valid_moves.append(boardFields[piece_row+1][piece_column+2].getName())
    if not(piece_row + 1 > 7):
        if not(piece_column - 2 < 0):
            if not(boardFields[piece_row+1][piece_column-2].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                valid_moves.append(boardFields[piece_row+1][piece_column-2].getName())
    if not(piece_row - 2 < 0):
        if not(piece_column + 1 > 7):
            if not(boardFields[piece_row-2][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                valid_moves.append(boardFields[piece_row-2][piece_column+1].getName())
    if not(piece_row - 2 < 0):
        if not(piece_column - 1 < 0):
            if not(boardFields[piece_row-2][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                valid_moves.append(boardFields[piece_row-2][piece_column-1].getName())
    if not(piece_row - 1 < 0):
        if not(piece_column + 2 > 7):
            if not(boardFields[piece_row-1][piece_column+2].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                valid_moves.append(boardFields[piece_row-1][piece_column+2].getName())
    if not(piece_row - 1 < 0):
        if not(piece_column - 2 < 0):
            if not(boardFields[piece_row-1][piece_column-2].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                valid_moves.append(boardFields[piece_row-1][piece_column-2].getName())
    return valid_moves

def getValidBishopMoves(origin_field: Field) -> list:
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = []

    for n in range(1, 8):
        if (piece_row + n > 7) or (piece_column + n > 7):
            break
        else:
            if boardFields[piece_row+n][piece_column+n].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
                break
            else:
                if boardFields[piece_row+n][piece_column+n].hasPiece():
                    valid_moves.append(boardFields[piece_row+n][piece_column+n].getName())
                    break
                valid_moves.append(boardFields[piece_row+n][piece_column+n].getName())
    for n in range(1, 8):
        if (piece_row + n > 7) or (piece_column - n < 0):
            break
        else:
            if boardFields[piece_row+n][piece_column-n].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
                break
            else:
                if boardFields[piece_row+n][piece_column-n].hasPiece():
                    valid_moves.append(boardFields[piece_row+n][piece_column-n].getName())
                    break
                valid_moves.append(boardFields[piece_row+n][piece_column-n].getName())
    for n in range(1, 8):
        if (piece_row - n < 0) or (piece_column + n > 7):
            break
        else:
            if boardFields[piece_row-n][piece_column+n].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
                break
            else:
                if boardFields[piece_row-n][piece_column+n].hasPiece():
                    valid_moves.append(boardFields[piece_row-n][piece_column+n].getName())
                    break
                valid_moves.append(boardFields[piece_row-n][piece_column+n].getName())
    for n in range(1, 8):
        if (piece_row - n < 0) or (piece_column - n < 0):
            break
        else:
            if boardFields[piece_row-n][piece_column-n].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
                break
            else:
                if boardFields[piece_row-n][piece_column-n].hasPiece():
                    valid_moves.append(boardFields[piece_row-n][piece_column-n].getName())
                    break
                valid_moves.append(boardFields[piece_row-n][piece_column-n].getName())
    return valid_moves


def getValidQueenMoves(origin_field: Field) -> list:
    valid_moves = getValidBishopMoves(origin_field) + getValidRookMoves(origin_field)
    return valid_moves


def getValidKingMoves(origin_field: Field) -> list:
    player = origin_field.getPiece().getOwner().getPlayer()
    if player == 1:
        enemy_player = 2
    else:
        enemy_player = 1
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = []
    illegal_moves = []
    if player == origin_field.getPiece().getOwner().getPlayer():
        illegal_moves = findIllegalCheckMoves(getAllPlayerField(enemy_player), origin_field)

    for column_in_positiv_x in range(piece_column+1, len(boardFields[piece_row])):
        if boardFields[piece_row][column_in_positiv_x].hasPiece() and not(boardFields[piece_row][column_in_positiv_x].getPiece().getKind() == "Rook"):
            break
        elif boardFields[piece_row][column_in_positiv_x].getPiece().getKind() == "Rook" and boardFields[piece_row][column_in_positiv_x].getPiece().getHasMoved() == False:
            valid_moves.append(boardFields[piece_row][column_in_positiv_x].getName())   
            
    for column_in_negative_x in range(piece_column-1, -1, -1):
        if boardFields[piece_row][column_in_negative_x].hasPiece() and not(boardFields[piece_row][column_in_negative_x].getPiece().getKind() == "Rook"):
            break
        elif boardFields[piece_row][column_in_negative_x].getPiece().getKind() == "Rook" and boardFields[piece_row][column_in_negative_x].getPiece().getHasMoved() == False:
            valid_moves.append(boardFields[piece_row][column_in_negative_x].getName())
    
    if not(piece_row + 1 > 7) and not(piece_column - 1 < 0) and not(boardFields[piece_row+1][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()) and not(containsFieldName(illegal_moves, boardFields[piece_row+1][piece_column-1].getName())):
        if not(checkFutureConflicts(boardFields[piece_row+1][piece_column-1], enemy_player, origin_field)):
            if not(boardFields[piece_row+1][piece_column-1].getPiece().getKind() == "King"):
                valid_moves.append(boardFields[piece_row+1][piece_column-1].getName())
    if not(piece_row + 1 > 7) and not(boardFields[piece_row+1][piece_column].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()) and not(containsFieldName(illegal_moves, boardFields[piece_row+1][piece_column].getName())):
        if not(checkFutureConflicts(boardFields[piece_row+1][piece_column], enemy_player, origin_field)):
            if not(boardFields[piece_row+1][piece_column].getPiece().getKind() == "King"):
                valid_moves.append(boardFields[piece_row+1][piece_column].getName())
    if not(piece_row + 1 > 7) and not(piece_column + 1 > 7) and not(boardFields[piece_row+1][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()) and not(containsFieldName(illegal_moves, boardFields[piece_row+1][piece_column+1].getName())):
        if not(checkFutureConflicts(boardFields[piece_row+1][piece_column+1], enemy_player, origin_field)):
            if not(boardFields[piece_row+1][piece_column+1].getPiece().getKind() == "King"):
                valid_moves.append(boardFields[piece_row+1][piece_column+1].getName())
    if not(piece_row - 1 < 0) and not(piece_column - 1 < 0) and not(boardFields[piece_row-1][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()) and not(containsFieldName(illegal_moves, boardFields[piece_row-1][piece_column-1].getName())):
        if not(checkFutureConflicts(boardFields[piece_row-1][piece_column-1], enemy_player, origin_field)):
            if not(boardFields[piece_row][piece_column-1].getPiece().getKind() == "King"):
                valid_moves.append(boardFields[piece_row-1][piece_column-1].getName())
    if not(piece_row - 1 < 0) and not(boardFields[piece_row-1][piece_column].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()) and not(containsFieldName(illegal_moves, boardFields[piece_row-1][piece_column].getName())):
        if not(checkFutureConflicts(boardFields[piece_row-1][piece_column], enemy_player, origin_field)):
            if not(boardFields[piece_row-1][piece_column].getPiece().getKind() == "King"):
                valid_moves.append(boardFields[piece_row-1][piece_column].getName())
    if not(piece_row - 1 < 0) and not(piece_column + 1 > 7) and not(boardFields[piece_row-1][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()) and not(containsFieldName(illegal_moves, boardFields[piece_row-1][piece_column+1].getName())):
        if not(checkFutureConflicts(boardFields[piece_row-1][piece_column+1], enemy_player, origin_field)):
            if not(boardFields[piece_row-1][piece_column+1].getPiece().getKind() == "King"):
                valid_moves.append(boardFields[piece_row-1][piece_column+1].getName())
    if not(piece_column - 1 < 0) and not(boardFields[piece_row][piece_column-1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()) and not(containsFieldName(illegal_moves, boardFields[piece_row][piece_column-1].getName())):
        if not(checkFutureConflicts(boardFields[piece_row][piece_column-1], enemy_player, origin_field)):
            if not(boardFields[piece_row][piece_column-1].getPiece().getKind() == "King"):
                valid_moves.append(boardFields[piece_row][piece_column-1].getName())
    if not(piece_column + 1 > 7) and not(boardFields[piece_row][piece_column+1].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()) and not(containsFieldName(illegal_moves, boardFields[piece_row][piece_column+1].getName())):
        if not(checkFutureConflicts(boardFields[piece_row][piece_column+1], enemy_player, origin_field)):
            if not(boardFields[piece_row][piece_column+1].getPiece().getKind() == "King"):
                valid_moves.append(boardFields[piece_row][piece_column+1].getName())
    return valid_moves

def findIllegalCheckMoves(fields_to_check: list, origin_field: Field) -> list:
    illegal_moves = []
    piece = origin_field.getPiece()
    origin_field.setPiece(None)
    for field in fields_to_check:
        if not(field.getPiece().getKind() == "King"):
            moves = getValidMoves(field)
            if field.getPiece().getKind() == "Pawn":
                moves = moves + getTheoreticallyPossiblePawnMoves(field)
                if piece.getOwner().getPlayer() == 1:
                    if containsFieldName(moves, boardFields[field.getRow()-1][field.getColumn()].getName()):
                        moves.remove(boardFields[field.getRow()-1][field.getColumn()].getName())
                        if containsFieldName(moves, boardFields[field.getRow()-2][field.getColumn()].getName()):
                            moves.remove(boardFields[field.getRow()-2][field.getColumn()].getName())
                elif piece.getOwner().getPlayer() == 2:
                    if containsFieldName(moves, boardFields[field.getRow()+1][field.getColumn()].getName()):
                        moves.remove(boardFields[field.getRow()+1][field.getColumn()].getName())
                        if containsFieldName(moves, boardFields[field.getRow()+2][field.getColumn()].getName()):
                            moves.remove(boardFields[field.getRow()+2][field.getColumn()].getName())
            for name in moves:
                illegal_moves.append(name)
    origin_field.setPiece(piece)
    return illegal_moves

def checkFutureConflicts(field_to_move_to: Field, enemy_player: int, origin_field: Field) -> bool:
    enemy_fields = getAllPlayerField(enemy_player)
    piece = origin_field.getPiece()
    origin_field.setPiece(None)
    additional_moves = []
    for field in enemy_fields:
        if not(field.getPiece().getKind() == "King"):
            valid_enemy_moves = getValidMoves(field)
            print("Checking: " + field.getName() + " : " + field.getPiece().getKind())
            if field.getPiece().getKind() == "Pawn":
                additional_moves = getTheoreticallyPossiblePawnMoves(field)
                if piece.getOwner().getPlayer() == 1:
                    if containsFieldName(valid_enemy_moves, boardFields[field.getRow()-1][field.getColumn()].getName()):
                        valid_enemy_moves.remove(boardFields[field.getRow()-1][field.getColumn()].getName())
                    if containsFieldName(valid_enemy_moves, boardFields[field.getRow()-2][field.getColumn()].getName()):
                            valid_enemy_moves.remove(boardFields[field.getRow()-2][field.getColumn()].getName())
                elif piece.getOwner().getPlayer() == 2:
                    if containsFieldName(valid_enemy_moves, boardFields[field.getRow()+1][field.getColumn()].getName()):
                        valid_enemy_moves.remove(boardFields[field.getRow()+1][field.getColumn()].getName())
                    if containsFieldName(valid_enemy_moves, boardFields[field.getRow()+2][field.getColumn()].getName()):
                            valid_enemy_moves.remove(boardFields[field.getRow()+2][field.getColumn()].getName())
            if containsFieldName(valid_enemy_moves + additional_moves, field_to_move_to.getName()) == True:
                print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz: " + str(valid_enemy_moves + additional_moves))
                origin_field.setPiece(piece)
                return True

    origin_field.setPiece(piece)


def containsFieldName(list_to_search_in: list, what_to_search_for: str) -> bool:
    for name in list_to_search_in:
        if name == what_to_search_for:
            return True
    return False

def highlightMoves(moves: list, should_highlight: bool):
    if should_highlight:
        for name in moves:
                chessboard.itemconfigure(getFieldByName(name).getId(), fill="#1419a6", activefill="#383fff")
                chessboard.addtag_withtag("Highlighted", getFieldByName(name).getId())
    elif not(should_highlight):
        highlighted_squares = chessboard.find_withtag("Highlighted")
        for id in highlighted_squares:
            tags_of_id = chessboard.gettags(id)
            for tag in tags_of_id:
                if tag == "Black":
                    chessboard.itemconfigure(id, fill=dark_field_color, activefill="#1419a6")
                elif tag == "White":
                    chessboard.itemconfigure(id, fill=light_field_color, activefill="#1419a6")


def movePiece(origin_field: Field, name_of_field_to_move_to: str, depth: int = 0, bIs_simulated: bool = False):
    target_field = getFieldByName(name_of_field_to_move_to)
    transformed_move = transformValidMovesIntoMoveClass(origin_field, target_field, depth)
    global AI_piece_capture
    global piece_capture_history
    if target_field.getName() == origin_field.getName():
        return
    if target_field.hasPiece() and (not(target_field.getPiece().getOwner().getPlayer() == current_player) or bIs_simulated):
        if bIs_simulated:
            AI_piece_capture = True
        captured_piece = transformed_move.getMoveField().getPiece()
        piece_capture_history.append([transformed_move, captured_piece])
        pieceCaptured(origin_field, target_field, bIs_simulated)
    if (origin_field.getPiece().getKind()) == "Pawn" and (target_field.getRow() == 0 or target_field.getRow() == 7):
        promotePawn(origin_field, target_field)
    if origin_field.getPiece().getKind() == "Pawn" and target_field.getRow() == origin_field.getRow() - 2:
        tracked_pawn_fields_2.append(boardFields[origin_field.getRow()-1][origin_field.getColumn()].getName())
    elif origin_field.getPiece().getKind() == "Pawn" and target_field.getRow() == origin_field.getRow() + 2:
        tracked_pawn_fields_1.append(boardFields[origin_field.getRow()+1][origin_field.getColumn()].getName())
    if target_field.getPiece().getKind() == "Rook" and target_field.getPiece().getOwner().getPlayer() == current_player:
        global castle
        castle = True
    else:
        target_field.setPiece(origin_field.getPiece())
        target_field.getPiece().setHasMoved(True)

    if tracked_pawn_fields_2 and origin_field.getPiece().getOwner().getPlayer() == current_player and origin_field.getPiece().getKind() == "Pawn":
        for field_name in tracked_pawn_fields_2:
            print("Checking field " + field_name)
            print("Checking if Pawn on " + boardFields[getFieldByName(field_name).getRow()-1][getFieldByName(field_name).getColumn()].getName())
            if not(boardFields[getFieldByName(field_name).getRow()-1][getFieldByName(field_name).getColumn()].getPiece().getKind() == "Pawn"):
                print("2: removed")
                tracked_pawn_fields_2.remove(field_name)
            elif target_field.getName() == field_name and not(boardFields[getFieldByName(field_name).getRow()-1][getFieldByName(field_name).getColumn()].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                print("2: captured")
                pieceCaptured(origin_field, boardFields[getFieldByName(field_name).getRow()-1][getFieldByName(field_name).getColumn()], bIs_simulated)
                if bIs_simulated:
                    AI_piece_capture = True
                piece_capture_history.append([transformed_move, captured_piece])
                target_field.setPiece(origin_field.getPiece())
                boardFields[getFieldByName(field_name).getRow()-1][getFieldByName(field_name).getColumn()].setPiece(None)
            elif target_field.getName() == field_name and boardFields[getFieldByName(field_name).getRow()-1][getFieldByName(field_name).getColumn()].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
                print("2-else: removed")
                tracked_pawn_fields_2.remove(field_name)
    
    if tracked_pawn_fields_1 and origin_field.getPiece().getOwner().getPlayer() == current_player and origin_field.getPiece().getKind() == "Pawn":
        for field_name in tracked_pawn_fields_1:
            print("Checking field " + field_name)
            print("Checking if Pawn on " + boardFields[getFieldByName(field_name).getRow()+1][getFieldByName(field_name).getColumn()].getName())
            if not(boardFields[getFieldByName(field_name).getRow()+1][getFieldByName(field_name).getColumn()].getPiece().getKind() == "Pawn"):
                print("1: removed")
                tracked_pawn_fields_1.remove(field_name)
            elif target_field.getName() == field_name and not(boardFields[getFieldByName(field_name).getRow()+1][getFieldByName(field_name).getColumn()].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer()):
                print("1: captured")
                pieceCaptured(origin_field, boardFields[getFieldByName(field_name).getRow()+1][getFieldByName(field_name).getColumn()], bIs_simulated)
                if bIs_simulated:
                    AI_piece_capture = True
                piece_capture_history.append([transformed_move, captured_piece])
                target_field.setPiece(origin_field.getPiece())
                boardFields[getFieldByName(field_name).getRow()+1][getFieldByName(field_name).getColumn()].setPiece(None)
            elif target_field.getName() == field_name and boardFields[getFieldByName(field_name).getRow()+1][getFieldByName(field_name).getColumn()].getPiece().getOwner().getPlayer() == origin_field.getPiece().getOwner().getPlayer():
                print("1-else: removed")
                tracked_pawn_fields_1.remove(field_name)


    if castle == True:
        if origin_field.getName() == "E1":
            if target_field.getName() == "A1":
                getFieldByName("C1").setPiece(origin_field.getPiece())
                getFieldByName("C1").getPiece().setHasMoved(True)
                origin_field.setPiece(None)
                getFieldByName("D1").setPiece(target_field.getPiece())
                getFieldByName("D1").getPiece().setHasMoved(True)
                target_field.setPiece(None)
            if target_field.getName() == "H1":
                getFieldByName("G1").setPiece(origin_field.getPiece())
                getFieldByName("G1").getPiece().setHasMoved(True)
                origin_field.setPiece(None)
                getFieldByName("F1").setPiece(target_field.getPiece())
                getFieldByName("F1").getPiece().setHasMoved(True)
                target_field.setPiece(None)
        if origin_field.getName() == "D8":
            if target_field.getName() == "A8":
                getFieldByName("B8").setPiece(origin_field.getPiece())
                getFieldByName("B8").getPiece().setHasMoved(True)
                origin_field.setPiece(None)
                getFieldByName("C8").setPiece(target_field.getPiece())
                getFieldByName("C8").getPiece().setHasMoved(True)
                target_field.setPiece(None)
            if target_field.getName() == "H8":
                getFieldByName("F8").setPiece(origin_field.getPiece())
                getFieldByName("F8").getPiece().setHasMoved(True)
                origin_field.setPiece(None)
                getFieldByName("E8").setPiece(target_field.getPiece())
                getFieldByName("E8").getPiece().setHasMoved(True)
                target_field.setPiece(None)

        castle = False
    else:
        origin_field.setPiece(None)

    global player_1_king_check
    global player_2_king_check
    for name in findPiecesByKind("King"):
        field = getFieldByName(name)
        if checkIfKingCheck(field):
            if current_player == 2:
                    player_1_king_check = True
                    player_1_check_field.config(background=bg_color_if_check_true, foreground=fg_color_if_check_true)
            elif current_player == 1:
                    player_2_king_check = True
                    player_2_check_field.config(background=bg_color_if_check_true, foreground=fg_color_if_check_true)
        else:
            if current_player == 2:
                    player_1_king_check = False
                    player_1_check_field.config(background=chessboard_color, foreground=fg_color_if_check_false)
            elif current_player == 1:
                    player_2_king_check = False
                    player_2_check_field.config(background=chessboard_color, foreground=fg_color_if_check_false)

    print("P1 check: " + str(player_1_king_check))
    print("P2 check: " + str(player_1_king_check))

    for name in findPiecesByKind("King"):
        field = getFieldByName(name)
        if not(getValidKingMoves(field)) and not(is_surrounded_by_allies(field)):
            if not bIs_simulated:
                if field.getPiece().getOwner().getPlayer() == 1:
                    gameWon(2)
                else:
                    gameWon(1)
    #addMoveHistory(origin_field, origin_piece_kind, target_field)
    drawWindow()
    root.update_idletasks()


def promotePawn(origin_field: Field, target_field: Field):
        target_field.setPiece(origin_field.getPiece())
        global promotion_piece
        promotion_piece = getPromotePawnPiece()
        target_field.getPiece().setKind(promotion_piece)
        print("Targetfield kind: " + target_field.getPiece().getKind())
        promotion_piece = "None"


def returnPieceSelected(selected_piece_via_button: str, window: Toplevel, selected_piece_var: StringVar):
    window.destroy()
    # save selection
    selected_piece_var.set(selected_piece_via_button)

def getPromotePawnPiece() -> str:

    optionsWindow = Toplevel()
    selected_piece = StringVar(value="None") # use StringVar instead of normal string
    pawnField = Button(optionsWindow, text="Pawn", anchor=W, command=lambda:
                               returnPieceSelected("Pawn", optionsWindow, selected_piece))
    rookField = Button(optionsWindow, text="Rook", anchor=W, command=lambda:
                               returnPieceSelected("Rook", optionsWindow, selected_piece))
    bishopField = Button(optionsWindow, text="Bishop", anchor=W, command=lambda:
                               returnPieceSelected("Bishop", optionsWindow, selected_piece))
    knightField = Button(optionsWindow, text="Knight", anchor=W, command=lambda:
                               returnPieceSelected("Knight", optionsWindow, selected_piece))
    queenField = Button(optionsWindow, text="Queen", anchor=W, command=lambda:
                               returnPieceSelected("Queen", optionsWindow, selected_piece))

    pawnField.grid(row=1, column=0, sticky=NSEW)
    rookField.grid(row=1, column=1, sticky=NSEW)
    bishopField.grid(row=1, column=3, sticky=NSEW)
    knightField.grid(row=1, column=2, sticky=NSEW)
    queenField.grid(row=1, column=4, sticky=NSEW)

    # wait for user selection
    optionsWindow.wait_window()

    # return user selection
    return selected_piece.get()


def nextPlayer():
    global current_player
    global turn
    if current_player == 1:
        if isAI(current_player):
            player_1_thinking_field.configure(foreground=window_color)
        current_player = 2
        print("Player changed from Player["+ str(current_player-1) + "] to Player[" + str(current_player) + "]")
        player_2_field.configure(background=light_field_color, foreground="Black")
        player_1_field.configure(background=dark_field_color, foreground=white_color_substitute)
    elif current_player == 2:
        if isAI(current_player):
            player_2_thinking_field.configure(foreground=window_color)
        print("Player changed from Player["+ str(current_player) + "] to Player[" + str(current_player-1) + "]")
        current_player = 1
        player_1_field.configure(background=light_field_color, foreground="Black")
        player_2_field.configure(background=dark_field_color, foreground=white_color_substitute)
    turn += 1
    print("Current turn: " + str(turn))
    if isAI(current_player):
        if current_player == 1:
            player_1_thinking_field.configure(foreground=light_field_color)
        if current_player == 2:
            player_2_thinking_field.configure(foreground=light_field_color)
        move(None)


def pieceCaptured(owner_field: Field, captured_field: Field, bIs_simulated: bool):
    owner = owner_field.getPiece().getOwner().getPlayer()
    captured_piece = captured_field.getPiece().getKind()
    if captured_piece == "King" and not bIs_simulated:
        gameWon(owner)

def gameWon(player: int):
    messagebox.showinfo("Game Over", "Player " + str(player) + " has won!")
    resetGame()

def addMoveHistory(starting_field: Field, starting_piece: str, ending_field: Field):
    global turn
    global historylist_length
    move_history.append(MoveRecord(starting_field, ending_field, turn, deepcopy(boardFields), current_player))
    text = "Turn " + str(turn) + " | Player " + str(current_player) + ": " + starting_piece + " -> " + ending_field.getName()
    move_history_field.insert(historylist_length, text)
    historylist_length += 1
        
def restoreSnapshot(event):
    if messagebox.askyesno("Snapshot restoration", "Are you sure you want to restore to a previous turn?\nTurn to jump to: " + str(move_history_field.curselection()[0] + 1)):
        global boardFields
        global turn
        global current_player
        global historylist_length
        global chessboard_displacement
        boardFields = []
        boardFields = move_history[move_history_field.curselection()[0]].getFieldSnapshot()
        turn = move_history[move_history_field.curselection()[0]].getTurn()
        current_player = move_history[move_history_field.curselection()[0]].getCurrentPlayer()
        nextPlayer()

        move_history_field.delete(move_history_field.curselection()[0] + 1, END)
        historylist_length = turn
        #for n in range(historylist_length, len(move_history)):
            #del move_history[n]
        root.update()
        drawChessboard(chessboard_displacement)
        drawPieces()

def resetGame():
    global boardFields
    boardFields = []
    global board_id
    board_id = []
    global hasPieceSelected
    hasPieceSelected = False
    global possible_moves
    possible_moves = []
    global click_history
    click_history = []
    global move_history
    move_history = []
    global turn
    turn = 1
    global historylist_length
    historylist_length = 0
    global promotion_piece
    promotion_piece = "None"

    global isBoard_initialized
    isBoard_initialized = False

    global tracked_pawn_fields_1
    tracked_pawn_fields_1 = []
    global tracked_pawn_fields_2
    tracked_pawn_fields_2 = []

    global castle
    castle = False
    global player_1_king_check
    player_1_king_check = False
    global player_2_king_check
    player_2_king_check = False
    initializeBoard()
    drawWindow()

root.update()
initializeBoard()
drawWindow()

root.bind("<Configure>", drawWindow)
chessboard.bind("<Button-1>", move)
move_history_field.bind("<Double-Button-1>", restoreSnapshot)

root.mainloop()
