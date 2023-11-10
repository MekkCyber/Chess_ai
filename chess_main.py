import pygame as p
from chess_engine import Game, Move

BOARD_WIDTH = 512
BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, game_state) : 
    for r in range(DIMENSION) : 
        for c in range(DIMENSION) : 
            piece = game_state[r][c]
            if piece != "--" : 
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    loadImages()
    running = True
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = Game()
    square_selected = ()
    player_click = []
    valid_moves = game_state.get_valid_moves()
    move_made = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN : 
                location = p.mouse.get_pos()
                col = location[0]//SQUARE_SIZE
                row = location[1]//SQUARE_SIZE
                if square_selected == (row, col) : # if the player re-clicks on the same square twice we deselect it
                    square_selected = () 
                    player_click = []
                else :
                    square_selected = (row, col)
                    player_click.append(square_selected)
                if (len(player_click)==2) : # to move a piece we need two clicks : source and destination
                    move = Move(player_click[0], player_click[1], game_state.board)
                    if move in valid_moves : 
                        game_state.make_move(move)
                        move_made = True
                        square_selected = ()
                        player_click = []
                    else : 
                        player_click = [square_selected]
            elif e.type == p.KEYDOWN : 
                if e.key == p.K_z : 
                    game_state.undo_move()
                    move_made = True
        if move_made : 
            valid_moves = game_state.get_valid_moves()
            move_made = False
        draw_board(screen)
        draw_pieces(screen, game_state.board)
        p.display.flip()
main()