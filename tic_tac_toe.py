# Importing modules
import json
import os.path
import sys
import time
from datetime import datetime

import pygame as pg
from pygame.locals import *

# initializing global variables
XO = "x"
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (10, 10, 10)

# TicTacToe 3x3 board
TTT = [[None] * 3, [None] * 3, [None] * 3]
board = [" " for x in range(10)]

# initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
bundle_dir2 = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
bundle_dir3 = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

# loading the images
path_to_opening = os.path.abspath(os.path.join(bundle_dir, "images/tic tac opening.png"))
opening = pg.image.load(path_to_opening)
path_to_x = os.path.abspath(os.path.join(bundle_dir2, "images/x.png"))
x_img = pg.image.load(path_to_x)
path_to_o = os.path.abspath(os.path.join(bundle_dir3, "images/o.png"))
o_img = pg.image.load(path_to_o)

# resizing images
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening = pg.transform.scale(opening, (width, height + 100))


def bconv(TTT):
    # B to T Conversion
    board = [" " for x in range(10)]
    z = 1
    for i in TTT:
        for j in i:
            if j == "x":
                board[z] = "X"
            elif j == "o":
                board[z] = "O"
            else:
                board[z] = " "
            z += 1

    return board


def t_to_b_conversion(board):
    # T to B Conversion
    TTT = [[None] * 3, [None] * 3, [None] * 3]
    z = 1
    for i in range(len(TTT)):
        for j in range(len(TTT[i])):
            if board[z] == "X":
                TTT[i][j] = "x"
            elif board[z] == "O":
                TTT[i][j] = "o"
            else:
                TTT[i][j] = None
            z += 1

    return TTT


def insert_letter(letter, pos):
    board[pos] = letter


def space_is_free(pos):
    return board[pos] == " "


def game_opening():
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)

    # Drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)

    # Drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    draw_status()


def draw_status():
    global draw
    message_winners = []

    if winner is None:

        message = XO.upper() + "'s Turn"
    else:
        if winner.upper() == "O":
            message = "Computer Won!"
            message_winners.append(message)

        else:
            message = "User Won!"
            message_winners.append(message)

    if draw:
        message = "Game Draw!"
        message_winners.append(message)

    if len(message_winners) > 0:
        json_data = {
            "time": f'{datetime.now()}',
            "history": f'{message_winners[0]}'}
        with open("data.json", "a") as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)
            file.write(',\n')

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # copying the rendered message onto the board
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global TTT, winner, draw

    # check for winning rows
    for row in range(0, 3):
        if TTT[row][0] == TTT[row][1] == TTT[row][2] and TTT[row][0] is not None:
            # this row won
            winner = TTT[row][0]
            # draw winning line
            pg.draw.line(
                screen,
                (250, 0, 0),
                (0, (row + 1) * height / 3 - height / 6),
                (width, (row + 1) * height / 3 - height / 6),
                4,
            )
            break

    # check for winning columns
    for col in range(0, 3):
        if TTT[0][col] == TTT[1][col] == TTT[2][col] and TTT[0][col] is not None:
            # this column won
            winner = TTT[0][col]
            # draw winning line
            pg.draw.line(
                screen,
                (250, 0, 0),
                ((col + 1) * width / 3 - width / 6, 0),
                ((col + 1) * width / 3 - width / 6, height),
                4,
            )
            break

    # check for diagonal winners
    if TTT[0][0] == TTT[1][1] == TTT[2][2] and TTT[0][0] is not None:
        # game won diagonally left to right
        winner = TTT[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if TTT[0][2] == TTT[1][1] == TTT[2][0] and TTT[0][2] is not None:
        # game won diagonally right to left
        winner = TTT[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if all([all(row) for row in TTT]) and winner is None:
        draw = True
    draw_status()


def draw_x_or_o(row, col):
    # Draw X or O
    global TTT, XO
    if row == 1:
        posx = 30
    if row == 2:
        posx = width / 3 + 30
    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height / 3 + 30
    if col == 3:
        posy = height / 3 * 2 + 30
    TTT[row - 1][col - 1] = XO
    if XO == "x":
        screen.blit(x_img, (posy, posx))
        XO = "o"
    else:
        screen.blit(o_img, (posy, posx))
        XO = "x"

    pg.display.update()


def user_click():
    # get coordinates of mouse click
    (x, y) = pg.mouse.get_pos()

    # get column of mouse click (1-3)
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # get row of mouse click (1-3)
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and TTT[row - 1][col - 1] is None:
        global XO

        # draw the x or o on screen accordingly
        draw_x_or_o(row, col)
        check_win()


def column_click(move):
    # Getting Row and Column for Drawing Line
    z = 1
    for i in range(3):
        for j in range(3):
            if move == z:
                return (i, j)
            z += 1


def is_winner(bo, le):
    # Checking if anyone wins
    return (
            bo[7] == le
            and bo[8] == le
            and bo[9] == le
            or bo[4] == le
            and bo[5] == le
            and bo[6] == le
            or bo[1] == le
            and bo[2] == le
            and bo[3] == le
            or bo[1] == le
            and bo[4] == le
            and bo[7] == le
            or bo[2] == le
            and bo[5] == le
            and bo[8] == le
            or bo[3] == le
            and bo[6] == le
            and bo[9] == le
            or bo[1] == le
            and bo[5] == le
            and bo[9] == le
            or bo[3] == le
            and bo[5] == le
            and bo[7] == le
    )


def is_board_full(board):
    # Checking if the Board is Full
    if board.count(" ") > 1:
        return False
    else:
        return True


def computer_move():
    # Minimax Algorithm Implementation
    board = bconv(TTT)
    possible_moves = [x for (x, letter) in enumerate(board) if letter == " " and x != 0]
    move = 0

    for let in ["O", "X"]:
        for i in possible_moves:
            boardCopy = board[:]
            boardCopy[i] = let
            if is_winner(boardCopy, let):
                move = i
                return move

    corners_open = []
    for i in possible_moves:
        if i in [1, 3, 7, 9]:
            corners_open.append(i)

    if len(corners_open) > 0:
        move = select_random(corners_open)
        return move

    if 5 in possible_moves:
        move = 5
        return move

    edges_open = []
    for i in possible_moves:
        if i in [2, 4, 6, 8]:
            edges_open.append(i)

    if len(edges_open) > 0:
        move = select_random(edges_open)

    return move


def select_random(li):
    import random

    ln = len(li)
    r = random.randrange(0, ln)
    return li[r]


def reset_game():
    # Reset Game
    global TTT, winner, XO, draw, board
    time.sleep(3)
    XO = "x"
    draw = False
    game_opening()
    winner = None
    TTT = [[None] * 3, [None] * 3, [None] * 3]
    board = [" " for x in range(10)]


game_opening()

# run the game loop forever until someone wins or match draws
while not is_board_full(board):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O accordingly
            board = bconv(TTT)

            if not is_winner(board, "O"):  # User Panel
                user_click()
                board = bconv(TTT)
                check_win()
            else:
                break

            if not is_winner(board, "X"):  # Minimax Panel
                move = computer_move()

                if move == 0:
                    pass
                else:
                    insert_letter("O", move)
                    TTT = t_to_b_conversion(board)
                    (x, y) = column_click(move)
                    draw_x_or_o(x + 1, y + 1)
                    check_win()
            else:
                break

            if winner or draw:
                reset_game()

    pg.display.update()
    CLOCK.tick(fps)
