

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
                    if piece == 'p' : 
                        self.get_pawn_moves(r,c,moves)
                    # if piece == 'R' : 
                    #     self.get_rook_moves(r,c,moves)
                    # if piece == 'b' : 
                    #     self.get_bishop_moves(r,c,moves)
                    # if piece == 'N' : 
                    #     self.get_knight_moves(r,c,moves)
                    # if piece == 'K' : 
                    #     self.get_king_moves(r,c,moves)
                    # if piece == 'Q' : 
                    #     self.get_queen_moves(r,c,moves)
        return moves
    def get_pawn_moves(self, r, c, moves) : 
        if self.white_to_move : 
            if self.board[r-1][c] == "--" : 
                moves.append(Move((r,c), (r-1, c), self.board))
                # we can only move a pawn by two if its on its starting place (6th row for white or 1th row for black)
                if r == 6 and self.board[r-2][c] == "--" : 
                    moves.append(Move((r,c), (r-2,c), self.board))
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