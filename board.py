import numpy as np
import pygame
import time

pygame.init()

pygame.mixer.quit()

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = SCREEN_WIDTH

checker_color_one = (235, 235, 209)
checker_color_two = (128, 148, 90)

screen = pygame.display.set_mode([SCREEN_WIDTH + 20, SCREEN_HEIGHT + 20])
screen.set_alpha(None)

running = True

CELLS = 16

BOARD = np.zeros(shape=(CELLS,CELLS), dtype=int)

BOARD[1::2,::2] = 1
BOARD[::2,1::2] = 1

PIECES = [["br", "br", "bn", "bn", "bb", "bb", "bq", "bq", "bk", "bq", "bb", "bb", "bn", "bn", "br", "br"],
          ["bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8", "bp9", "bp10", "bp11", "bp12", "bp13", "bp14", "bp15", "bp16"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
          ["wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8", "wp9", "wp10", "wp11", "wp12", "wp13", "wp14", "wp15", "wp16"],
          ["wr", "wr", "wn", "wn", "wb", "wb", "wq", "wq", "wk", "wq", "wb", "wb", "wn", "wn", "wr", "wr"]]

'''PIECES = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
          ["bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"],
          ["0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0"],
          ["0", "0", "0", "0", "0", "0", "0", "0"],
          ["wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"],
          ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
'''
PIECES = np.array(PIECES)

class Piece:
    def __init__(self, piece, width, height, position, screen):
        self.piece = piece
        self.width = int(width)
        self.height = int(height)
        self.position = position
        self.screen = screen
    def load_image(self):
        piece_dir = self.piece[0:2]
        directory = "pieces_images/" + str(piece_dir) + ".png"
        piece = pygame.image.load(directory)
        piece = pygame.transform.scale(piece, (self.width, self.height))
        self.screen.blit(piece, self.position)



CELL_WIDTH = SCREEN_WIDTH/CELLS
CELL_HEIGHT = CELL_WIDTH
CELL_OFFSET = 0

screen.fill((51, 50, 47))

CELL_MATRIX = np.zeros(shape=(CELLS,CELLS), dtype=tuple)
def draw(CELL_OFFSET):

    for i_idx, i in enumerate(BOARD):

        for idx, j in enumerate(i):

            if j == 1:
                pygame.draw.rect(screen, checker_color_one, (10 + (CELL_WIDTH * idx), 10 + CELL_OFFSET, CELL_WIDTH, CELL_HEIGHT))
                piece = PIECES[i_idx][idx]

                position = (10 + (CELL_WIDTH * idx), 10 + CELL_OFFSET)

                CELL_MATRIX[i_idx][idx] = position

                if piece != "0":
                    piece_load = Piece(piece, CELL_WIDTH, CELL_HEIGHT, position, screen)
                    piece_load.load_image()

            else:
                pygame.draw.rect(screen, checker_color_two, (10 + (CELL_WIDTH * idx), 10 + CELL_OFFSET, CELL_WIDTH, CELL_HEIGHT))
                piece = PIECES[i_idx][idx]

                position = (10 + (CELL_WIDTH * idx), 10 + CELL_OFFSET)

                CELL_MATRIX[i_idx][idx] = position

                if piece != "0":
                    piece_load = Piece(piece, CELL_WIDTH, CELL_HEIGHT, position, screen)
                    piece_load.load_image()

        CELL_OFFSET = CELL_OFFSET + CELL_HEIGHT
def check_bishop(piece, s, posx, posy, posx2, posy2, valid_moves, ifqueen):
    if not ifqueen:
        if piece == "wb":
            piece_color = "white"
        else:
            piece_color = "black"
    else:
        if piece == "wq":
            piece_color = "white"
        else:
            piece_color = "black"
    while (posx - 1) >= 0 and (posy - 1) >= 0:
        posx = posx - 1
        posy = posy - 1
        if PIECES[posy][posx] == "0":
            valid_moves.append([posy, posx])
        elif piece_color == "white" and PIECES[posy][posx][0] == "b":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "white" and PIECES[posy][posx][0] == "w":
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "w":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "b":
            break
    posx = posx2
    posy = posy2
    while (posx - 1) >= 0 and (posy + 1) < CELLS:
        posx = posx - 1
        posy = posy + 1
        if PIECES[posy][posx] == "0":
            valid_moves.append([posy, posx])
        elif piece_color == "white" and PIECES[posy][posx][0] == "b":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "white" and PIECES[posy][posx][0] == "w":
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "w":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "b":
            break
    posx = posx2
    posy = posy2
    while (posx + 1) < CELLS and (posy + 1) < CELLS:
        posx = posx + 1
        posy = posy + 1
        if PIECES[posy][posx] == "0":
            valid_moves.append([posy, posx])
        elif piece_color == "white" and PIECES[posy][posx][0] == "b":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "white" and PIECES[posy][posx][0] == "w":
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "w":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "b":
            break
    posx = posx2
    posy = posy2
    while (posx + 1) < CELLS and (posy - 1) >= 0:
        posx = posx + 1
        posy = posy - 1
        if PIECES[posy][posx] == "0":
            valid_moves.append([posy, posx])
        elif piece_color == "white" and PIECES[posy][posx][0] == "b":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "white" and PIECES[posy][posx][0] == "w":
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "w":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "b":
            break
    posx = posx2
    posy = posy2

def check_rook(piece, s, posx, posy, posx2, posy2, valid_moves, ifqueen):
    if not ifqueen:
        if piece == "wr":
            piece_color = "white"
        else:
            piece_color = "black"
    else:
        if piece == "wq":
            piece_color = "white"
        else:
            piece_color = "black"
    while (posy - 1) >= 0:
        posy = posy - 1
        if PIECES[posy][posx] == "0":
            valid_moves.append([posy, posx])
        elif piece_color == "white" and PIECES[posy][posx][0] == "b":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "white" and PIECES[posy][posx][0] == "w":
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "w":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "b":
            break
    posx = posx2
    posy = posy2
    while (posy + 1) < CELLS:
        posy = posy + 1
        if PIECES[posy][posx] == "0":
            valid_moves.append([posy, posx])
        elif piece_color == "white" and PIECES[posy][posx][0] == "b":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "white" and PIECES[posy][posx][0] == "w":
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "w":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "b":
            break
    posx = posx2
    posy = posy2
    while (posx - 1) >= 0:
        posx = posx - 1
        if PIECES[posy][posx] == "0":
            valid_moves.append([posy, posx])
        elif piece_color == "white" and PIECES[posy][posx][0] == "b":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "white" and PIECES[posy][posx][0] == "w":
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "w":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "b":
            break
    posx = posx2
    posy = posy2
    while (posx + 1) < CELLS:
        posx = posx + 1
        if PIECES[posy][posx] == "0":
            valid_moves.append([posy, posx])
        elif piece_color == "white" and PIECES[posy][posx][0] == "b":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "white" and PIECES[posy][posx][0] == "w":
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "w":
            valid_moves.append([posy, posx])
            break
        elif piece_color == "black" and PIECES[posy][posx][0] == "b":
            break
    posx = posx2
    posy = posy2
def check_queen(piece, s, posx, posy, posx2, posy2, valid_moves):
    check_bishop(piece, s, posx, posy, posx2, posy2, valid_moves, True)
    check_rook(piece, s, posx, posy, posx2, posy2, valid_moves, True)
def check_king(piece, s, posx, posy, posx2, posy2, valid_moves):
    if piece == "wk":
        piece_color = "white"
    else:
        piece_color = "black"
    if (posy - 1) >= 0:
        if PIECES[posy - 1][posx] == "0":
            valid_moves.append([posy - 1, posx])
        elif piece_color == "white" and PIECES[posy-1][posx][0] == "b":
            valid_moves.append([posy-1, posx])
        elif piece_color == "black" and PIECES[posy-1][posx][0] == "w":
            valid_moves.append([posy-1, posx])
    if (posy - 1) >= 0 and (posx + 1) < CELLS:
        if PIECES[posy - 1][posx + 1] == "0":
            valid_moves.append([posy - 1, posx + 1])
        elif piece_color == "white" and PIECES[posy-1][posx+1][0] == "b":
            valid_moves.append([posy-1, posx+1])
        elif piece_color == "black" and PIECES[posy-1][posx+1][0] == "w":
            valid_moves.append([posy-1, posx+1])
    if (posx + 1) < CELLS:
        if PIECES[posy][posx + 1] == "0":
            valid_moves.append([posy, posx + 1])
        elif piece_color == "white" and PIECES[posy][posx+1][0] == "b":
            valid_moves.append([posy, posx+1])
        elif piece_color == "black" and PIECES[posy][posx+1][0] == "w":
            valid_moves.append([posy, posx+1])
    if (posy + 1) < CELLS and (posx + 1) < CELLS:
        if PIECES[posy + 1][posx + 1] == "0":
            valid_moves.append([posy + 1, posx + 1])
        elif piece_color == "white" and PIECES[posy+1][posx+1][0] == "b":
            valid_moves.append([posy+1, posx+1])
        elif piece_color == "black" and PIECES[posy+1][posx+1][0] == "w":
            valid_moves.append([posy+1, posx+1])
    if (posy + 1) < CELLS:
        if PIECES[posy + 1][posx] == "0":
            valid_moves.append([posy + 1, posx])
        elif piece_color == "white" and PIECES[posy+1][posx][0] == "b":
            valid_moves.append([posy+1, posx])
        elif piece_color == "black" and PIECES[posy+1][posx][0] == "w":
            valid_moves.append([posy+1, posx])
    if (posy + 1) < CELLS and (posx - 1) >= 0:
        if PIECES[posy + 1][posx - 1] == "0":
            valid_moves.append([posy + 1, posx - 1])
        elif piece_color == "white" and PIECES[posy+1][posx-1][0] == "b":
            valid_moves.append([posy+1, posx-1])
        elif piece_color == "black" and PIECES[posy+1][posx-1][0] == "w":
            valid_moves.append([posy+1, posx-1])
    if (posx - 1) >= 0:
        if PIECES[posy][posx - 1] == "0":
            valid_moves.append([posy, posx - 1])
        elif piece_color == "white" and PIECES[posy][posx-1][0] == "b":
            valid_moves.append([posy, posx-1])
        elif piece_color == "black" and PIECES[posy][posx-1][0] == "w":
            valid_moves.append([posy, posx-1])
    if (posy - 1) >= 0 and (posx - 1) >= 0:
        if PIECES[posy - 1][posx - 1] == "0":
            valid_moves.append([posy - 1, posx - 1])
        elif piece_color == "white" and PIECES[posy-1][posx-1][0] == "b":
            valid_moves.append([posy-1, posx-1])
        elif piece_color == "black" and PIECES[posy-1][posx-1][0] == "w":
            valid_moves.append([posy-1, posx-1])

def check_knight(piece, s, posx, posy, posx2, posy2, valid_moves):
    if piece == "wn":
        piece_color = "white"
    else:
        piece_color = "black"

    if (posy - 2) >= 0:
        if (posx - 1) >= 0:
            if PIECES[posy - 2][posx - 1] == "0":
                valid_moves.append([posy - 2, posx - 1])
            elif piece_color == "white" and PIECES[posy - 2][posx - 1][0] == "b":
                valid_moves.append([posy - 2, posx - 1])
            elif piece_color == "black" and PIECES[posy - 2][posx - 1][0] == "w":
                valid_moves.append([posy - 2, posx - 1])
        if (posx + 1) < CELLS:
            if PIECES[posy - 2][posx + 1] == "0":
                valid_moves.append([posy - 2, posx + 1])
            elif piece_color == "white" and PIECES[posy - 2][posx + 1][0] == "b":
                valid_moves.append([posy - 2, posx + 1])
            elif piece_color == "black" and PIECES[posy - 2][posx + 1][0] == "w":
                valid_moves.append([posy - 2, posx + 1])
    if (posy + 2) < CELLS:
        if (posx - 1) >= 0:
            if PIECES[posy + 2][posx - 1] == "0":
                valid_moves.append([posy + 2, posx - 1])
            elif piece_color == "white" and PIECES[posy + 2][posx - 1][0] == "b":
                valid_moves.append([posy + 2, posx - 1])
            elif piece_color == "black" and PIECES[posy + 2][posx - 1][0] == "w":
                valid_moves.append([posy + 2, posx - 1])
        if (posx + 1) < CELLS:
            if PIECES[posy + 2][posx + 1] == "0":
                valid_moves.append([posy + 2, posx + 1])
            elif piece_color == "white" and PIECES[posy + 2][posx + 1][0] == "b":
                valid_moves.append([posy + 2, posx + 1])
            elif piece_color == "black" and PIECES[posy + 2][posx + 1][0] == "w":
                valid_moves.append([posy + 2, posx + 1])
    if (posx + 2) < CELLS:
        if (posy - 1) >= 0:
            if PIECES[posy - 1][posx + 2] == "0":
                valid_moves.append([posy - 1, posx + 2])
            elif piece_color == "white" and PIECES[posy - 1][posx + 2][0] == "b":
                valid_moves.append([posy - 1, posx + 2])
            elif piece_color == "black" and PIECES[posy - 1][posx + 2][0] == "w":
                valid_moves.append([posy - 1, posx + 2])
        if (posy + 1) < CELLS:
            if PIECES[posy + 1][posx + 2] == "0":
                valid_moves.append([posy + 1, posx + 2])
            elif piece_color == "white" and PIECES[posy + 1][posx + 2][0] == "b":
                valid_moves.append([posy + 1, posx + 2])
            elif piece_color == "black" and PIECES[posy + 1][posx + 2][0] == "w":
                valid_moves.append([posy + 1, posx + 2])
    if (posx - 2) >= 0:
        if (posy - 1) >= 0:
            if PIECES[posy - 1][posx - 2] == "0":
                valid_moves.append([posy - 1, posx - 2])
            elif piece_color == "white" and PIECES[posy - 1][posx - 2][0] == "b":
                valid_moves.append([posy - 1, posx - 2])
            elif piece_color == "black" and PIECES[posy - 1][posx - 2][0] == "w":
                valid_moves.append([posy - 1, posx - 2])
        if (posy + 1) < CELLS:
            if PIECES[posy + 1][posx - 2] == "0":
                valid_moves.append([posy + 1, posx - 2])
            elif piece_color == "white" and PIECES[posy + 1][posx - 2][0] == "b":
                valid_moves.append([posy + 1, posx - 2])
            elif piece_color == "black" and PIECES[posy + 1][posx - 2][0] == "w":
                valid_moves.append([posy + 1, posx - 2])

def show_valid_moves(piece, posx, posy, posx2, posy2):
    posx = posx - 1
    posy = posy - 1
    posx2 = posx2 - 1
    posy2 = posy2 - 1
    valid_moves = []

    if "bp" in piece:
        if posy == 1:
            if PIECES[posy + 1][posx] == "0":
                valid_moves.append([posy + 1, posx])
            if PIECES[posy + 2][posx] == "0":
                valid_moves.append([posy + 2, posx])
        else:
            if PIECES[posy + 1][posx] == "0":
                valid_moves.append([posy + 1, posx])

        if (posy + 1) < CELLS and (posx - 1) >= 0:
            if PIECES[posy + 1][posx - 1][0] == "b":
                valid_moves.append([posy + 1, posx - 1])
        if (posy + 1) < CELLS and (posx + 1) < CELLS:
            if PIECES[posy + 1][posx + 1][0] == "b":
                valid_moves.append([posy + 1, posx + 1])
    elif "wp" in piece:
        if posy == CELLS - 2:
            if PIECES[posy - 1][posx] == "0":
                valid_moves.append([posy - 1, posx])
            if PIECES[posy - 2][posx] == "0":
                valid_moves.append([posy - 2, posx])
        else:
            if PIECES[posy - 1][posx] == "0":
                valid_moves.append([posy - 1, posx])

        if (posy - 1) >= 0 and (posx - 1) >= 0:
            if PIECES[posy - 1][posx - 1][0] == "b":
                valid_moves.append([posy - 1, posx - 1])
        if (posy - 1) >= 0 and (posx + 1) < CELLS:
            if PIECES[posy - 1][posx + 1][0] == "b":
                valid_moves.append([posy - 1, posx + 1])

    elif piece == "bb" or piece == "wb":
        check_bishop(piece, s, posx, posy, posx2, posy2, valid_moves, False)

    elif piece == "bk" or piece == "wk":
        check_king(piece, s, posx, posy, posx2, posy2, valid_moves)

    elif piece == "bn" or piece == "wn":
        check_knight(piece, s, posx, posy, posx2, posy2, valid_moves)

    elif piece == "br" or piece == "wr":
        check_rook(piece, s, posx, posy, posx2, posy2, valid_moves, False)

    elif piece == "bq" or piece == "wq":
        check_queen(piece, s, posx, posy, posx2, posy2, valid_moves)

    return valid_moves

selected = False
selected_first = False
deselect = False
clock = pygame.time.Clock()
draw(CELL_OFFSET)
i_id = 0
id = 0
pygame.display.update()
selected_second = False
s = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
s.set_alpha(128)
s.fill((196, 127, 0))
while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and selected == False:
            x, y = pygame.mouse.get_pos()
            for i_idx, i in enumerate(CELL_MATRIX):
                for idx, j in enumerate(i):
                    if x >= j[0] and x <= j[0] + CELL_WIDTH and y >= j[1] and y <= j[1] + CELL_HEIGHT:
                        piece = PIECES[i_idx][idx]
                        if piece != "0":
                            selected = True
                            i_id = i_idx
                            id = idx
                            nil_destroy_piece = False
                            break

        if selected:
            if not selected_first:
                piece_image = pygame.image.load("pieces_images/" + piece[0:2] + ".png")
                piece_image = pygame.transform.scale(piece_image, (int(CELL_WIDTH), int(CELL_HEIGHT)))
                pygame.draw.rect(screen, (255, 255, 51),
                                 ((10 + CELL_WIDTH * id), (10 + CELL_HEIGHT * i_id), CELL_WIDTH, CELL_HEIGHT), 5)
                selected_first = True
                valid_moves = show_valid_moves(piece, id + 1, i_id + 1, id + 1, i_id + 1)
            x, y = pygame.mouse.get_pos()
            for valid_move in valid_moves:
                screen.blit(s, ((10 + CELL_WIDTH * valid_move[1]), (10 + CELL_HEIGHT * valid_move[0])))
            rect = (x - CELL_WIDTH/2, y - CELL_HEIGHT/2)
            screen.blit(piece_image, rect)
            CELL_OFFSET = 0
            pygame.display.update(piece_image.get_rect())
            screen.fill((51, 50, 47))
            draw(CELL_OFFSET)
            if event.type == pygame.MOUSEBUTTONDOWN and selected_second == True:
                for valid_move in valid_moves:
                    px = valid_move[0]
                    py = valid_move[1]
                    if x >= 10 + py * CELL_WIDTH and x <= 10 + py * CELL_WIDTH + CELL_WIDTH and y >= 10 + px * CELL_HEIGHT and y <= 10 + px * CELL_HEIGHT + CELL_HEIGHT:
                        PIECES[px][py] = piece
                        PIECES[i_id][id] = "0"
                        selected = False
                        selected_first = False
                        selected_second = False
                        CELL_OFFSET = 0
                        screen.fill((51, 50, 47))
                        draw(CELL_OFFSET)
                        pygame.display.update()
                    else:
                        selected = False
                        selected_first = False
                        selected_second = False
                        CELL_OFFSET = 0
                        screen.fill((51, 50, 47))
                        draw(CELL_OFFSET)
                        pygame.display.update()

            if nil_destroy_piece == False:
                selected_second = True
                nil_destroy_piece = True


    pygame.time.wait(0)