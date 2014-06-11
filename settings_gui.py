#Daniel Diaz 74393336
#Settings GUI

import tkinter
import othello

_BACKGROUND_COLOR = '#FFFFFF'
SETTINGS = None
#SETTINGS = othello.othello_settings(6,6,'B','W','+')

class settings_gui:
    def __init__(self):
        #init root window of settings gui
        self._root_window = tkinter.Tk()
        #creat welcome button
        welcome_text = "Welcome to Othello \n To play, select your settings:"
        self.button = tkinter.Label(master = self._root_window, text = welcome_text, font = ('Helvetica', 20))
        self.button.pack()
        #starting player option
        optionList1 = ('Black Player Moves First', 'White Player Moves First')
        self.first_to_move_options_list = tkinter.StringVar()
        self.first_to_move_options_list.set(optionList1[0])
        self.om_first = tkinter.OptionMenu(self._root_window, self.first_to_move_options_list, *optionList1)
        self.om_first.pack()
        #rows
        optionList2 = ('4 ROWS','6 ROWS','8 ROWS','10 ROWS','12 ROWS','14 ROWS','16 ROWS')
        self.rows = tkinter.StringVar()
        self.rows.set(optionList2[0])
        self.om_rows = tkinter.OptionMenu(self._root_window, self.rows, *optionList2)
        self.om_rows.pack()
        #columns
        optionList3 = ('4 Columns','6 Columns','8 Columns','10 Columns','12 Columns','14 Columns','16 Columns')
        self.cols = tkinter.StringVar()
        self.cols.set(optionList3[0])
        self.om_cols = tkinter.OptionMenu(self._root_window, self.cols, *optionList3)
        self.om_cols.pack()
        #upper left piece
        optionList4 = ('W: Upper left piece starts as WHITE','B: Upper left piece starts as Black')
        self.ulp = tkinter.StringVar()
        self.ulp.set(optionList4[0])
        self.om_ulp = tkinter.OptionMenu(self._root_window, self.ulp, *optionList4)
        self.om_ulp.pack()
        #win
        optionList5 = ('+ Player with most pieces wins','- Player with least peices wins')
        self.win = tkinter.StringVar()
        self.win.set(optionList5[0])
        self.om_win = tkinter.OptionMenu(self._root_window, self.win, *optionList5)
        self.om_win.pack()
        #Done
        self.doneButton = tkinter.Button(self._root_window,text='Done!',command=self.set_settings)
        self.doneButton.pack()

    def start(self) -> None:
        self._root_window.mainloop()

    def set_settings(self):
        """take the settings from the options gui and save them to the global settings tuple"""
        #global SETTINGS
        columns = self.cols.get()
        rows = self.rows.get()
        start_player = self.first_to_move_options_list.get()
        start_piece_color = self.ulp.get()
        win_mode = self.win.get()
        temp_settings = othello.othello_settings(columns,rows,start_player,start_piece_color,win_mode)
        clean_settings(temp_settings)
        print('Settings: ',SETTINGS)
        self._root_window.quit()
        return

def clean_settings(temp_settings):
    global SETTINGS
    columns = int(temp_settings.columns[0])
    rows = int(temp_settings.rows[0])
    start_player = temp_settings.start_player[0]
    start_piece_color = temp_settings.start_piece_color[0]
    win_mode = temp_settings.win_mode[0]
    SETTINGS = othello.othello_settings(columns,rows,start_player,start_piece_color,win_mode)
    return

# if __name__ == '__main__':
#     #logic to get the settings info
#     #which is returned as an othello settings tuple
#     settings = settings_gui()
#     settings.start()
