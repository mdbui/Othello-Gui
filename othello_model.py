#daniel diaz 74393336
__author__ = 'danieldiaz'

import point
import othello
from collections import namedtuple

GREEN = '#306241'
LIGHTGREEN = '#006000'
BLACK_COLOR = '#000000'
WHITE_COLOR = '#FFFFFF'

valid_tile = namedtuple('valid_tile',['col','row','valid'])

class disk:
    def __init__(self,color):
        self.color = color


    def switch_color(self):
        if self.color == BLACK_COLOR:
            self.color = WHITE_COLOR
        else:
            self.color = BLACK_COLOR

class tile:
    """represents a tile on the board and its associated info"""
    def __init__(self,col,row,topP,botP,color):
        self.col = col
        self.row = row

        self.topP = topP
        self.botP = botP

        self.color = color
        self.disk = None

    def contains(self,click_point,w,h):
        click_point_x,click_point_y = click_point.absolute((w,h))
        topPx,topPy = self.topP.absolute((w, h))
        botPx,botPy = self.botP.absolute((w, h))
        if topPx < click_point_x and click_point_x < botPx:
            if topPy < click_point_y and click_point_y < botPy:
                return True

    def place_disk(self,color):
        print('PLacing Disk')
        d = disk(color)
        self.disk = d


class OthelloState:
    """rep othello state"""
    def __init__(self,settings,w,h):
        self._tiles = []
        self.settings = settings
        self.make_init_board(w,h)
        self.turn = settings.start_player
        #self.game = othello.game(settings)
        self.set_start_pieces()
        self.black_score = 2
        self.white_score = 2
        self.winner = None


    def all_tiles(self):
        return self._tiles

    def tile_from_row_col(self,row,col):
        for tile in self._tiles:
            if tile.row == row and tile.col == col:
                return tile

    def handle_click(self,click_point,w,h):
        for tile in self._tiles:
            if tile.contains(click_point,w,h):
                print('You clicked on tile in col: ',tile.col,' and row: ',tile.row)
                #place disk if valid move
                if tile.disk is None:
                    #this is the only req for a valid move
                    print('Placing Disk')
                    if self.turn == 'B':
                        tile.place_disk(BLACK_COLOR)
                    else:
                        tile.place_disk(WHITE_COLOR)
                    self.flip_adjacent(tile)
                    self.update_score()
                    self.change_turn()
        return self.check_a_tile_available()

    def make_init_board(self,w,h):
        box_width = w/self.settings.columns
        box_height = h/self.settings.rows

        count = 0
        for y in range(self.settings.rows):
            count+=1
            for x in range(self.settings.columns):
                topx = int(box_width*x)
                topy = int(box_height*y)
                botx = int(box_width*x + box_width )
                boty = int(box_height*y + box_height )

                topP = point.from_absolute((topx,topy),(w,h))
                botP = point.from_absolute((botx,boty),(w,h))

                if count%2 == 0:
                    color = GREEN
                else:
                    color  = LIGHTGREEN

                t = tile(x,y,topP,botP,color)

                #append new tile to array
                self._tiles.append(t)
                count+=1

    def change_turn(self):
        if self.turn == 'B':
            self.turn = 'W'
        else:
            self.turn = 'B'

    def set_start_pieces(self):
        col_start = int((self.settings.columns / 2) - 1)
        row_start = int((self.settings.rows / 2) - 1)

        if self.settings.start_piece_color == 'W':
            t = self.tile_from_row_col(row_start,col_start)
            t.place_disk(WHITE_COLOR)
            t1 = self.tile_from_row_col(row_start + 1,col_start)
            t1.place_disk(BLACK_COLOR)
            t2 = self.tile_from_row_col(row_start + 1,col_start + 1)
            t2.place_disk(WHITE_COLOR)
            t3 = self.tile_from_row_col(row_start,col_start + 1)
            t3.place_disk(BLACK_COLOR)
        if self.settings.start_piece_color == 'B':
            t = self.tile_from_row_col(row_start,col_start)
            t.place_disk(BLACK_COLOR)
            t1 = self.tile_from_row_col(row_start + 1,col_start)
            t1.place_disk(WHITE_COLOR)
            t2 = self.tile_from_row_col(row_start + 1,col_start + 1)
            t2.place_disk(BLACK_COLOR)
            t3 = self.tile_from_row_col(row_start,col_start + 1)
            t3.place_disk(WHITE_COLOR)

    def flip_adjacent(self,tile):
        col = tile.col
        row = tile.row
        color = tile.disk.color

        #adjacent pieces
        np = valid_tile(col,row-1,True)
        ep = valid_tile(col+1,row,True)
        wp = valid_tile(col-1,row,True)
        sp = valid_tile(col,row+1,True)
        nep = valid_tile(col+1,row-1,True)
        nwp = valid_tile(col-1,row-1,True)
        sep = valid_tile(col+1,row+1,True)
        swp = valid_tile(col-1,row+1,True)

        adj_pieces = [np,ep,wp,sp,nep,nwp,sep,swp]

        valid_adj_pieces = []

        for piece in adj_pieces:
            add_this_piece = True
            if piece.col > self.settings.columns - 1 or piece.col < 0:
                #piece.valid = False
                add_this_piece = False
            if piece.row > self.settings.rows - 1 or piece.row < 0:
                #piece.valid = False
                add_this_piece = False
            if add_this_piece:
                valid_adj_pieces.append(valid_tile(piece.col,piece.row,True))

        for piece in valid_adj_pieces:
            if piece.valid:
                t = self.tile_from_row_col(piece.row,piece.col)
                if t.disk is not None:
                    if t.disk.color != color:
                        t.disk.switch_color()

    def update_score(self):
        self.black_score = 0
        self.white_score = 0
        #add score
        for tile in self._tiles:
            if tile.disk is not None:
                if tile.disk.color == BLACK_COLOR:
                    self.black_score += 1
                else:
                    self.white_score += 1
        #find current win player
        if self.settings.win_mode == '+':
            if self.black_score > self.white_score:
                self.winner = 'BLACK'
            elif (self.black_score == self.white_score):
                self.winner = "None"
            else:
                self.winner = 'WHITE'
            print(self.black_score,self.white_score,self.winner)
        if self.settings.win_mode == '-':
            if self.black_score > self.white_score:
                self.winner = 'WHITE'
            elif (self.black_score == self.white_score):
                self.winner = "None"
            else:
                self.winner = 'BLACK'
            print(self.black_score,self.white_score,self.winner)

    def check_a_tile_available(self):
        all_tiles_filled = True
        for tile in self._tiles:
            if tile.disk is None:
                all_tiles_filled = False
        return all_tiles_filled




# if __name__ == '__main__':
#     settings = othello.othello_settings(6,6,'B','W','+')
#     state = OthelloState(settings,600,600)
#     for x in state.all_tiles():
#         print(x.col,x.row,x.topP.frac_x,x.topP.frac_y,x.botP.frac_x,x.botP.frac_y,x.color)