#daniel diaz 74393336
__author__ = 'danieldiaz'

import tkinter
import point
import othello_model
import othello

class OthelloApplication:
    """main game window"""
    def __init__(self,settings):
        #init main window
        self._root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(
            master = self._root_window,
            width=600,
            height = 600,
            background = '#306241'
        )
        self._canvas.grid(
            row = 0,
            column = 0,
            padx = 10,
            pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W
        )
        #events
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        #row config
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

        #self.state = othello_model.OthelloState(settings,self._canvas.winfo_width(),self._canvas.winfo_height())
        self.state = othello_model.OthelloState(settings,606,606)

        self.redraw_game()
        self._canvas.update()


    def start(self) -> None:
        self._root_window.mainloop()

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        #print('canvas resized')
        self.redraw_game()

    def _on_canvas_clicked(self, event) -> None:
        print('canvas clicked')
        click_point = point.from_absolute(
            (event.x, event.y),
            (self._canvas.winfo_width(), self._canvas.winfo_height()))
        #print(event.x,event.y)
        all_tiles_filled = self.state.handle_click(click_point,self._canvas.winfo_width(), self._canvas.winfo_height())
        self.redraw_game()
        self._canvas.update()
        if all_tiles_filled:
            #do game over logic
            self.game_over()


    def game_over(self):
        self._canvas.delete(tkinter.ALL)
        self.redraw_board()
        self._canvas.create_text(150,60,text = "GAME OVER",fill='#FF0000')
        self._canvas.create_text(150,70,text = "THE WINNIER IS: {}".format(self.state.winner),fill='#FF0000')
        #tempposwinner = self.state
        self.draw_score()
        self._canvas.update()

    def redraw_game(self):
        self._canvas.delete(tkinter.ALL)
        #self.draw_score()
        self.redraw_board()
        self.draw_score()
        self.draw_player()
        #self.redraw_disks()
        pass

    def redraw_board(self):
        for tile in self.state.all_tiles():
            #redraw all tiles
            newtopPx,newtopPy = tile.topP.absolute((self._canvas.winfo_width(), self._canvas.winfo_height()))
            newbotPx,newbotPy = tile.botP.absolute((self._canvas.winfo_width(), self._canvas.winfo_height()))
            self._canvas.create_rectangle(newtopPx,newtopPy,newbotPx,newbotPy,fill=tile.color)
            #redraw all disks inside tiles
            if tile.disk is not None:
                self._canvas.create_oval(newtopPx,newtopPy,newbotPx,newbotPy,fill=tile.disk.color)
            #self._canvas.create_oval(newtopPx,newtopPy,newbotPx,newbotPy,fill = '#000000')

    def draw_score(self):
        text = ('BLACK SCORE: {}, WHITE SCORE: {}').format(self.state.black_score,self.state.white_score)
        self._canvas.create_text(150,25,text = text,fill='#FF0000')

    def draw_player(self):
        text = ('The Current Player Is: {}').format(self.state.turn)
        self._canvas.create_text(150,45,text = text,fill='#FF0000')

    def redraw_disks(self):
        pass


# if __name__ == '__main__':
#     settings = othello.othello_settings(6,6,'B','B','+')
#     OthelloApplication(settings).start()


