

class Game:
    def __init__(self):
        
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.white_to_move = True
        self.logs = []
        self.move_functions = {'p': self.get_pawn_moves, 'N': self.get_knight_moves,
                               'K': self.get_king_moves, 'R': self.get_rook_moves,
                               'Q': self.get_queen_moves, 'B': self.get_bishop_moves}
    
    def make_move(self, move) : 
        self.board[move.src_row][move.src_col] = "--"
        self.board[move.dst_row][move.dst_col] = move.piece_moved
        self.logs.append(move)
        self.white_to_move = not self.white_to_move
    
    def undo_move(self) : 
        if (len(self.logs)!=0) :
            move = self.logs.pop()
            self.board[move.src_row][move.src_col] = move.piece_moved
            self.board[move.dst_row][move.dst_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self) : 
        return self.get_all_possible_moves()
    
    # a move may be possible but not valid (for example moving an other piece when king on check)
    def get_all_possible_moves(self) :
        moves = []
        for r in range(len(self.board)) : 
            for c in range(len(self.board)) : 
                turn = self.board[r][c][0] # this is either "b" for black or "w" for white
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move) :
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves
    def get_pawn_moves(self, r, c, moves) : 
        if self.white_to_move : 
            if self.board[r-1][c] == "--" : 
                moves.append(Move((r,c), (r-1, c), self.board))
                # we can only move a pawn by two if its on its starting place (6th row for white or 1th row for black)
                if r == 6 and self.board[r-2][c] == "--" : 
                    moves.append(Move((r,c), (r-2,c), self.board))
            # capturing logic 
            if c-1 >= 0 : # capture to the left
                # if the piece right above our pawn to the left is black we can capture it
                if self.board[r-1][c-1][0] == "b" : 
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <=7 :
                # if the piece right above our pawn to the right is black we can capture it
                if self.board[r-1][c+1][0] == "b" : 
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        # black to move
        else : 
            if self.board[r+1][c] == "--" : 
                moves.append(Move((r,c), (r+1, c), self.board))
                # we can only move a pawn by two if its on its starting place (6th row for white or 1th row for black)
                if r == 1 and self.board[r+2][c] == "--" : 
                    moves.append(Move((r,c), (r+2,c), self.board))
            # capturing logic 
            if c-1 >= 0 : # capture to the right
                # if the piece right below our pawn to its right is white we can capture it
                if self.board[r+1][c-1][0] == "w" : 
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            if c+1 <=7 :
                # if the piece right above our pawn to its left is white we can capture it
                if self.board[r+1][c+1][0] == "w" : 
                    moves.append(Move((r,c), (r+1,c+1), self.board))

    def get_rook_moves(self, row, col, moves) : 
        # piece_pinned = False
        # pin_direction = ()
        # for i in range(len(self.pins) - 1, -1, -1):
        #     if self.pins[i][0] == row and self.pins[i][1] == col:
        #         piece_pinned = True
        #         pin_direction = (self.pins[i][2], self.pins[i][3])
        #         if self.board[row][col][1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
        #             self.pins.remove(self.pins[i])
        #         break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) 
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check for possible moves only in boundaries of the board
                    # if not piece_pinned or pin_direction == direction or pin_direction == (
                    #         -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break
    def get_bishop_moves(self, row, col, moves) : 
        # piece_pinned = False
        # pin_direction = ()
        # for i in range(len(self.pins) - 1, -1, -1):
        #     if self.pins[i][0] == row and self.pins[i][1] == col:
        #         piece_pinned = True
        #         pin_direction = (self.pins[i][2], self.pins[i][3])
        #         self.pins.remove(self.pins[i])
        #         break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # check if the move is on board
                    # if not piece_pinned or pin_direction == direction or pin_direction == (
                    #         -direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break
    def get_knight_moves(self, row, col, moves) : 
        # piece_pinned = False
        # for i in range(len(self.pins) - 1, -1, -1):
        #     if self.pins[i][0] == row and self.pins[i][1] == col:
        #         piece_pinned = True
        #         self.pins.remove(self.pins[i])
        #         break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))  # up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.white_to_move else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                # if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:  # either enemy piece or empty square 
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_queen_moves(self, r, c, moves) : 
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)
    
    def get_king_moves(self, row, col, moves) : 
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                        moves.append(Move((row, col), (end_row, end_col), self.board))

                    # place king on end square and check for checks
                    # if ally_color == "w":
                    #     self.white_king_location = (end_row, end_col)
                    # else:
                    #     self.black_king_location = (end_row, end_col)
                    # in_check, pins, checks = self.checkForPinsAndChecks()
                    # if not in_check:
                    #     moves.append(Move((row, col), (end_row, end_col), self.board))
                    # # place king back on original location
                    # if ally_color == "w":
                    #     self.white_king_location = (row, col)
                    # else:
                    #     self.black_king_location = (row, col)
class Move :
    # This notation may seem inversed but its because the upper left cell corresponds to (0,0)
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, src_square, dst_square, board) : 
        self.src_row = src_square[0]
        self.src_col = src_square[1]
        self.dst_row = dst_square[0]
        self.dst_col = dst_square[1]
        self.piece_moved = board[self.src_row][self.src_col]
        self.piece_captured = board[self.dst_row][self.dst_col]
        self.move_id = self.src_row*1000 + self.src_col*100 + self.dst_row*10 +self.dst_col

    # we need to override the equal method
    def __eq__(self, other) : 
        if isinstance(other, Move) : 
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self) : 
        return self.get_rank_file(self.src_row, self.src_col)+self.get_rank_file(self.dst_row, self.dst_col)
    def get_rank_file(self, r, c) : 
        return self.cols_to_files[c]+self.rows_to_ranks[r]