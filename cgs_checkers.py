import pygame as pg, pickle
from math import pi
import cgs
from random import randint


def build_board():
    """This function creates the initial model that represents the board before any moves are made."""
    board = []  # builds the board that will be modified throughout the game
    for i in range(8):
        board.append([])
        for j in range(8):
            if i < 3 and on_dark(i, j):
                board[i].append(1)
            elif i > 4 and on_dark(i, j):
                board[i].append(2)
            else:
                board[i].append(0)
    cgs.draw_records(screen, 2, mode, logged_in, difficulty)  # draws left panel of screen
    return board


def get_move():
    """This function returns data about the current state of the game based on the global turn variable."""
    if turn % 2 == 0:
        color = (0, 0, 0)  # color to be used
        piece = 2  # current player's piece
        king = 4  # current player's piece (king)
        word = 'BLACK'  # word to be used
        turned = 1  # opposing player's piece
        king_turn = 3  # opposing player's piece

    else:
        color = (50, 70, 90)  # color to be used
        piece = 1  # current player's piece
        king = 3   # current player's piece (king)
        word = 'WHITE'  # word to be used
        turned = 2  # opposing player's piece
        king_turn = 4  # opposing player's piece

    return color, piece, king, word, turned, king_turn


def on_dark(i, j):
    """This function returns True if the current piece being checked has a dark background (either odd row or column)"""
    if i % 2 == 0 and j % 2 != 0:  # if column is even and row is odd
        return True
    elif i % 2 != 0 and j % 2 == 0:   # if column is odd and row is even
        return True
    else:
        return False


def get_coordinates(x, y):
    """This function accepts x and y coordinates and returns the reformatted coordinates to fit board"""
    x = (x - 250) // 75  # 250px shift right and then each row is 75
    y = (650 - y) // 75    # 650 shift down and then each column is 75
    return [y, x]


def on_board(y, x):
    """This function ensures that the move that is about to be examined is actually on the board."""
    if 0 <= y <= 7 and 0 <= x <= 7:  # ensures that both the x and y values are between 0 and 7
        return True
    else:
        return False


def check_moves(array, turned, king_turn, piece, x, y, state):
    """This function determines all of the potential moves and its corresponding flips
    for a given piece on the board. If it is checking a normal piece then it checks for either up or down depending
    on side of board and right and left. If it is checking a king then it checks for both up and down and right and left
    ."""
    switches = []
    options = []

    if state == 'reg':  # if non-king piece being checked
        if piece == 1:  # if user's turn
            if on_board(y + 1, x - 1) and array[y + 1][x - 1] == 0:  # check if 1 up and 1 left is open
                options.append([y + 1, x - 1])  # add it to options if it is
                switches.append([])
            if on_board(y + 1, x - 1) and on_board(y + 2, x - 2) and \
                    (array[y + 1][x - 1] == turned or array[y + 1][x - 1] == king_turn) \
                    and array[y + 2][x - 2] == 0:  # check if sandwich exists where up 1, left 1 is captured
                options.append([y + 2, x - 2])
                switches.append([y + 1, x - 1])
            if on_board(y + 1, x + 1) and array[y + 1][x + 1] == 0:   # check if 1 up and 1 right is open
                options.append([y + 1, x + 1])
                switches.append([])
            if on_board(y + 1, x + 1) and on_board(y + 2, x + 2) and \
                    (array[y + 1][x + 1] == turned or array[y + 1][x + 1] == king_turn) \
                    and array[y + 2][x + 2] == 0:  # check if sandwich exists where up 1, right 1 is captured
                options.append([y + 2, x + 2])
                switches.append([y + 1, x + 1])

        elif piece == 2:  # if user's turn
            if on_board(y - 1, x - 1) and array[y - 1][x - 1] == 0:  # check if 1 down and 1 left is open
                options.append([y - 1, x - 1])
                switches.append([])
            if on_board(y - 1, x - 1) and on_board(y - 2, x - 2) and \
                    (array[y - 1][x - 1] == turned or array[y - 1][x - 1] == king_turn) \
                    and array[y - 2][x - 2] == 0:   # check if sandwich exists where down 1, left 1 is captured
                options.append([y - 2, x - 2])
                switches.append([y - 1, x - 1])
            if on_board(y - 1, x + 1) and array[y - 1][x + 1] == 0:  # check if 1 down and 1 right is open
                options.append([y - 1, x + 1])
                switches.append([])
            if on_board(y - 1, x + 1) and on_board(y - 2, x + 2) and \
                    (array[y - 1][x + 1] == turned or array[y - 1][x + 1] == king_turn) \
                    and array[y - 2][x + 2] == 0:   # check if sandwich exists where up 1, right 1 is captured
                options.append([y - 2, x + 2])
                switches.append([y - 1, x + 1])

    elif state == 'king':  # if king piece being checked then can move back or forward (U= Up, D= Dwn, L= lft, R = rt)
        if on_board(y + 1, x - 1) and array[y + 1][x - 1] == 0:  # check pos 1U1L
            options.append([y + 1, x - 1])
            switches.append([])
        if on_board(y + 1, x - 1) and on_board(y + 2, x - 2) and \
                (array[y + 1][x - 1] == turned or array[y + 1][x - 1] == king_turn) \
                and array[y + 2][x - 2] == 0:  # check if capture 1U1L
            options.append([y + 2, x - 2])
            switches.append([y + 1, x - 1])
        if on_board(y + 1, x + 1) and array[y + 1][x + 1] == 0:  # check pos 1U1R
            options.append([y + 1, x + 1])
            switches.append([])
        if on_board(y + 1, x + 1) and on_board(y + 2, x + 2) and \
                (array[y + 1][x + 1] == turned or array[y + 1][x + 1] == king_turn) \
                and array[y + 2][x + 2] == 0:  # check if capture 1U1R
            options.append([y + 2, x + 2])
            switches.append([y + 1, x + 1])
        if on_board(y - 1, x - 1) and array[y - 1][x - 1] == 0:  # check pos 1D1L
            options.append([y - 1, x - 1])
            switches.append([])
        if on_board(y - 1, x - 1) and on_board(y - 2, x - 2) and \
                (array[y - 1][x - 1] == turned or array[y - 1][x - 1] == king_turn) \
                and array[y - 2][x - 2] == 0:  # check if capture 1D1L
            options.append([y - 2, x - 2])
            switches.append([y - 1, x - 1])
        if on_board(y - 1, x + 1) and array[y - 1][x + 1] == 0:  # check pos 1D1R
            options.append([y - 1, x + 1])
            switches.append([])
        if on_board(y - 1, x + 1) and on_board(y - 2, x + 2) and \
                (array[y - 1][x + 1] == turned or array[y - 1][x + 1] == king_turn) \
                and array[y - 2][x + 2] == 0:  # check if capture 1D1R
            options.append([y - 2, x + 2])
            switches.append([y - 1, x + 1])

    return options, switches


def check_winner(array):
    """This function evaluates whether there are any moves to be made. If there arent then player loses. It also
    checks to see whether all of the pieces have been collected or whether game will end in tie."""
    global winner, game_over
    color, piece, king, word, turned, king_turn = get_move()  # gets data
    if len(get_all_moves(array, piece, king)[0]) < 1:
        winner = turned
        game_over = True
        display_winner()

    else:
        # if 12 collected pcs  are found for either player then game is over so set winner and update counters
        if p1_collected == 12:
            winner = 2
            game_over = True
        elif p2_collected == 12:
            winner = 1
            game_over = True
        # if 11 collected pcs are found for both players then game is over with tie
        elif p1_collected == 11 and p2_collected == 11:  #
            winner = 3  # set winner to tie
            game_over = True
        # otherwise no winner found
        else:
            winner = 0
            game_over = False
        if game_over and not checking:
            display_winner()  # show who won
    if checking:
        return game_over, winner


def move_piece(array, highlighted, box, switch, piece):
    """This function alters the model after a move has been selected."""
    global turn, p1_collected, p2_collected
    if piece == 1 and box[0] == 7:  # if person reaches other end then turn piece into king
        array[box[0]][box[1]] = 3
    elif piece == 2 and box[0] == 0:
        array[box[0]][box[1]] = 4
    else:  # otherwise simply move the piece that is currently highlighted
        array[box[0]][box[1]] = array[highlighted[0]][highlighted[1]]
    array[highlighted[0]][highlighted[1]] = 0  # change the highlighted piece to zero
    if len(switch) > 0:  # if there is flip to be made then
        if not checking:
            if array[switch[0]][switch[1]] == 1 or array[switch[0]][switch[1]] == 3:  # add to piece counters
                p1_collected += 1
            elif array[switch[0]][switch[1]] == 2 or array[switch[0]][switch[1]] == 4:
                p2_collected += 1
            array[switch[0]][switch[1]] = 0  # captures piece and sets to zero

    return array


def draw_background():
    """Function that draws the initial board with no pieces on it"""
    pg.draw.rect(screen, (200, 200, 200), (200, 0, 900, 800))  # draws gray background box

    def get_color(i, j):
        """Function that returns the color that the given background square should be painted.
        Used to draw the original board."""
        if i % 2 == 0 and j % 2 == 0:  # if the piece is on an even row and even column then it is dark brown
            return (90, 45, 0)
        elif i % 2 == 0 and j % 2 != 0:   # if the piece is on an even row and odd column then it is light brown
            return (200, 140, 80)
        elif i % 2 != 0 and j % 2 == 0:  # if the piece is on an odd row and even column then it is light brown
            return (200, 140, 80)
        elif i % 2 != 0 and j % 2 != 0:  # if the piece is on an odd row and odd column then it is dark brown
            return (90, 45, 0)

    for i in range(8):  # iterates through board and paints alternating light/dark brown squares
        for j in range(8):
            pg.draw.rect(screen, get_color(i, j), (250 + (75 * j), 50 + (75 * i), 75, 75))  # green box

    for i in range(0, 9):  # draws horizontal and vertical lines between squares
        pg.draw.rect(screen, (30, 30, 30), (250 + 75 * i, 50, 1, 600))  # vertical
        pg.draw.rect(screen, (30, 30, 30), (250, 50 + 75 * i, 600, 1))  # horizontal

    # sets print statements (two options) for each piece's total count (depending on formatting)
    p2 = font80.render(str(p2_collected), 1, (0, 0, 0))
    p20 = font65.render(str(p2_collected), 1, (0, 0, 0))
    p1 = font80.render(str(p1_collected), 1, (50, 70, 90))
    p10 = font65.render(str(p1_collected), 1, (50, 70, 90))

    if p1_collected < 10:  # if player 1 has less than 10 pieces, then use the bigger font
        screen.blit(p1, (211, 50))
    else:
        screen.blit(p10, (200, 50))  # otherwise use the smaller font

    if p2_collected < 10:   # if player 1 has less than 10 pieces, then use the bigger font
        screen.blit(p2, (861, 600))
    else:
        screen.blit(p20, (850, 600))  # otherwise use the smaller font

    cgs.draw_records(screen, 2, mode, logged_in, difficulty)  # draws left panel

    pg.display.update()


def update_board(array):
    """This function updates the board according to the model. It draws out the circles on the board according to their
    corresponding value in the model and also prints out on the bottom whose turn it is."""
    draw_background()  # draws the raw background

    for i in range(8):  # iterates through board model and draws it out according to parameters
        for j in range(8):
            if array[i][j] == 1:  # if number is 1 then draw blue
                pg.draw.circle(screen, (50, 70, 90), (288 + (j * 75), 613 - (i * 75)), 36)
            elif array[i][j] == 2:  # if number is 2 then draw black
                pg.draw.circle(screen, (0, 0, 0), (288 + (j * 75), 613 - (i * 75)), 36)
            elif array[i][j] == 3:  # if number is 3 then draw blue king
                pg.draw.circle(screen, (50, 70, 90), (288 + (j * 75), 613 - (i * 75)), 36)
                pg.draw.polygon(screen, (120, 145, 165), ((264 + (j * 75), 628 - (i * 75)),
                                                          (264 + (j * 75), 598 - (i * 75)),
                                                          (276 + (j * 75), 615 - (i * 75)),
                                                          (288 + (j * 75), 598 - (i * 75)),
                                                          (300 + (j * 75), 615 - (i * 75)),
                                                          (312 + (j * 75), 598 - (i * 75)),
                                                          (312 + (j * 75), 628 - (i * 75))))  # draws crown
            elif array[i][j] == 4:  # if number is 4 then draw black king
                pg.draw.circle(screen, (0, 0, 0), (288 + (j * 75), 613 - (i * 75)), 36)
                pg.draw.polygon(screen, (70, 70, 70), ((264 + (j * 75), 628 - (i * 75)),
                                                          (264 + (j * 75), 598 - (i * 75)),
                                                          (276 + (j * 75), 615 - (i * 75)),
                                                          (288 + (j * 75), 598 - (i * 75)),
                                                          (300 + (j * 75), 615 - (i * 75)),
                                                          (312 + (j * 75), 598 - (i * 75)),
                                                          (312 + (j * 75), 628 - (i * 75))))  # draws crown

    display_turn()

    pg.display.update()


def display_turn():
    """Function called to draw on the screen whose turn it is. It adjusts the labeling according to the mode"""
    color, piece, king, word, turned, king_turn = get_move()  # gets data

    pg.draw.circle(screen, color, (480, 715), 36)  # draws out whose turn it is (their color circle)
    if color == (50, 70, 90):  # prints name of person whose turn it is next to circle
        text = '(' + str(logged_in['username'].upper()) + ')'
        turn_display = font65.render("TURN", 1, (90, 45, 0))
    else:
        if mode == 0:  # if in human mode it is opponent
            text = '(OPPONENT)'
            turn_display = font65.render("TURN", 1, (90, 45, 0))
        else:
            text = '(AI)'  # if in AI then it is AI
            turn_display = font65.render("THINKING...", 1, (90, 45, 0))
    player = font50.render(str(text), 1, color)
    screen.blit(turn_display, (530, 695))
    screen.blit(player, (450, 755))


def make_fonts_global():
    """This font instantiates the font options as global variables to be used throughout the program."""
    global font65, font80, font50
    pg.font.init()
    font65 = pg.font.SysFont('Comic Sans MS', 65)
    font80 = pg.font.SysFont('Comic Sans MS', 80)
    font50 = pg.font.SysFont('Comic Sans MS', 50)


def get_collected(array):
    """This function counts the number of pieces each player has collected at the begining of the game (if game is
    resumed) instead of saving data to account."""
    p1_pieces, p2_pieces = 0, 0  # set pieces counters to zero prior to counting

    for i in range(8):  # draws board according to rules
        for j in range(8):
            if array[i][j] == 1 or array[i][j] == 3:
                p1_pieces += 1
            elif array[i][j] == 2 or array[i][j] == 4:
                p2_pieces += 1
    collected1 = 12 - p1_pieces
    collected2 = 12 - p2_pieces

    return collected1, collected2


def get_options(array, y, x, state):
    """Function that obtains and paints all of the potential options while also setting a global variable to a list
    of all the options"""
    global highlighted, options, switches

    color, piece, king, word, turned, king_turn = get_move()  # gets essential game data
    highlighted = [y, x]  # sets position to highlight

    pieces, options_all, switches_all = get_all_moves(array, piece, king)
    if highlighted in pieces:
        if piece == 1:  # sets colors for option circles
            color = (120, 145, 165)
        elif piece == 2:
            color = (70, 70, 70)
        options, switches = check_moves(array, turned, king_turn, piece, x, y, state)  # gets potential moves and flips

        count = 0
        for i in range(len(switches)):  # removes non-jump moves if a capture move exists
            if switches[i] == []:
                count += 1
        if len(switches) != count:
            diff = 0
            for i in range(len(switches)):
                if switches[i - diff] == []:
                    switches.pop(i - diff)
                    options.pop(i - diff)
                    diff += 1
        # print(options, ',', switches)

        if len(options) > 0:  # if there are options for given move then highlight it
            pg.draw.arc(screen, (255, 255, 0), [251 + (75 * x), 576 - (y * 75), 75, 75], 0, 2 * pi, 2)

        for option in options:  # draw out options
            pg.draw.circle(screen, color, (288 + (option[1] * 75), 613 - (option[0] * 75)), 20)

        pg.display.update()


def get_all_moves(array, piece, king):
    """FUnction that compiles all moves for a given player. Was added after realizing that only determining whether a
    move is valid if a user clicks on it does not allow for eliminating that move if a capture exists and must be
    taken"""
    pieces = []
    options_all = []
    switches_all = []
    if piece == 1:
        turned = 2
        king_turned = 4
    else:
        turned = 1
        king_turned = 3
    for i in range(len(array)):
        for j in range(len(array[i])):
            # iterates through all pieces and kings to get all raw moves
            if array[i][j] == piece:
                options, switches = check_moves(array, turned, king_turned, piece, j, i, 'reg')
                if len(options) > 0:
                    pieces.append([i, j])
                    options_all.append(options)
                    switches_all.append(switches)
            elif array[i][j] == king:
                options, switches = check_moves(array, turned, king_turned, piece, j, i, 'king')
                if len(options) > 0:
                    pieces.append([i, j])
                    options_all.append(options)
                    switches_all.append(switches)
    # then takes all of the moves and runs them through function to check if any need to be eliminated
    pieces, options_all, switches_all = eliminate_non_captures(options_all, switches_all, pieces)
    return pieces, options_all, switches_all


def eliminate_non_captures(options, switches, pieces):
    """This function accepts the determined options and their corresponding switches (flips) in parallel lists and
    removes any move that is not a flip if a flip exists among them. """
    indicies = []
    non_capture = 0  # counts moves within options that don't have flips
    total = 0
    for i in range(len(options)):
        for j in range(len(options[i])):
            total += 1
            if switches[i][j] == []:
                non_capture += 1

    if non_capture == total:  # if none of the moves have flips then return received data
        return pieces, options, switches
    else:  # otherwise...
        for i in range(len(switches)):
            empties = 0
            for j in range(len(switches[i])):
                if switches[i][j] == []:
                    empties += 1  # count how many moves correlate to empty switches (no capture)
            if empties == len(switches[i]):  # if all moves have no capture add index to list to edit later
                indicies.append(i)

        diff = 0
        for i in indicies:  # remove indices that don't have captures from all pieces lists
            pieces.pop(i - diff)
            options.pop(i - diff)
            switches.pop(i - diff)
            diff += 1

        for i in range(len(switches)):
            # finds and removes options within a move that has one capture and one non-capture
            diff = 0
            for j in range(len(switches[i])):
                if switches[i][j - diff] == []:
                    switches[i].pop(j - diff)
                    options[i].pop(j - diff)
                    diff += 1

        return pieces, options, switches


def display_winner():
    """This function is called to add to the user score keepers and also display the winner/tie at the end of the game.
    """
    global end
    display_turn()
    pg.draw.rect(screen, (200, 200, 200), (200, 700, 700, 800))  # draws gray background box
    if winner == 1 or winner == 2:
        turn_display = font65.render("WINS", 1, (90, 45, 0), (200, 200, 200))
        screen.blit(turn_display, (530, 695))
        if winner == 1:
            pg.draw.circle(screen, (50, 70, 90), (480, 715), 36)  # draws blue circle
            if not end:  # adds to counter
                if mode == 0:
                    logged_in['checkers_record'][0] += 1
                else:
                    logged_in['checkers_record_ai'][0] += 1
        elif winner == 2:
            pg.draw.circle(screen, (0, 0, 0), (480, 715), 36)  # draws black circle
            if not end:   # adds to counter
                if mode == 0:
                    logged_in['checkers_record'][1] += 1
                else:
                    logged_in['checkers_record_ai'][1] += 1
    elif winner == 3:  # if it is a tie
        turn_display = font65.render("ENDS IN A DRAW", 1, (90, 45, 0), (200, 200, 200))
        screen.blit(turn_display, (220, 695))
        if not end:
            if mode == 0:   # adds to counter
                logged_in['checkers_record'][2] += 1
            else:
                logged_in['checkers_record_ai'][2] += 1
    end = True  # sets variable to true from preventing continuous adding to the record keepers


def make_ai_move(array):
    """Function called when mode is set to AI and it is the AI's turn."""
    global turn, game_over, checking

    def score_board(board):
        """Function that scores the given board first according to the number of pieces on the board at any given moment
        . The number of AI pieces (regular representing 3 and king representing 5) minus the number of user pieces is
        the baseline. Next piece positioning is taken into account. Finally, the score is adjusted based to weigh
        captures heavier."""
        blue_score = 0
        black_score = 0
        p1, p2 = get_collected(board)
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                    blue_score += 3
                elif board[i][j] == 3:
                    blue_score += 5
                elif board[i][j] == 2:
                    black_score += 3
                elif board[i][j] == 4:
                    black_score += 5
        score = black_score - blue_score
        for i in range(8):
            for j in range(8):
                if board[i][j] > 0:
                    if board[i][j] == 2:
                        mult = 1
                        p2 += 1
                    elif board[i][j] == 4:
                        mult = 1
                        p2 += 1
                    elif board[i][j] == 1 or board[i][j] == 3:
                        mult = -1
                        p1 += 1
                    else:
                        mult = 0

                    if j == 0 or i == 7 or j == 7 or i == 0:
                        score += 4 * mult
                    elif j == 6 or i == 1 or j == 1 or i == 6:
                        score += 3 * mult
                    elif j == 5 or i == 2 or j == 2 or i == 5:
                        score += 2 * mult
                    elif j == 5 or i == 2 or j == 2 or i == 5:
                        score += 2 * mult
                    elif j == 3 or i == 4 or j == 4 or i == 3:
                        score += 1 * mult

        score = score + (p1 * 10)
        score = score - (p2 * 10)
        # print(score, board)
        return score

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        """Function used to determine which column the AI should place their piece in. For any given board, it creates
        a copy and then deepens until specified depth (2, 4, 6). After reaches max depth it starts to build its way back
        up (out of the hole) and extend back down in next column."""
        global checking

        checking = True
        is_terminal, temp_winner = check_winner(board)  # checks to see if board is terminal node/ winner determined
        if depth == 0 or is_terminal:  # if end of recursion or terminal node
            if is_terminal:
                if temp_winner == 2:  # if terminal node and winner is AI then return huge number
                    return 0, 0, 3000000000, 0
                elif temp_winner == 1:  # if terminal node and winner is human then return tiny number
                    return 0, 0, -3000000000, 0
                else:  # Game is over, no more valid moves
                    return 0, 0, 0, 0  # if terminal node and winner is 0 or 3 then return 0 (game is over or tie)
            if depth == 0:  # Depth is zero
                return 0, 0, score_board(board), 0  # if end of recursion return the score of the board

        if maximizingPlayer:  # Even number in recursion/tree (want to maximize AI score)
            pieces, options_all, switches_all = get_all_moves(board, 2, 4)
            # print(pieces, options_all, switches_all)
            value = -100
            if len(pieces) == 0:
                return 0, 0, -3000, 0
            else:
                rand_p = int(randint(0, len(pieces) - 1))  # randomly chooses move for default before minimax
                rand_m = int(randint(0, len(options_all[rand_p]) - 1))
                best_piece = pieces[rand_p]
                best_move = options_all[rand_p][rand_m]
                best_switch = switches_all[rand_p][rand_m]

            for i in range(len(pieces)):
                for j in range(len(options_all[i])):
                    if printing:
                        if depth == 4:
                            print('MAX--', pieces[i], options_all[i][j], value, best_piece, best_move, best_switch)
                        elif depth == 2:
                            print('-----------MAX--', pieces[i], options_all[i][j], value, best_piece, best_move, best_switch)
                    b_copy1 = [x[:] for x in board]  # make a copy of the board
                    b_copy1 = move_piece(b_copy1, pieces[i], options_all[i][j], switches_all[i][j], 2)
                    new_score = minimax(b_copy1, depth - 1, alpha, beta, False)[2]  # alternate to min/next level in tree
                    if printing:
                        if depth == 4:
                            print('MAX++',  value, new_score)
                        elif depth == 2:
                            print('-----------MAX++', value, new_score)
                    if new_score > value:  # if the minimax returns a score higher than default reset it to one found
                        value = new_score
                        best_piece = pieces[i]
                        best_move = options_all[i][j]
                        best_switch = switches_all[i][j]
                    alpha = max(alpha, value)  # set alpha variable to alpha or value (whichever is higher)
                    if alpha >= beta:  # ALPHA BETA PRUNING
                        break  # if winning move found or column found with score greater then beta, break out of loop
            return best_piece, best_move, value, best_switch

        else:  # Odd number in recursion/tree (want to minimize Human score)
            pieces, options_all, switches_all = get_all_moves(board, 1, 3)
            # print(pieces, options_all, switches_all)
            value = 100
            if len(pieces) == 0:
                return 0, 0, 3000, 0
            else:
                rand_p = int(randint(0, len(pieces) - 1))  # randomly chooses move for default before minimax
                rand_m = int(randint(0, len(options_all[rand_p]) - 1))
                best_piece = pieces[rand_p]
                best_move = options_all[rand_p][rand_m]
                best_switch = switches_all[rand_p][rand_m]

            for i in range(len(pieces)):
                for j in range(len(options_all[i])):
                    if printing:
                        if depth == 3:
                            print('------MIN', pieces[i], options_all[i][j], value, best_piece, best_move, best_switch)
                        elif depth == 1:
                            print('--------------------MIN', pieces[i], options_all[i][j], value, best_piece, best_move,
                                  best_switch)
                    b_copy2 = [x[:] for x in board]  # make a copy of the board
                    b_copy2 = move_piece(b_copy2, pieces[i], options_all[i][j], switches_all[i][j], 1)
                    new_score = minimax(b_copy2, depth - 1, alpha, beta, True)[2]  # alternate to max/next level in tree
                    if printing:
                        if depth == 3:
                            print('++++++MIN++', value, new_score)
                        elif depth == 1:
                            print('--------------------MIN++', value, new_score)
                    if new_score < value:  # if the minimax returns a score less than default reset it to one found
                        value = new_score
                        best_piece = pieces[i]
                        best_move = options_all[i][j]
                        best_switch = switches_all[i][j]
                    beta = min(beta, value)  # set beta variable to beta or value (whichever is lower)
                    if alpha >= beta:
                        break  # if winning move found or column found with score greater then beta, break out of loop
            return best_piece, best_move, value, best_switch

    current_board = array.copy()  # copy the board for the minimax function
    selection, move, value, switch = minimax(current_board, difficulty, -50, 50, True)  # call the minimax to determine best column
    if selection != 0:
        checking = False
        pg.time.wait(2000)
        array = move_piece(array, selection, move, switch, 2)  # make the move that minimax determined

    return array


def playing_game(board):
    """This function is called to commence the game and handles all interactions with the screen. It redirects events
    to their relevant functions. This is the brain of the game that re-formats and redirects data to be used in a
    meaningful manner."""
    global turn, options, p1_collected, p2_collected, logged_in, difficulty, checking, printing, winner, game_over, end
    game_over, checking, printing, end = False, False, False, False
    turn = logged_in['current_checkers'][1]
    p1_collected, p2_collected = get_collected(board)

    update_board(board)

    while True:
        for event in pg.event.get():
            color, piece, king, word, turned, king_turn = get_move()  # gets necessary data for given game state
            check_winner(board)  # checks if winner has been established with new board
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[0] < 190:  # event on the left panel calls function in cgs
                    cgs.left_panel_event(2, screen, event, logged_in, mode, difficulty, board, turn, game_over)
                    difficulty = logged_in['current_checkers'][3]

            if game_over:
                cgs.draw_records(screen, 2, mode, logged_in, difficulty)  # updates left panel scores
            else:
                if mode == 1 and turn % 2 == 0:  # if AI turn
                    board = make_ai_move(board)  # commence AI process
                    check_winner(board)  # checks to see if winner can be established on board
                    turn += 1
                    update_board(board)

                if event.type == pg.MOUSEBUTTONDOWN:
                    if 250 < event.pos[0] < 850 and 50 < event.pos[1] < 650:
                        box = get_coordinates(event.pos[0], event.pos[1])  # gets position of event
                        if board[box[0]][box[1]] == piece or board[box[0]][box[1]] == king:  # if belongs to current player
                            update_board(board)  # then update the board and clears other turn highlighting
                            if board[box[0]][box[1]] == piece:
                                get_options(board, box[0], box[1], 'reg')  # gets potential moves for regular piece
                            elif board[box[0]][box[1]] == king:
                                get_options(board, box[0], box[1], 'king')   # gets potential moves for king piece
                    try:
                        if box in options:  # if clicked position is one of potential moves then alter board according to click
                            index = options.index(box)
                            switch = switches[index]
                            board = move_piece(board, highlighted, box, switch, piece)  # makes move
                            check_winner(board)  # checks if winner has been established with new board
                            turn += 1
                            update_board(board)
                            options.clear()  # clear current list of potential moves
                    except NameError:  # if variable options is not defined yet then break
                        break

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if not game_over:  # saves data with function in cgs b4 exiting
                    logged_in = cgs.save_data(board, turn, 2, logged_in, difficulty, mode)
                cgs.dump(logged_in)  # dumps the newly updated user account
                cgs.main()  # calls cgs.main function to return to game option window (homepage when logged in)

            pg.display.update()


def main(pg):
    """This is the main function that is called to start/restart checkers. It designates essential global variables
    and opens up the game data from files. It then commences the game by calling the playing_game function"""
    global screen, logged_in, mode, difficulty

    pickle_in_logged_in = open("logged_in", "rb")  # pickle in the logged_in data
    logged_in = pickle.load(pickle_in_logged_in)
    screen = pg
    make_fonts_global()  # makes fonts global variables

    mode, difficulty = logged_in['current_checkers'][2], logged_in['current_checkers'][3]
    if logged_in['current_checkers'][0] == []:  # if checkers board is empty then call build_board() and return model
        board = build_board()
    else:  # otherwise use existing board
        build_board()
        board = logged_in['current_checkers'][0]

    playing_game(board)  # commence game play


if __name__ == '__main__':
    main()