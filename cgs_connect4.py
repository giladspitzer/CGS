import pygame as pg
import cgs
import pickle

#  Board is inversely represented throughout the code [3, 2] = [y, x]


def draw_board_raw():
    """Function that draws the basic the basic starting board and calls function from cgs file to draw left
    side panel"""
    pg.draw.rect(screen, (0, 100, 255), (200, 95, 900, 705))  # Big Blue Box
    pg.draw.rect(screen, (250, 250, 250), (200, 0, 900, 100))  # Top White Box
    pg.draw.rect(screen, (0, 0, 0), (200, 710, 900, 5))  # Bottom black bar
    for i in range(6):  # draw white circles in 7x6 board
        for j in range(7):
            pg.draw.circle(screen, (250, 250, 250), (250 + (j * 100), 650 - (i * 100)), 45)

    cgs.draw_records(screen, 0, mode, logged_in, difficulty)  # draws left panel of game suite from cgs

    pg.display.update()  # update the window with changes


def build_board():
    """Function that builds the board/model that will be altered throughout the game"""

    draw_board_raw()  # calls function to draw background graphics for initial board

    board = []  # builds the board/model that will be modified throughout the game
    for i in range(6):  # creates a 7x6 grid that is inversely represented throughout the code
        board.append([])
        for j in range(7):
            board[i].append(0)

    return board


def update_board(board):
    """Function that updates the window based on the changes in the model."""

    p1_pieces, p2_pieces = 0, 0  # set pieces counters to zero prior to counting

    for i in range(6):  # draws board according to rules
        for j in range(7):
            color = (250, 250, 250)  # default is white
            if board[i][j] == 1:
                color = (255, 0, 0)  # if number is 1 draw in for red
                p1_pieces += 1
            elif board[i][j] == 2:
                color = (255, 240, 0)  # if number is 2 draw in for yellow
                p2_pieces += 1

            pg.draw.circle(screen, color, (250 + (j * 100), 650 - (i * 100)), 45)  # actually draw the circle

    if winner == 1:  # sets color of text 'Pieces Used' based on if there is a winner or not
        pieces_color = (250, 0, 0)
    elif winner == 2:
        pieces_color = (255, 240, 0)
    else:
        pieces_color = (250, 250, 250)

    pg.draw.rect(screen, (0, 100, 255), (200, 750, 900, 100))
    pieces_used = font50.render("PIECES USED:", 1, pieces_color)
    screen.blit(pieces_used, (430, 717))

    """Color depends on whose turn it is"""
    color, piece = get_move()  # gets whose turn it is
    # sets colors accordingly
    if piece == 1:
        player1_color = color
        player2_color = (0, 0, 0)
    elif piece == 2:
        player1_color = (0, 0, 0)
        player2_color = color

    font45 = pg.font.SysFont('Comic Sans MS', 45)
    player1_counter = font45.render(str(logged_in['username']) + '~ ' + str(p1_pieces), 1, player1_color)
    screen.blit(player1_counter, (270, 760))  # prints logged in user and their pieces

    if mode == 0:  # sets opponent name based on mode
        text = 'OPPONENT ~'
    else:
        text = 'AI ~'
    player2_counter = font45.render(text + str(p2_pieces), 1, player2_color)
    screen.blit(player2_counter, (600, 760))  # prints opponent and their pieces

    if game_over:  # if the game is over then update the records on left panel via cgs
        cgs.draw_records(screen, 0, mode, logged_in, difficulty)

    pg.display.update()  # update the window with changes


def get_move():
    """Function that determines whose turn it is and what color to use for various drawings."""
    if turn % 2 == 0:  # if the global turn variable is odd then its player 2's turn
        color = (255, 250, 0)
        piece = 2
    else:  # or else it is player 1's turn
        color = (250, 0, 0)
        piece = 1
    return color, piece


def clear_top():
    """Function that repaints the top bar to white with dividing lines after each mouse movement."""
    pg.draw.rect(screen, (250, 250, 250), (200, 0, 900, 100))
    for i in range(7):
        pg.draw.rect(screen, (50, 50, 50), (200 + (i * 100), 0, 1, 100))

    pg.display.update()  # update the window with changes


def drop_piece(board_in, piece, column):
    """Function that modifies the model based on the user's column selection. It returns True (column is maximized)
    if the column is full."""
    column_options = []  # adds all of the numbers in that column to list
    for i in range(0, 6):
        column_options.append(board_in[i][column])
    if 0 not in column_options:  # if there is not a zero in the list then it is maximized so return True
        return True
    index = column_options.index(0)  # otherwise place the piece in the column in the first available row
    board_in[index][column] = piece


def display_turn():
    """Function that paints whose turn it is in the top bar."""
    color, piece = get_move()  # gets whose turn it is and what color to use
    if piece == 1:  # if it is
        text = logged_in['username'].upper() + "'S TURN"
        x = 300
    else:
        if mode == 0:  # sets opponent name based on mode
            text = "OPPONENT'S TURN"
        else:
            text = "AI'S TURN"
        x = 230
    turn_display = font100.render(str(text), 1, color)
    pg.draw.rect(screen, (0, 100, 255), (200, 0, 900, 100))  # draws blue rectangle background
    screen.blit(turn_display, (x, 20))  # prints message


def check_winner(board):
    """Function that checks if there is a winner on the current board"""
    def show_winner(winners):
        for winner in winners:
            pg.draw.circle(screen, (0, 0, 0), (250 + (winner[1] * 100), 650 - (winner[0] * 100)), 5)

    def tie_game():
        """Function that prints tie game status, updates counters"""
        global winner, logged_in
        if not checking:
            if mode == 0:
                logged_in['connect4_record'][2] += 1  # adds 1 to the user's tie record
            else:
                logged_in['connect4_record_ai'][2] += 1  # adds 1 to the user's tie record for AI

            turn_display = font100.render("TIE GAME", 1, (255, 240, 0))
            pg.draw.rect(screen, (0, 100, 255), (200, 0, 900, 100))
            screen.blit(turn_display, (440, 15))  # prints message
        winner = 0  # sets global variable winner = 0
        return True  # winner determined

    def player1_wins(winners):
        """Function that prints winner status, updates counters, and sets variables if user WINS"""
        global winner, logged_in
        if not checking:
            if mode == 0:
                logged_in['connect4_record'][0] += 1   # adds 1 to the user's winning record
            else:
                logged_in['connect4_record_ai'][0] += 1  # adds 1 to the user's winning record for AI
            turn_display = font100.render(str(logged_in['username'].upper()) + ' WINS!', 1, (255, 0, 0))
            pg.draw.rect(screen, (0, 100, 255), (200, 0, 900, 100))
            screen.blit(turn_display, (265, 15))  # prints message
        show_winner(winners)
        winner = 1  # sets global variable winner = 1
        return True  # winner determined

    def player2_wins(winners):
        """Function that prints winner status, updates counters, and sets variables if user LOSES"""
        global winner, logged_in
        if not checking:
            if mode == 0:
                logged_in['connect4_record'][1] += 1   # adds 1 to the user's losing record
            else:
                logged_in['connect4_record_ai'][1] += 1  # adds 1 to the user's losing record for AI
            if mode == 0:  # sets opponent name based on mode
                text = 'OPPONENT'
            else:
                text = 'AI'
            turn_display = font100.render(text + " WINS!", 1, (255, 240, 0))
            pg.draw.rect(screen, (0, 100, 255), (200, 0, 900, 100))
            screen.blit(turn_display, (240, 15))  # prints message
        show_winner(winners)
        winner = 2  # sets global variable winner = 2
        return True  # winner determined

    number1 = 0
    number2 = 0
    for col in board:  # counts number of each player on board to check for tie game
        number1 += col.count(1)
        number2 += col.count(2)

    if number1 == 21 and number2 == 21:
        return tie_game()  # TIE GAME

    else:
        for i in range(3):  # check vertical
            for j in range(7):
                if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == 1:
                    return player1_wins([[i, j], [i+1, j], [i+2, j], [i+3, j]])
                if board[i][j] == board[i+1][j] == board[i+2][j] == board[i+3][j] == 2:
                    return player2_wins([[i, j], [i+1, j], [i+2, j], [i+3, j]])

        for i in range(6):  # check horizontal
            for j in range(4):
                if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == 1:
                    return player1_wins([[i, j], [i, j+1], [i, j+2], [i, j+3]])
                if board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == 2:
                    return player2_wins([[i, j], [i, j+1], [i, j+2], [i, j+3]])

        for i in range(3):  # check diagonal direct
            for j in range(4):
                if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == 1:
                    return player1_wins([[i, j], [i+1, j+1], [i+2, j+2], [i+3, j+3]])
                if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == 2:
                    return player2_wins([[i, j], [i+1, j+1], [i+2, j+2], [i+3, j+3]])

        for i in range(3):  # check diagonal indirect
            for j in range(7):
                if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == 1:
                    return player1_wins([[i, j], [i+1, j-1], [i+2, j-2], [i+3, j-3]])
                if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == 2:
                    return player2_wins([[i, j], [i+1, j-1], [i+2, j-2], [i+3, j-3]])
        return False  # no winner determined


def make_ai_move(array):
    """Function called when mode is set to AI and it is the AI's turn."""
    global turn, game_over

    def evaluate_window(window, piece):
        """Function used to evaluate and score a window of 4 pieces distinct pieces."""
        score = 0
        opp_piece = 1
        if piece == 1:
            opp_piece = 2

        if window.count(piece) == 4:  # if there are 4 of the AI piece (AI wins) then add 800 to overall score
            score += 800
        elif window.count(piece) == 3 and window.count(0) == 1:  # if there are 3 AI pieces and 1 unfilled add 400
            score += 400
        elif window.count(piece) == 2 and window.count(0) == 2:  # if there are 2 AI pieces and 2 open then add 2
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:  # if there are 3 opponent pieces and 1 open -350
            score -= 350
        elif window.count(opp_piece) == 4:  # if there are 4 opponent pieces (opponent wins) subtract 700
            score -= 700

        return score  # return the score

    def score_position(board, piece):
        """Checks all four winning directions in order to score the board."""
        score = 0

        # Score center column
        center_column = board[3]
        center_count = center_column.count(piece)
        score += center_count * 3  # add number of pieces and multiply by 3

        # Score Horizontal by sending different combinations of 4 horizontally connected pieces to other function
        for c in range(4):
            for r in range(6):
                window = [board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]]
                score += evaluate_window(window, piece)

        # Score Vertical by sending different combinations of 4 vertically connected pieces to other function
        for c in range(7):
            for r in range(3):
                window = [board[r][c], board[r + 1][c], board[r + 2][c], board[r + 3][c]]
                score += evaluate_window(window, piece)

        # Score POSITIVE Diag by sending different combinations of 4 diag connected pieces to other function
        for r in range(3):
            for c in range(4):
                window = [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]]
                score += evaluate_window(window, piece)

        # Score NEGATIVE Diag by sending different combinations of 4 diag connected pieces to other function
        for r in range(3):
            for c in range(4):
                window = [board[r][c + 3], board[r + 1][c + 2], board[r + 2][c + 1], board[r + 3][c]]
                score += evaluate_window(window, piece)

        return score

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        """Function used to determine which column the AI should place their piece in. For any given board, it creates
        a copy and then deepens until specified depth (2, 4, 6). After reaches max depth it starts to build its way back
        up (out of the hole) and extend back down in next column."""
        global checking, winner

        winner = 0
        checking = True

        column_options = []  # adds all of open column options to list
        for i in range(7):
            if board[5][i] == 0:
                column_options.append(i)

        is_terminal = check_winner(board)  # checks to see if board is terminal node/ winner determined
        if depth == 0 or is_terminal:  # if end of recursion or terminal node
            if is_terminal:
                if check_winner(board) and winner == 2:  # if terminal node and winner is AI then return huge number
                    return None, 3000000000
                elif check_winner(board) and winner == 1: # if terminal node and winner is human then return tiny number
                    return None, -3000000000
                else:  # Game is over, no more valid moves
                    return None, 0  # if terminal node and winner is 0 then return 0 (game is over)
            else:  # Depth is zero
                return None, score_position(board, get_move()[1])  # if end of recursion return the score of the board
        if maximizingPlayer:  # Even number in recursion/tree (want to maximize AI score)
            value = -2000
            best_column = 0  # default column is 0
            for column in column_options:  # iterate over all open columns
                b_copy1 = [x[:] for x in board]  # make a copy of the board
                drop_piece(b_copy1, 2, column)  # drop a piece in the copied board in current column in iteration
                new_score = minimax(b_copy1, depth - 1, alpha, beta, False)[1]  # alternate to min/next level in tree
                if new_score > value:  # if the minimax returns a score higher than default reset it to one found
                    value = new_score
                    best_column = column  # set best_column to current iteration too
                alpha = max(alpha, value)  # set alpha variable to alpha or value (whichever is higher)
                if alpha >= beta: # ALPHA BETA PRUNING
                    break  # if winning move found or column found with score greater then beta, break out of loop
            return best_column, value

        else:   # Odd number in recursion/tree (want to minimize Human score)
            value = 2000
            best_column = 0  # default column is 0
            for column in column_options:  # iterate over all open columns
                b_copy2 = [x[:] for x in board]  # make a copy of the board
                drop_piece(b_copy2, 1, column)  # drop a piece in the copied board in current column in iteration
                new_score = minimax(b_copy2, depth - 1, alpha, beta, True)[1]  # alternate to max/next level in tree
                if new_score < value:  # if the minimax returns a score less than default reset it to one found
                    value = new_score
                    best_column = column  # set best_column to current iteration too
                beta = min(beta, value)  # set beta variable to beta or value (whichever is lower)
                if alpha >= beta:
                    break  # if winning move found or column found with score greater then beta, break out of loop
            return best_column, value

    current_board = array.copy()  # copy the board for the minimax function
    col, value = minimax(current_board, difficulty, -1000, 1000, True)  # call the minimax to determine best column
    pg.time.delay(300)  # delay so user can see where AI goes
    drop_piece(array, 2, col)  # make the move that minimax determined
    turn += 1  # add 1 to turn counter


def make_fonts_global():
    """Function called in the begining of the game to globalize the font surfaces that will be used"""
    global font50, font100
    pg.font.init()
    font50 = pg.font.SysFont('Comic Sans MS', 50)
    font100 = pg.font.SysFont('Comic Sans MS', 100)


def playing_game(board):
    """Function that deals with all interactions with the screen and redirects events to various functions to either
    update the game model and or screen."""
    global winner, turn, logged_in, mode, game_over, checking, difficulty

    make_fonts_global()
    winner = 0
    checking = False  # checking variable set to False when AI is not checking
    game_over, turn = False, logged_in['current_connect4'][1]      # designate essential game variables

    update_board(board)

    while True:  # opens infinite loop
        if mode == 1 and turn % 2 == 0 and not game_over:  # if AI turn
            make_ai_move(board)  # commence AI process
            checking = False
            game_over = check_winner(board)  # checks to see if winner can be established on board
            update_board(board)

        for event in pg.event.get():  # gathers every interaction with the screen

            color, piece = get_move()  # calls function to gather info on whose turn it is and what color to use

            if game_over:
                checking = True
                update_board(board)  # update the board
                game_over = check_winner(board)  # checks to see if winner can be established on board
                cgs.dump(logged_in)  # dump newly updated records after win or loss

            if event.type == pg.MOUSEMOTION and not game_over:  # if the interaction is a move of the mouse:
                clear_top()  # function that clears the top bar
                # draws narrow box on left side to compensate for circle
                pg.draw.rect(screen, (0, 0, 0), (185, 0, 15, 100))
                posx = event.pos[0]  # sets variable to number representing x coordinate of mouse
                if posx > 230:  # if movement is in top bar then draw the person's circle
                    pg.draw.circle(screen, color, (posx, 50), 45)

            if event.type == pg.MOUSEBUTTONDOWN:  # if the interaction is a click of the mouse:
                if event.pos[0] < 190:
                    cgs.left_panel_event(0, screen, event, logged_in, mode, difficulty, board, turn, game_over)
                    difficulty = logged_in['current_connect4'][3]

                else:  # user is placing a piece/ making a move
                    if not game_over:
                        posx = event.pos[0] - 200  # adjustment making up for changed screen size because of left panel
                        column = posx // 100  # attains the column the user is clicking into
                        if posx > 0:
                            maximized = drop_piece(board, piece, column)  # drop the user's piece in his desired column
                            if maximized:  # if the column is full then break
                                break
                            turn += 1  # add one to the global turn counter after his turn
                            if mode == 0:
                                display_turn()  # paints whose turn it is on top bar

                        game_over = check_winner(board)  # checks to see if winner can be established on board

                        if mode == 1 and turn % 2 == 0 and not game_over:
                            make_ai_move(board)  # commence AI process
                            checking = False
                            game_over = check_winner(board)  # checks to see if winner can be established on board

                        update_board(board)

                pg.display.update()  # update the window with changes

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # if the user clicks esc
                if not game_over:  # saves data with function in cgs b4 exiting
                    logged_in = cgs.save_data(board, turn, 0, logged_in, difficulty, mode)
                cgs.dump(logged_in)  # dumps the newly updated user account
                cgs.main()  # calls cgs.main function to return to game option window (homepage when logged in)

            pg.display.update()  # update the window with changes


def main(pg):
    """Function called to get everything ready for game. Sets variables from data and builds board before calling
    playing_game function to commence game play."""
    global screen, logged_in, mode, difficulty
    pickle_in_logged_in = open("logged_in", "rb")  # pickle in the data from file regarding who is logged in (or None)
    logged_in = pickle.load(pickle_in_logged_in)
    screen = pg  # passed screen from cgs
    mode = logged_in['current_connect4'][2]
    difficulty = logged_in['current_connect4'][3]
    # screen = pg.display.set_mode((700, 800))  # was used as screen prior to cgs implementation
    if logged_in['current_connect4'][0] == []:  # if current user has no ongoing game then create a new board
        board = build_board()
    else:
        draw_board_raw()  # because we are importing our own board, we need to specifically draw the board
        board = logged_in['current_connect4'][0]  # import the board to resume from the (logged_in) user data

    playing_game(board)  # commence the game by calling the playing_game function


if __name__ == '__main__':
    main()