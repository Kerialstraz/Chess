from tkinter import * 
from dataclasses import dataclass, field
from typing import *
from copy import deepcopy
from tkinter import messagebox


class Vector2D():
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Owner():
    __player: int
    __color: str

    def __init__(self, player: int, color: str):
        self.__player = player
        self.__color = color

    def getColor(self):
        return self.__color

    def getPlayer(self):
        return self.__player

class Piece():
    __owner: Owner
    __piece_kind: str
    __hasMoved: bool
    __id: int

    def __init__(self, piece_kind: str, owner: Owner):
        self.__piece_kind = piece_kind
        self.__owner = owner
        self.__hasMoved = False
        self.__id = None

    def getKind(self):
        return self.__piece_kind

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
    __name: str #Example A7
    __coordinates: Vector2D #Top-left corner of the square
    __dimension: Vector2D #The x and y span originating from the coordinates
    __piece: Piece #The piece currently on the field, None if there is none
    __row_position: int
    __column_position: int
    __board_id: str

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
            return Piece("None", Owner(0, "None"))

    def getPlayer(self):
        if not(self.__piece == None):
            return self.__piece.__owner.__player
        else:
            return Piece("None", Owner(0, "None"))

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

class MoveRecord():
    __starting_move: Field
    __ending_move: Field
    __turn: int
    __field_snapshot: list
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

root = Tk()
root.minsize(1000, 800)
root.title("Chess by Tobias Seipenbusch")

root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=5)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=5)
root.columnconfigure(4, weight=1)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=7)

boardFields = []
board_id = []
hasPieceSelected = False
possible_moves = []
click_history = []
move_history = []
turn = 1
historylist_length = 0

isBoard_initialized = False

font_1 = ("Arial", 16)
field_letters = ("Arial", 12, "bold")
listbox_font = ("Arial", 12)
white_color_substitute = "#f5f5ff"
chessboard_color = "#060c0d"
window_color = "#001314"
light_field_color = "#00eeff"
dark_field_color = "#183638"
line_width = 4

player_1_color = "White"
player_2_color = "Black"
current_player = 1

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

root.configure(background=window_color)
chessboard = Canvas(root, background=chessboard_color, borderwidth=0, highlightthickness=3, highlightbackground=light_field_color)
chessboard_displacement = 60
player_1_field = Label(root, text="Player 1", anchor=W, background="#EBEBEB", font=font_1, height=0)
player_2_field = Label(root, text="Player 2", anchor=W, background="#EBEBEB", font=font_1, height=0)
player_1_timer_field = Label(root, text="2:00", background=window_color, font=font_1, fg=light_field_color, height=0)
player_2_timer_field = Label(root, text="2:00", background=window_color, font=font_1, fg=light_field_color, height=0)
move_history_label = Label(root, text="History", anchor=W, background=window_color, foreground=light_field_color,font=font_1, height=0)
move_history_field = Listbox(root, background=window_color, foreground=light_field_color, font=listbox_font, width=30, height=20, exportselection=0, borderwidth=0, highlightthickness=0)
menu_button = Menubutton(root, text="Menü", font=field_letters, background=light_field_color, relief=FLAT , borderwidth=0, activebackground="#2cff29", activeforeground="#ff21f8")

chessboard.grid(row=2, column=1, columnspan=4, sticky=NSEW)
player_1_field.grid(row=1, column=1, sticky=NSEW)
player_2_field.grid(row=1, column=3, sticky=NSEW)
player_1_timer_field.grid(row=1, column=2, sticky=NSEW)
player_2_timer_field.grid(row=1, column=4, sticky=NSEW)
move_history_label.grid(row=1, column=0, sticky=NSEW)
move_history_field.grid(row=2, column=0, rowspan=2, sticky=NSEW)
menu_button.grid(row=0, column=0, sticky=W)


def getWindowDimension():
    return Vector2D(root.winfo_width(), root.winfo_height())

def drawWindow(event=None):
    adjustBoardFields(chessboard_displacement)
    drawChessboard(chessboard_displacement)
    drawPieces()

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
    getFieldByName("A2").setPiece(Piece("Pawn", Owner(1, player_1_color)))
    getFieldByName("B2").setPiece(Piece("Pawn", Owner(1, player_1_color)))
    getFieldByName("C2").setPiece(Piece("Pawn", Owner(1, player_1_color)))
    getFieldByName("D2").setPiece(Piece("Pawn", Owner(1, player_1_color)))
    getFieldByName("E2").setPiece(Piece("Pawn", Owner(1, player_1_color)))
    getFieldByName("F2").setPiece(Piece("Pawn", Owner(1, player_1_color)))
    getFieldByName("G2").setPiece(Piece("Pawn", Owner(1, player_1_color)))
    getFieldByName("H2").setPiece(Piece("Pawn", Owner(1, player_1_color)))
    # Player 2 Pawns
    getFieldByName("A7").setPiece(Piece("Pawn", Owner(2, player_2_color)))
    getFieldByName("B7").setPiece(Piece("Pawn", Owner(2, player_2_color)))
    getFieldByName("C7").setPiece(Piece("Pawn", Owner(2, player_2_color)))
    getFieldByName("D7").setPiece(Piece("Pawn", Owner(2, player_2_color)))
    getFieldByName("E7").setPiece(Piece("Pawn", Owner(2, player_2_color)))
    getFieldByName("F7").setPiece(Piece("Pawn", Owner(2, player_2_color)))
    getFieldByName("G7").setPiece(Piece("Pawn", Owner(2, player_2_color)))
    getFieldByName("H7").setPiece(Piece("Pawn", Owner(2, player_2_color)))

def initializeRooks():
    # Player 1 Rooks
    getFieldByName("A1").setPiece(Piece("Rook", Owner(1, player_1_color)))
    getFieldByName("H1").setPiece(Piece("Rook", Owner(1, player_1_color)))
    # Player 2 Rooks
    getFieldByName("A8").setPiece(Piece("Rook", Owner(2, player_2_color)))
    getFieldByName("H8").setPiece(Piece("Rook", Owner(2, player_2_color)))

def initializeKnights():
    # Player 1 Knights
    getFieldByName("B1").setPiece(Piece("Knight", Owner(1, player_1_color)))
    getFieldByName("G1").setPiece(Piece("Knight", Owner(1, player_1_color)))
    # Player 2 Knights
    getFieldByName("B8").setPiece(Piece("Knight", Owner(2, player_2_color)))
    getFieldByName("G8").setPiece(Piece("Knight", Owner(2, player_2_color)))

def initializeBishops():
    # Player 1 Bishops
    getFieldByName("C1").setPiece(Piece("Bishop", Owner(1, player_1_color)))
    getFieldByName("F1").setPiece(Piece("Bishop", Owner(1, player_1_color)))
    # Player 2 Bishops
    getFieldByName("C8").setPiece(Piece("Bishop", Owner(2, player_2_color)))
    getFieldByName("F8").setPiece(Piece("Bishop", Owner(2, player_2_color)))

def initializeQueens():
    # Player 1 Queen
    getFieldByName("D1").setPiece(Piece("Queen", Owner(1, player_1_color)))
    # Player 2 Queen
    getFieldByName("E8").setPiece(Piece("Queen", Owner(2, player_2_color)))

def initializeKings():
    # Player 1 King
    getFieldByName("E1").setPiece(Piece("King", Owner(1, player_1_color)))
    # Player 2 King
    getFieldByName("D8").setPiece(Piece("King", Owner(2, player_2_color)))

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
    field_clicked = getFieldClicked(event)
    global hasPieceSelected
    global possible_moves
    isOutside_of_possible_moves = False

    # Checkt ob ein Feld geklickt wurde
    if not(field_clicked == None):
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

        for possible_field in range(0, len(possible_moves)):
            if field_clicked.getName() == possible_moves[possible_field]:
                click_history.append(field_clicked)
                movePiece(click_history[len(click_history)-2], possible_moves[possible_field])
                possible_moves.clear()
                hasPieceSelected = False
                return
            else:
                isOutside_of_possible_moves = True

        if hasPieceSelected == True and isOutside_of_possible_moves == True:
            # Goes through all possible moves and checks if the current click is one of the possible moves, if not, deselect
            for name in possible_moves:
                if not(field_clicked.getName() == name):
                    highlightMoves(possible_moves, False)
                    hasPieceSelected = False
                    possible_moves = []

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

def getValidMoves(origin_field: Field) -> list:
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

def getValidPawnMoves(origin_field: Field) -> list:
    player = origin_field.getPiece().getOwner().getPlayer()
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = []
    if player == 1:
        if piece_row == 1:
            valid_moves.append(boardFields[piece_row+2][piece_column].getName())
        if not(boardFields[piece_row+1][piece_column].hasPiece()):
            valid_moves.append(boardFields[piece_row+1][piece_column].getName())

        if piece_column == 0:
            if boardFields[piece_row+1][piece_column+1].hasPiece():
                if not(boardFields[piece_row+1][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
                    valid_moves.append(boardFields[piece_row+1][piece_column+1].getName())
        elif piece_column == 7:
            if boardFields[piece_row+1][piece_column-1].hasPiece():
                if not(boardFields[piece_row+1][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
                    valid_moves.append(boardFields[piece_row+1][piece_column-1].getName())
        else:
            if boardFields[piece_row+1][piece_column-1].hasPiece():
                if not(boardFields[piece_row+1][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
                    valid_moves.append(boardFields[piece_row+1][piece_column-1].getName())
            if boardFields[piece_row+1][piece_column+1].hasPiece():
                if not(boardFields[piece_row+1][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
                    valid_moves.append(boardFields[piece_row+1][piece_column+1].getName())
    elif player == 2:
        if piece_row == 6:
            valid_moves.append(boardFields[piece_row-2][piece_column].getName())
        if not(boardFields[piece_row-1][piece_column].hasPiece()):
            valid_moves.append(boardFields[piece_row-1][piece_column].getName())

        if piece_column == 0:
            if boardFields[piece_row-1][piece_column+1].hasPiece():
                if not(boardFields[piece_row-1][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
                    valid_moves.append(boardFields[piece_row-1][piece_column+1].getName())
        elif piece_column == 7:
            if boardFields[piece_row-1][piece_column-1].hasPiece():
                if not(boardFields[piece_row-1][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
                    valid_moves.append(boardFields[piece_row-1][piece_column-1].getName())
        else:
            if boardFields[piece_row-1][piece_column-1].hasPiece():
                if not(boardFields[piece_row-1][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
                    valid_moves.append(boardFields[piece_row-1][piece_column-1].getName())
            if boardFields[piece_row-1][piece_column+1].hasPiece():
                if not(boardFields[piece_row-1][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
                    valid_moves.append(boardFields[piece_row-1][piece_column+1].getName())
    return valid_moves

def getValidRookMoves(origin_field: Field) -> list:
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = []
    for row_in_positiv_x in range(piece_row+1, len(boardFields)):
        if boardFields[row_in_positiv_x][piece_column].getPiece().getOwner().getPlayer() == current_player:
            break
        else:
            valid_moves.append(boardFields[row_in_positiv_x][piece_column].getName())
            if boardFields[row_in_positiv_x][piece_column].hasPiece():
                break
    for row_in_negative_x in range(piece_row-1, -1, -1):
        if boardFields[row_in_negative_x][piece_column].getPiece().getOwner().getPlayer() == current_player:
            break
        else:
            valid_moves.append(boardFields[row_in_negative_x][piece_column].getName())
            if boardFields[row_in_negative_x][piece_column].hasPiece():
                break
    for column_in_positiv_x in range(piece_column+1, len(boardFields[piece_row])):
        if boardFields[piece_row][column_in_positiv_x].getPiece().getOwner().getPlayer() == current_player:
            break
        else:
            valid_moves.append(boardFields[piece_row][column_in_positiv_x].getName())
            if boardFields[piece_row][column_in_positiv_x].hasPiece():
                break
    for column_in_negative_x in range(piece_column-1, -1, -1):
        if boardFields[piece_row][column_in_negative_x].getPiece().getOwner().getPlayer() == current_player:
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
            if not(boardFields[piece_row+2][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
                valid_moves.append(boardFields[piece_row+2][piece_column+1].getName())
    if not(piece_row + 2 > 7):
        if not(piece_column - 1 < 0):
            if not(boardFields[piece_row+2][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
                valid_moves.append(boardFields[piece_row+2][piece_column-1].getName())
    if not(piece_row + 1 > 7):
        if not(piece_column + 2 > 7):
            if not(boardFields[piece_row+1][piece_column+2].getPiece().getOwner().getPlayer() == current_player):
                valid_moves.append(boardFields[piece_row+1][piece_column+2].getName())
    if not(piece_row + 1 > 7):
        if not(piece_column - 2 < 0):
            if not(boardFields[piece_row+1][piece_column-2].getPiece().getOwner().getPlayer() == current_player):
                valid_moves.append(boardFields[piece_row+1][piece_column-2].getName())
    if not(piece_row - 2 < 0):
        if not(piece_column + 1 > 7):
            if not(boardFields[piece_row-2][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
                valid_moves.append(boardFields[piece_row-2][piece_column+1].getName())
    if not(piece_row - 2 < 0):
        if not(piece_column - 1 < 0):
            if not(boardFields[piece_row-2][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
                valid_moves.append(boardFields[piece_row-2][piece_column-1].getName())
    if not(piece_row - 1 < 0):
        if not(piece_column + 2 > 7):
            if not(boardFields[piece_row-1][piece_column+2].getPiece().getOwner().getPlayer() == current_player):
                valid_moves.append(boardFields[piece_row-1][piece_column+2].getName())
    if not(piece_row - 1 < 0):
        if not(piece_column - 2 < 0):
            if not(boardFields[piece_row-1][piece_column-2].getPiece().getOwner().getPlayer() == current_player):
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
            if boardFields[piece_row+n][piece_column+n].getPiece().getOwner().getPlayer() == current_player:
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
            if boardFields[piece_row+n][piece_column-n].getPiece().getOwner().getPlayer() == current_player:
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
            if boardFields[piece_row-n][piece_column+n].getPiece().getOwner().getPlayer() == current_player:
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
            if boardFields[piece_row-n][piece_column-n].getPiece().getOwner().getPlayer() == current_player:
                break
            else:
                if boardFields[piece_row-n][piece_column-n].hasPiece():
                    valid_moves.append(boardFields[piece_row-n][piece_column-n].getName())
                    break
                valid_moves.append(boardFields[piece_row-n][piece_column-n].getName())
    return valid_moves

def getValidQueenMoves(origin_field: Field) -> list:
    player = origin_field.getPiece().getOwner().getPlayer()
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = getValidBishopMoves(origin_field) + getValidRookMoves(origin_field)
    return valid_moves

def getValidKingMoves(origin_field: Field) -> list:
    player = origin_field.getPiece().getOwner().getPlayer()
    piece_row = origin_field.getRow()
    piece_column = origin_field.getColumn()
    valid_moves = []
    if not(piece_row + 1 > 7) and not(piece_column - 1 < 0) and not(boardFields[piece_row+1][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
        valid_moves.append(boardFields[piece_row+1][piece_column-1].getName())
    if not(piece_row + 1 > 7) and not(boardFields[piece_row+1][piece_column].getPiece().getOwner().getPlayer() == current_player):
        valid_moves.append(boardFields[piece_row+1][piece_column].getName())
    if not(piece_row + 1 > 7) and not(piece_column + 1 > 7) and not(boardFields[piece_row+1][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
        valid_moves.append(boardFields[piece_row+1][piece_column+1].getName())
    if not(piece_row - 1 < 0) and not(piece_column - 1 < 0) and not(boardFields[piece_row-1][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
        valid_moves.append(boardFields[piece_row-1][piece_column-1].getName())
    if not(piece_row - 1 < 0) and not(boardFields[piece_row-1][piece_column].getPiece().getOwner().getPlayer() == current_player):
        valid_moves.append(boardFields[piece_row-1][piece_column].getName())
    if not(piece_row - 1 < 0) and not(piece_column + 1 > 7) and not(boardFields[piece_row-1][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
        valid_moves.append(boardFields[piece_row-1][piece_column+1].getName())
    if not(piece_column - 1 < 0) and not(boardFields[piece_row][piece_column-1].getPiece().getOwner().getPlayer() == current_player):
        valid_moves.append(boardFields[piece_row][piece_column-1].getName())
    if not(piece_column + 1 > 7) and not(boardFields[piece_row][piece_column+1].getPiece().getOwner().getPlayer() == current_player):
        valid_moves.append(boardFields[piece_row][piece_column+1].getName())
    return valid_moves

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

def movePiece(origin_field: Field, name_of_field_to_move_to: str):
    target_field = getFieldByName(name_of_field_to_move_to)
    if target_field.getName() == origin_field.getName():
        return
    if target_field.hasPiece():
        pieceCaptured(origin_field, target_field)
    target_field.setPiece(origin_field.getPiece())
    origin_piece_kind = origin_field.getPiece().getKind()
    origin_field.setPiece(None)

    addMoveHistory(origin_field, origin_piece_kind, target_field)
    nextPlayer()
    
    drawWindow()

def nextPlayer():
    global current_player
    global turn
    if current_player == 1:
        current_player = 2
        print("Player changed from Player["+ str(current_player-1) + "] to Player[" + str(current_player) + "]")
        player_2_field.configure(background=light_field_color, foreground="Black")
        player_1_field.configure(background=dark_field_color, foreground=white_color_substitute)
    elif current_player == 2:
        print("Player changed from Player["+ str(current_player) + "] to Player[" + str(current_player-1) + "]")
        current_player = 1
        player_1_field.configure(background=light_field_color, foreground="Black")
        player_2_field.configure(background=dark_field_color, foreground=white_color_substitute)
    turn += 1
    print("Current turn: " + str(turn))

def pieceCaptured(owner_field: Field, captured_field: Field):
    owner = owner_field.getPiece().getOwner().getPlayer()
    captured_piece = captured_field.getPiece().getKind()
    if captured_piece == "King":
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
    initializeBoard()
    drawWindow()

root.update()
initializeBoard()
drawWindow()

root.bind("<Configure>", drawWindow)
chessboard.bind("<Button-1>", move)
move_history_field.bind("<Double-Button-1>", restoreSnapshot)

root.mainloop()
