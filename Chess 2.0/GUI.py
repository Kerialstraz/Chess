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
    chessboard_line_width = 2

class GUI:
    def __init__(self):
        # Initializies the main window
        self.root = Tk()
        self.root.minsize(1000, 800)
        self.root.title("Chess by Tobias Seipenbusch")

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
            background=GUI_Settings.dark_boardfield_color
        )
        self.chess_move_history_listbox = Listbox(
            self.root,
            background=GUI_Settings.dark_boardfield_color,
        )

        # GUI for the playable chess-field
        self.chessboard = Canvas(
            self.root,
            background=GUI_Settings.dark_boardfield_color
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

    def drawChessboard(self):
        self.chessboard.delete("all")
        self.chessboard.create_rectangle(GUI_Settings.chessboard_displacement / 2, GUI_Settings.chessboard_displacement / 2, self.chessboard.winfo_width() - GUI_Settings.chessboard_displacement / 2,
                                    self.chessboard.winfo_height() - GUI_Settings.chessboard_displacement / 2, width=GUI_Settings.chessboard_line_width, fill="white")
        #drawChessboardRectangles()
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
            # print(str(chessboard.winfo_width()) + " - " + str(chessboard.winfo_height()))
        # for n in range(0, 8):
        #     self.chessboard.create_text((self.chessboard.winfo_width() - GUI_SETTINGS.chessboard_displacement) / 8 * n + (
        #                 self.chessboard.winfo_width() - GUI_SETTINGS.chessboard_displacement) / 16 + GUI_SETTINGS.chessboard_displacement / 2, GUI_SETTINGS.chessboard_displacement / 4,
        #                            text=lettering_bib[n], font=field_letters, fill=light_field_color)
        #     self.chessboard.create_text(GUI_SETTINGS.chessboard_displacement / 4, (self.chessboard.winfo_height() - GUI_SETTINGS.chessboard_displacement) / 8 * n + (
        #                 self.chessboard.winfo_height() - GUI_SETTINGS.chessboard_displacement) / 16 + GUI_SETTINGS.chessboard_displacement / 2, text=numbering_bib[n],
        #                            font=field_letters, fill=light_field_color)
        #     self.chessboard.create_text((chessboard.winfo_width() - GUI_SETTINGS.chessboard_displacement) / 8 * n + (
        #                 self.chessboard.winfo_width() - GUI_SETTINGS.chessboard_displacement) / 16 + GUI_SETTINGS.chessboard_displacement / 2,
        #                            (self.chessboard.winfo_height() - GUI_SETTINGS.chessboard_displacement) + GUI_SETTINGS.chessboard_displacement * (3 / 4),
        #                            text=lettering_bib[n], font=field_letters, fill=light_field_color)
        #     self.chessboard.create_text((self.chessboard.winfo_width() - GUI_SETTINGS.chessboard_displacement) + GUI_SETTINGS.chessboard_displacement * (3 / 4),
        #                            (self.chessboard.winfo_height() - GUI_SETTINGS.chessboard_displacement) / 8 * n + (
        #                                        chessboard.winfo_height() - GUI_SETTINGS.chessboard_displacement) / 16 + GUI_SETTINGS.chessboard_displacement / 2,
        #                            text=numbering_bib[n], font=field_letters, fill=light_field_color)