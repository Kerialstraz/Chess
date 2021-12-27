from tkinter import *

class GUI_Settings:
    # Colors
    root_background_color = "#001314"
    playerfield_active_color = "#00eeff"
    playerfield_unactive_color = "#183638"
    light_boardfield_color = "#00eeff"
    dark_boardfield_color = "#183638"
    chessboard_background = "#060c0d"
    light_grey_font_color = "#46e0eb"

    # Fonts
    player_information_font = ("Arial", 16)
    move_history_font = ("Arial", 16)

    # Constants
    chessboard_displacement = 60
    chessboard_line_width = 4

    # Letter Bib
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

    # Number Bib
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

class GUI:
    def __init__(self):
        # Initializies the main window
        self.root = Tk()
        self.root.minsize(800, 800)
        self.root.title("Chess 2.0 by ")

        # Root configurations
        self.root.configure(background=GUI_Settings.root_background_color)

        # Determines the size of the individual rows and column
        # Rows
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=7)

        # Columns
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=5)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=5)
        self.root.columnconfigure(5, weight=1)
        self.root.columnconfigure(6, weight=1)

        # GUI for Player 1
        self.player_1_name_field = Label(
            self.root,
            text="Player 1",
            font=GUI_Settings.player_information_font,
            anchor=W,
            background=GUI_Settings.playerfield_active_color
        )
        self.player_1_check_field = Label(
            self.root,
            text="Player 1 Check",
            font=GUI_Settings.player_information_font,
            anchor=W,
            background=GUI_Settings.playerfield_active_color
        )
        # Only active if the Player is an AI
        self.player_1_thinking_field = Label(
            self.root,
            text="Player 1 Thinking",
            font=GUI_Settings.player_information_font,
            anchor=W,
            background=GUI_Settings.playerfield_active_color
        )

        # GUI for Player 2
        self.player_2_name_field = Label(
            self.root,
            text="Player 2",
            font=GUI_Settings.player_information_font,
            anchor=W,
            background=GUI_Settings.playerfield_unactive_color
        )
        self.player_2_check_field = Label(
            self.root,
            text="Player 2 Check",
            font=GUI_Settings.player_information_font,
            anchor=W,
            background=GUI_Settings.playerfield_unactive_color
        )
        # Only active if the Player is an AI
        self.player_2_thinking_field = Label(
            self.root,
            text="Player 2 Thinking",
            font=GUI_Settings.player_information_font,
            anchor=W,
            background=GUI_Settings.playerfield_unactive_color
        )

        # GUI for the move history
        self.chess_move_history_field = Label(
            self.root,
            text="Move History",
            font=GUI_Settings.move_history_font,
            anchor=W,
            foreground=GUI_Settings.light_grey_font_color,
            background=GUI_Settings.dark_boardfield_color,
            borderwidth=0,
            highlightthickness=0
        )
        self.chess_move_history_listbox = Listbox(
            self.root,
            background=GUI_Settings.dark_boardfield_color,
            borderwidth=0,
            highlightthickness=0
        )

        # GUI for the playable chess-field
        self.chessboard = Canvas(
            self.root,
            background=GUI_Settings.dark_boardfield_color,
            borderwidth=0,
            highlightthickness=3,
            highlightbackground=GUI_Settings.light_boardfield_color
        )

        # Grid Management
        # Player 1
        self.player_1_name_field.grid(
            row=1,
            column=1,
            sticky=NSEW
        )
        self.player_1_check_field.grid(
            row=1,
            column=2,
            sticky=NSEW
        )
        self.player_1_thinking_field.grid(
            row=1,
            column=3,
            sticky=NSEW
        )

        # Player 2
        self.player_2_name_field.grid(
            row=1,
            column=4,
            sticky=NSEW
        )
        self.player_2_check_field.grid(
            row=1,
            column=5,
            sticky=NSEW
        )
        self.player_2_thinking_field.grid(
            row=1,
            column=6,
            sticky=NSEW
        )

        # Move history
        self.chess_move_history_field.grid(
            row=1,
            column=0,
            sticky=NSEW
        )
        self.chess_move_history_listbox.grid(
            row=2,
            rowspan=2,
            column=0,
            sticky=NSEW)

        # chess-board
        self.chessboard.grid(
            row=2,
            column=1,
            columnspan=6,
            sticky=NSEW
        )

        self.board_fields = []
        self.initializeBoard()

        self.chessboard.bind("<Configure>", self.drawWindow)

        self.root.mainloop()

    def drawChessboard(self):
        self.chessboard.delete("all")
        self.chessboard.create_rectangle(GUI_Settings.chessboard_displacement / 2, GUI_Settings.chessboard_displacement / 2, self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement / 2,
                                    self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement / 2, width=GUI_Settings.chessboard_line_width, fill=GUI_Settings.chessboard_background)
        self.drawChessboardRectangles()
        for n in range(1, 8):
            self.chessboard.create_line((self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) / 8 * n + GUI_Settings.chessboard_displacement / 2,
                                   GUI_Settings.chessboard_displacement / 2,
                                   (self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) / 8 * n + GUI_Settings.chessboard_displacement / 2,
                                   self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement / 2, width=GUI_Settings.chessboard_line_width)
            self.chessboard.create_line(GUI_Settings.chessboard_displacement / 2,
                                   (self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) / 8 * n + GUI_Settings.chessboard_displacement / 2,
                                   self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement / 2,
                                   (self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) / 8 * n + GUI_Settings.chessboard_displacement / 2,
                                   width=GUI_Settings.chessboard_line_width)
        for n in range(0, 8):
            self.chessboard.create_text((self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) / 8 * n + (
                        self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) / 16 + GUI_Settings.chessboard_displacement / 2, GUI_Settings.chessboard_displacement / 4,
                                   text=GUI_Settings.lettering_bib[n], font=GUI_Settings.move_history_font, fill=GUI_Settings.light_boardfield_color)
            self.chessboard.create_text(GUI_Settings.chessboard_displacement / 4, (self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) / 8 * n + (
                        self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) / 16 + GUI_Settings.chessboard_displacement / 2, text=GUI_Settings.numbering_bib[n],
                                   font=GUI_Settings.move_history_font, fill=GUI_Settings.light_boardfield_color)
            self.chessboard.create_text((self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) / 8 * n + (
                        self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) / 16 + GUI_Settings.chessboard_displacement / 2,
                                   (self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) + GUI_Settings.chessboard_displacement * (3 / 4),
                                   text=GUI_Settings.lettering_bib[n], font=GUI_Settings.move_history_font, fill=GUI_Settings.light_boardfield_color)
            self.chessboard.create_text((self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) + GUI_Settings.chessboard_displacement * (3 / 4),
                                   (self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) / 8 * n + (
                                               self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) / 16 + GUI_Settings.chessboard_displacement / 2,
                                   text=GUI_Settings.numbering_bib[n], font=GUI_Settings.move_history_font, fill=GUI_Settings.light_boardfield_color)


    def initializeBoard(self):
        for row in range(0, 8):
            self.board_fields.append([])
            for column in range(0, 8):
                self.board_fields[row].append([(0, 0), (0, 0)])


    def adjustBoardFieldsPosition(self):
        for row in range(0, len(self.board_fields)):
            y_coord = (self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) / 8 * (7 - row) + GUI_Settings.chessboard_displacement / 2
            for column in range(0, len(self.board_fields[row])):
                x_coord = (self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) / 8 * (column) + GUI_Settings.chessboard_displacement / 2
                self.board_fields[row][column][0] = (x_coord, y_coord)

    # Adjusts the length/Dimension of the playfield squares
    def adjustBoardFieldsDimension(self):
        for row in range(0, len(self.board_fields)):
            for column in range(0, len(self.board_fields[row])):
                self.board_fields[row][column][1] = ((self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement) / 8 + self.board_fields[row][column][0][0],
                                                    (self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement) / 8 + self.board_fields[row][column][0][1])


    def drawChessboardRectangles(self):
        black_field = True
        field_value = 0
        for row in range(len(self.board_fields)):
            for field in self.board_fields[row]:
                if black_field:
                    self.chessboard.create_rectangle(field[0][0] + GUI_Settings.chessboard_line_width / 2,
                                                     field[0][1] + GUI_Settings.chessboard_line_width / 2,
                                                     field[1][0] - GUI_Settings.chessboard_line_width / 2,
                                                     field[1][1] - GUI_Settings.chessboard_line_width / 2, width=0,
                                                     fill=GUI_Settings.dark_boardfield_color)
                    field_value += 1
                    if field_value % 8 == 0:
                        field_value = 0
                    else:
                        black_field = False
                elif not (black_field):
                    self.chessboard.create_rectangle(field[0][0] + GUI_Settings.chessboard_line_width / 2,
                                                     field[0][1] + GUI_Settings.chessboard_line_width / 2,
                                                     field[1][0] - GUI_Settings.chessboard_line_width / 2,
                                                     field[1][1] - GUI_Settings.chessboard_line_width / 2, width=0,
                                                     fill=GUI_Settings.light_boardfield_color)
                    field_value += 1
                    if field_value % 8 == 0:
                        field_value = 0
                    else:
                        black_field = True

    def drawWindow(self, event=None):
        self.adjustBoardFieldsPosition()
        self.adjustBoardFieldsDimension()
        self.drawChessboard()
        self.root.update()
