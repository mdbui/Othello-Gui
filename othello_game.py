#DANIEL DIAZ 74393336
__author__ = 'danieldiaz'

#RUN THIS FILE!!!

import settings_gui
import othello
import othello_model
import othello_gui

def translate():
    """take the console game board and applies it to the gui"""
def run_game():
    print('OTHELLO GAME STARTED\n')
    #ask for settings
    settings_gui.settings_gui().start()
    #settings is a global var updated by the settings_gui
    #test_settings = othello.othello_settings(6,6,'B','W','+')
    othello_gui.OthelloApplication(settings_gui.SETTINGS).start()

if __name__ == '__main__':
    run_game()