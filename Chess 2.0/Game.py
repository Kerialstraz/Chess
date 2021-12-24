from GUI import GUI
from Board import Board

class Game():
    def __init__(self):
        self.GUI = GUI()
        self.board = Board()
        self.GUI.drawChessboard()
        self.GUI.root.mainloop()


Game()