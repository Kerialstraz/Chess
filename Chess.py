from tkinter import * 
from dataclasses import dataclass
from typing import *


class Vector2D():
    x: int
    y: int
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Field():
    coordinates: Vector2D
    dimension: Vector2D
    def __init__(self, coordinates: Vector2D, dimension: Vector2D):
        self.coordinates = coordinates
        self.dimension = dimension

class Owner():
    player: int
    color: str

class Piece():
    field: Field
    owner: Owner
    piece_kind: str


root = Tk()
root.minsize(800, 800)
root.title("Chess by Tobias Seipenbusch")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=5)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=5)
root.columnconfigure(4, weight=1)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=7)

font_1 = ("Helvetica", 16)

chessboard = Canvas(root, background="#ffdead")
player_1_field = Label(root, text="Player 1", anchor=W, background="grey", font=font_1, height=-20)
player_2_field = Label(root, text="Player 2", anchor=W, background="grey", font=font_1, height=-20)
player_1_pieces_captured_field = Canvas(root, background="#ff0000", height=-30)
player_2_pieces_captured_field = Canvas(root, background="#ff0000", height=-30)
player_1_timer_field = Label(root, text="Timer P1", anchor=W, background="black", font=font_1, fg="white", height=-20)
player_2_timer_field = Label(root, text="Timer P2", anchor=W, background="black", font=font_1, fg="white", height=-20)
move_history_label = Label(root, text="History", anchor=W, background="grey", font=font_1, height=-20)
move_history_field = Listbox(root, background="grey", font=font_1, width=15)

chessboard.grid(row=2, column=1, columnspan=4, sticky=NSEW)
player_1_field.grid(row=0, column=1, sticky=NSEW)
player_2_field.grid(row=0, column=3, sticky=NSEW)
player_1_pieces_captured_field.grid(row=1, column=1, columnspan=2, sticky=NSEW)
player_2_pieces_captured_field.grid(row=1, column=3, columnspan=2, sticky=NSEW)
player_1_timer_field.grid(row=0, column=2, sticky=NSEW)
player_2_timer_field.grid(row=0, column=4, sticky=NSEW)
move_history_label.grid(row=0, column=0, sticky=NSEW)
move_history_field.grid(row=1, column=0, rowspan=2, sticky=NSEW)

def getWindowDimension():
    return Vector2D(root.winfo_width(), root.winfo_height())

def drawWindow():
    return

def drawChessboard(chessboard):
    for n in range(0, 7):
        chessboard.create_line(getWindowDimension().x - chessboard.winfo_width(), getWindowDimension().y - chessboard.winfo_height(), chessboard.winfo_width(), getWindowDimension().y, width=2)

drawChessboard(chessboard)

root.mainloop()