#Daniel Diaz 74393336
#
# ICS 32 Spring 2014
#

"""
This module contains the Othello game logic
"""

import collections
import copy

NONE = '0'
BLACK = 'B'
WHITE = 'W'

#Othello Settings
#Columns = Board Columns -> must be even between 4 an 16
#Rows = Boards Rows -> must be even between 4 and 16
#start player -> either white or black
#strt disk -> determines color of upper left piece of 4 piece start box
#win mode _. determine win mode by most pieces or least
othello_settings = collections.namedtuple('othello_settings',
    ['columns','rows','start_player', 'start_piece_color', 'win_mode'])
position = collections.namedtuple('position',['x','y'])
vector = collections.namedtuple('vector',['direction','x1','y1','x2','y2'])
#piece_vector = collections.namedtuple('piece_vector',['direction','pieces'])
#pieces is an array of pieces with start at [0] and end at [-1]

class InvalidOthelloMoveError(Exception):
    """invalid move is made"""
    pass

class OthelloGameOverError(Exception):
    """
    Raised whenever an attempt is made to make a move after the game is
    already over
    """
    pass

class piece_vector:

    def __init__(self,direction,piece,temp_board,settings):
        self.direction = direction
        self.start_piece = piece[0]
        self.end_piece = None
        self.piece_array = [piece[0]]
        self.board = temp_board
        self.legit = True
        self.pieces_between_end_points = 0
        self.neighbor = None
        self.recursion_index = 0
        self.settings = settings

    def calc_adjacent_in_direction(self):
        ####NEGATIVE COORDS ARE VALID ARRAY INDEXES SO
        ####NEED TO ADD CHECK TO PREVENT WRAP
        if self.direction == 'S':
            tempx = self.start_piece.x
            tempy = self.start_piece.y + 1
            xcomp = self.settings.columns-1
            ycomp = self.settings.rows-1
            if tempx >= 0 and tempy >= 0 and tempx <= xcomp and tempy <= ycomp:
                self.calc_adjacent_in_dir_with_coords(tempx,tempy)
            else:
                self.legit = False
            return
        if self.direction == 'N':
            tempx = self.start_piece.x
            tempy = self.start_piece.y - 1
            xcomp = self.settings.columns-1
            ycomp = self.settings.rows-1
            if tempx >= 0 and tempy >= 0 and tempx <= xcomp and tempy <= ycomp:
                self.calc_adjacent_in_dir_with_coords(tempx,tempy)
            else:
                self.legit = False
            return
        if self.direction == 'E':
            tempx = self.start_piece.x + 1
            tempy = self.start_piece.y
            xcomp = self.settings.columns-1
            ycomp = self.settings.rows-1
            if tempx >= 0 and tempy >= 0 and tempx <= xcomp and tempy <= ycomp:
                self.calc_adjacent_in_dir_with_coords(tempx,tempy)
            else:
                self.legit = False
            return
        if self.direction == 'W':
            tempx = self.start_piece.x -  1
            tempy = self.start_piece.y
            xcomp = self.settings.columns-1
            ycomp = self.settings.rows-1
            if tempx >= 0 and tempy >= 0 and tempx <= xcomp and tempy <= ycomp:
                self.calc_adjacent_in_dir_with_coords(tempx,tempy)
            else:
                self.legit = False
            return
        if self.direction == 'NE':
            tempx = self.start_piece.x + 1
            tempy = self.start_piece.y - 1
            xcomp = self.settings.columns-1
            ycomp = self.settings.rows-1
            if tempx >= 0 and tempy >= 0 and tempx <= xcomp and tempy <= ycomp:
                self.calc_adjacent_in_dir_with_coords(tempx,tempy)
            else:
                self.legit = False
            return
        if self.direction == 'NW':
            tempx = self.start_piece.x - 1
            tempy = self.start_piece.y - 1
            xcomp = self.settings.columns-1
            ycomp = self.settings.rows-1
            if tempx >= 0 and tempy >= 0 and tempx <= xcomp and tempy <= ycomp:
                self.calc_adjacent_in_dir_with_coords(tempx,tempy)
            else:
                self.legit = False
            return
        if self.direction == 'SE':
            tempx = self.start_piece.x + 1
            tempy = self.start_piece.y + 1
            xcomp = self.settings.columns-1
            ycomp = self.settings.rows-1
            if tempx >= 0 and tempy >= 0 and tempx <= xcomp and tempy <= ycomp:
                self.calc_adjacent_in_dir_with_coords(tempx,tempy)
            else:
                self.legit = False
            return
        if self.direction == 'SW':
            tempx = self.start_piece.x - 1
            tempy = self.start_piece.y + 1
            xcomp = self.settings.columns-1
            ycomp = self.settings.rows-1
            if tempx >= 0 and tempy >= 0 and tempx <= xcomp and tempy <= ycomp:
                self.calc_adjacent_in_dir_with_coords(tempx,tempy)
            else:
                self.legit = False
            return


    def calc_adjacent_in_dir_with_coords(self,tempx,tempy):
        try:
            temp_adj_piece = self.board[tempy][tempx]
        except:
            #catch out of bounds error
            self.legit = False
        else:
            if type(temp_adj_piece) != str and temp_adj_piece.color != self.start_piece.color:
                self.piece_array.append(temp_adj_piece)
                #self.end_piece = temp_adj_piece
            else:
                #piece trying to be palced next to same color
                self.neighbor = False
                self.legit = False
        return

    def general_adjacent_piece(self,tempx,tempy):
        try:
            if self.end_piece is None:
                if tempx < 0 or tempx >= self.settings.columns or tempy < 0 or tempy >= self.settings.rows:
                    raise InvalidOthelloMoveError()
                else:
                    temp_adj_piece = self.board[tempy][tempx]
            else:
                return
        except:
            #catch out of bounds error
            self.legit = False
            return
        else:
            if (temp_adj_piece is not None) and (temp_adj_piece.color != self.start_piece.color):
                self.piece_array.append(temp_adj_piece)
                #self.end_piece = temp_adj_piece
                self.pieces_between_end_points += 1
            elif (temp_adj_piece is not None) and (temp_adj_piece.color == self.start_piece.color):
                self.end_piece = temp_adj_piece
                self.piece_array.append(temp_adj_piece)
            else:
                #if spot is empty
                if type(temp_adj_piece) == str:
                    self.legit = False
        return

    def calc_end_piece(self):
        if self.direction == 'S':
            try:
                if self.end_piece is None:
                    #calculate another neighbor
                    tempx = self.piece_array[-1].x
                    tempy = self.piece_array[-1].y + 1
                    self.general_adjacent_piece(tempx,tempy)
                if self.end_piece is not None:
                    #could still be a legit vector thats just done
                    return
                #added this line for recursion solution!
                #recursively call again
                if self.end_piece is None:
                    self.recursion_index += 1
                    if self.recursion_index < 20:
                        self.calc_end_piece()
                    else:
                        self.legit = False
            except:
                self.legit = False
            return
        if self.direction == 'N':
            try:
                if self.end_piece is None:
                    #calculate another neighbor
                    tempx = self.piece_array[-1].x
                    tempy = self.piece_array[-1].y - 1
                    self.general_adjacent_piece(tempx,tempy)
                if self.end_piece is not None:
                    #could still be a legit vector thats just done
                    return
                #added this line for recursion solution!
                #recursively call again
                if self.end_piece is None:
                    self.recursion_index += 1
                    if self.recursion_index < 20:
                        self.calc_end_piece()
                    else:
                        self.legit = False
            except:
                self.legit = False
            return
        if self.direction == 'E':
            try:
                if self.end_piece is None:
                    #calculate another neighbor
                    tempx = self.piece_array[-1].x + 1
                    tempy = self.piece_array[-1].y
                    self.general_adjacent_piece(tempx,tempy)
                if self.end_piece is not None:
                    #could still be a legit vector thats just done
                    return
                #added this line for recursion solution!
                #recursively call again
                if self.end_piece is None:
                    self.recursion_index += 1
                    #recursion limiter
                    if self.recursion_index < 20:
                        self.calc_end_piece()
                    else:
                        self.legit = False
            except:
                self.legit = False
            return
        if self.direction == 'W':
            try:
                if self.end_piece is None:
                    #calculate another neighbor
                    tempx = self.piece_array[-1].x - 1
                    tempy = self.piece_array[-1].y
                    self.general_adjacent_piece(tempx,tempy)
                if self.end_piece is not None:
                    #could still be a legit vector thats just done
                    return
                #added this line for recursion solution!
                #recursively call again
                if self.end_piece is None:
                    self.recursion_index += 1
                    #recursion limiter
                    if self.recursion_index < 20:
                        self.calc_end_piece()
                    else:
                        self.legit = False
            except:
                self.legit = False
            return
        if self.direction == 'NE':
            try:
                if self.end_piece is None:
                    #calculate another neighbor
                    tempx = self.piece_array[-1].x + 1
                    tempy = self.piece_array[-1].y - 1
                    self.general_adjacent_piece(tempx,tempy)
                if self.end_piece is not None:
                    #could still be a legit vector thats just done
                    return
                #added this line for recursion solution!
                #recursively call again
                if self.end_piece is None:
                    self.recursion_index += 1
                    #recursion limiter
                    if self.recursion_index < 20:
                        self.calc_end_piece()
                    else:
                        self.legit = False
            except:
                self.legit = False
            return
        if self.direction == 'NW':
            try:
                if self.end_piece is None:
                    #calculate another neighbor
                    tempx = self.piece_array[-1].x - 1
                    tempy = self.piece_array[-1].y - 1
                    self.general_adjacent_piece(tempx,tempy)
                if self.end_piece is not None:
                    #could still be a legit vector thats just done
                    return
                #added this line for recursion solution!
                #recursively call again
                if self.end_piece is None:
                    self.recursion_index += 1
                    #recursion limiter
                    if self.recursion_index < 20:
                        self.calc_end_piece()
                    else:
                        self.legit = False
            except:
                self.legit = False
            return
        if self.direction == 'SE':
            try:
                if self.end_piece is None:
                    #calculate another neighbor
                    tempx = self.piece_array[-1].x + 1
                    tempy = self.piece_array[-1].y + 1
                    self.general_adjacent_piece(tempx,tempy)
                if self.end_piece is not None:
                    #could still be a legit vector thats just done
                    return
                #added this line for recursion solution!
                #recursively call again
                if self.end_piece is None:
                    self.recursion_index += 1
                    #recursion limiter
                    if self.recursion_index < 20:
                        self.calc_end_piece()
                    else:
                        self.legit = False
            except:
                self.legit = False
            return
        if self.direction == 'SW':
            try:
                if self.end_piece is None:
                    #calculate another neighbor
                    tempx = self.piece_array[-1].x - 1
                    tempy = self.piece_array[-1].y + 1
                    self.general_adjacent_piece(tempx,tempy)
                if self.end_piece is not None:
                    #could still be a legit vector thats just done
                    return
                #added this line for recursion solution!
                #recursively call again
                if self.end_piece is None:
                    self.recursion_index += 1
                    #recursion limiter
                    if self.recursion_index < 20:
                        self.calc_end_piece()
                    else:
                        self.legit = False
            except:
                self.legit = False
            return

class game_piece:

    def __init__(self,init_color):
        self.color = init_color
        self.x = None
        self.y = None
        self.dirty = False

    def color(self):
        #color can either be black or white
        return self.color

    def set_coords(self,x,y):
        self.x = x
        self.y = y

    def switch(self,piece):
        if self.color == BLACK:
            self.color == 'W'
            self.dirty = True
        else:
            #self.color == 'B'
            piece.color == 'B'
            self.dirty = True

class game:

    def __init__(self, settings):
        #init empty game board
        self.settings = settings
        self.game_board = None
        self.turn = settings.start_player
        self.white_score = 0
        self.black_score = 0
        self.win_mode = settings.win_mode
        self.game_over = False
        self._new_game_board()


    #Public Functions
    def place_piece(self,col_pos,row_pos):
        """ places a piece
        """
        piece = game_piece(self.turn)
        self._require_valid_row(row_pos)
        self._require_valid_col(col_pos)
        self._require_game_not_over()
        piece.set_coords(col_pos,row_pos)
        valid_vectors = None
        valid_vectors = self._is_valid_move(piece)

        if valid_vectors is not None:
            #flip affected pieces
            self._flip_affected_pieces(valid_vectors)
            if type(self.game_board[row_pos][col_pos]) == str:
                self.game_board[row_pos][col_pos] = piece
                self._set_score()
                self._switch_turn()
            else:
                InvalidOthelloMoveError()
        #check game over
        #todo add this back
        self._check_general_game_over()
        #check game over with available moves
        mov_avail = self._check_move_available_for_next_player()
        if mov_avail:
            pass
        else:
            #print('no move available')
            #so u can see what cause the error
            #self._check_move_available_for_next_player()
            print('no more turns available for the next player')
            print('switching to next player')
            self._switch_turn()
            if not self._check_move_available_for_next_player():
                self.game_over = True
        #    self._switch_turn()
        #    if not self._check_move_available_for_next_player():
        #        self.game_over = True
            #print('move available for next player')
            #self._switch_turn()
            #if self._check_move_available_for_next_player:
                #self.game_over = True
        #else:
            #print('no move available')
        return

    def winning_player(self):
        """returns the winning player, none if no winner yetz
        """
        pass

    def game_to_string(self):
        """to string for the game"""
        result = ''
        for x in self.game_board:
            for y in x:
                if y == NONE or None:
                    result = result + str(y) + ' '
                else:
                    #hey its a game piece
                    result = result + y.color + ' '
            result += '\n'
        return result

    #Private Class Functions
    def _set_score(self):
        self.black_score = 0
        self.white_score = 0
        for x in self.game_board:
            for y in x:
                if type(y) != str:
                    if y.color == 'B':
                        self.black_score += 1
                    if y.color == 'W':
                        self.white_score += 1
        return


    def _new_game_board(self):
        """ inits a new game board according to the settings
        """
        #create new game board
        A = [NONE] * self.settings.rows
        for i in range(self.settings.rows):
            A[i] = [NONE] * self.settings.columns
        self.game_board = A
        #place default pices
        #determine starting positions for pieces
        x1 = int((self.settings.columns / 2) - 1)
        y1 = int((self.settings.rows / 2) - 1)
        #print(x1,y1)
        #determine top left piece color
        if self.settings.start_piece_color == WHITE:
            #pass
            #print(x1,y1)
            self.place_start_piece(x1,y1,game_piece(WHITE))
            self.place_start_piece(x1+1,y1,game_piece(BLACK))
            self.place_start_piece(x1+1,y1+1,game_piece(WHITE))
            self.place_start_piece(x1,y1+1,game_piece(BLACK))
        if self.settings.start_piece_color == BLACK:
            #pass
            #print(x1,y1)
            self.place_start_piece(x1,y1,game_piece(BLACK))
            self.place_start_piece(x1+1,y1,game_piece(WHITE))
            self.place_start_piece(x1+1,y1+1,game_piece(BLACK))
            self.place_start_piece(x1,y1+1,game_piece(WHITE))
        return

    def _check_move_available_for_next_player(self):
        #place piece in each spot nd check that a valid vector is returned
        valid_moves = False
        #col_count = 0
        row_count = 0
        temp_piece = game_piece(self.turn)
        for x in self.game_board:
            col_count = 0
            for y in x:
                if type(y) == str:
                    #place dummy piece and see if its valid
                    temp_piece.set_coords(col_count,row_count)
                    valid_vectors = None
                    try:
                        valid_vectors = self._is_valid_move(temp_piece)
                    except:
                        pass
                    else:
                        if len(valid_vectors)>0:
                            valid_moves = True
                col_count += 1
            row_count += 1
        return valid_moves
        #if no_valid_moves is True:
            #self.game_over = True
        #return

    def _check_general_game_over(self):
        game_board_filled = True
        count = 0
        for x in self.game_board:
            for y in x:
                if type(y) == str:
                    #there is a space with a non game piece
                    count += 1
                    game_board_filled = False
        if count == 0 or game_board_filled:
            self.game_over = True

    def place_start_piece(self,col_pos,row_pos,piece):
        """ places a piece
        """
        #dont need to error checking cause its a start piece
        piece.x = col_pos
        piece.y = row_pos
        self.game_board[row_pos][col_pos] = piece
        pass

    def _require_valid_row(self,row):
        if type(row) != int or not self._is_valid_row(row):
            raise ValueError('column_number must be int between 0 and {}'.format(self.settings.rows - 1))

    def _is_valid_row(self,row):
        """Returns True if the given column number is valid; returns False otherwise"""
        return 0 <= row < self.settings.rows

    def _require_valid_col(self,col):
        if type(col) != int or not self._is_valid_row(col):
            raise ValueError('column_number must be int between 0 and {}'.format(self.settings.columns - 1))

    def _is_valid_col(self,col):
        """Returns True if the given row number is valid; returns False otherwise"""
        return 0 <= col < self.settings.columns

    def _require_game_not_over (self):
        """checks game isnt over"""
        if self.game_over:
            raise OthelloGameOverError()
        pass

    def _switch_turn(self):
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def _flip_affected_pieces(self,valid_vectors):
        #fliping all the pieces in the piece array except first and last
        for x in valid_vectors:
            count = 0
            for piece in x.piece_array:
                #skip first and last pieces
                if count == 0 or count == len(x.piece_array)-1:
                    count +=  1
                else:
                    xflip = piece.x
                    yflip = piece.y
                    #temp = self.game_board[yflip][xflip]
                    #for some readon i cant set the color switch from here
                    #just gunna hack it and place a new piece there
                    #temp_old_color = temp.color
                    #temp.switch(temp)
                    replacement_piece = game_piece(self.turn)
                    replacement_piece.dirty = True
                    self.place_start_piece(xflip,yflip,replacement_piece)
                    count += 1
        pass

    def _is_valid_move(self,piece):
        #place piece on temp board
        #create vector from piece to another piece of same color
        #change all piece between vector end points
        temp_board = copy.deepcopy(self.game_board)
        #place piece on temp board
        x = None
        if temp_board[piece.y][piece.x] != type(game_piece):
            temp_board[piece.y][piece.x] = piece
            x = self.calculate_valid_vectors(temp_board,piece)
        if len(x) == 0:
            #no valid moves
            raise InvalidOthelloMoveError()
            #return None
        else:
            return x

    def calculate_valid_vectors(self,temp_board,piece):
        pv_north = piece_vector('N',[piece],temp_board,self.settings)
        pv_east = piece_vector('E',[piece],temp_board,self.settings)
        pv_south = piece_vector('S',[piece],temp_board,self.settings)
        pv_west = piece_vector('W',[piece],temp_board,self.settings)
        pv_north_east = piece_vector('NE',[piece],temp_board,self.settings)
        pv_north_west = piece_vector('NW',[piece],temp_board,self.settings)
        pv_south_east = piece_vector('SE',[piece],temp_board,self.settings)
        pv_south_west = piece_vector('SW',[piece],temp_board,self.settings)


        pv_south.calc_adjacent_in_direction()
        if pv_south.legit is not False:
            pv_south.calc_end_piece()

        pv_north.calc_adjacent_in_direction()
        if pv_north.legit is not False:
            pv_north.calc_end_piece()

        pv_east.calc_adjacent_in_direction()
        if pv_east.legit is not False:
            pv_east.calc_end_piece()

        pv_west.calc_adjacent_in_direction()
        if pv_west.legit is not False:
            pv_west.calc_end_piece()

        pv_north_east.calc_adjacent_in_direction()
        if pv_north_east.legit is not False:
            pv_north_east.calc_end_piece()

        pv_north_west.calc_adjacent_in_direction()
        if pv_north_west.legit is not False:
            pv_north_west.calc_end_piece()

        pv_south_east.calc_adjacent_in_direction()
        if pv_south_east.legit is not False:
            pv_south_east.calc_end_piece()

        pv_south_west.calc_adjacent_in_direction()
        if pv_south_west.legit is not False:
            pv_south_west.calc_end_piece()

        valid_array = []

        if pv_south.legit:
            valid_array.append(pv_south)
        if pv_north.legit:
            valid_array.append(pv_north)
        if pv_east.legit:
            valid_array.append(pv_east)
        if pv_west.legit:
            valid_array.append(pv_west)
        if pv_north_east.legit:
            valid_array.append(pv_north_east)
        if pv_north_west.legit:
            valid_array.append(pv_north_west)
        if pv_south_east.legit:
            valid_array.append(pv_south_east)
        if pv_south_west.legit:
            valid_array.append(pv_south_west)

        return valid_array
