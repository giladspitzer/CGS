import pygame as pg, cgs, pickle


def build_board():
    """This function builds the simple model for Othello (8x8 board) and then modifies the middle pieces."""
    board = []  # builds the board that will be modified throughout the game
    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(0)

    # edits center four pieces
    board[3][3] = 2
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2

    build_board_raw()  # draws beginning of game

    return board


def build_board_raw():
    """This function draws the basic board at the beginning of the game and refers to cgs to draw left pannel."""
    pg.draw.rect(screen, (150, 150, 150), (200, 0, 900, 800))  # white background
    pg.draw.rect(screen, (0, 65, 0), (250, 50, 600, 600))  # green board/box
    for i in range(0, 9):
        pg.draw.rect(screen, (30, 30, 30), (250 + 75 * i, 50, 1, 600))  # vertical lines
        pg.draw.rect(screen, (30, 30, 30), (250, 50 + 75 * i, 600, 1))  # horizontal lines

    # labeling pieces counter and text
    turn_display = font50.render("PIECES ON BOARD:", 1, (75, 75, 75))
    screen.blit(turn_display, (380, 660))

    user = font65.render(str(logged_in['username']), 1, (250, 250, 250))
    if mode == 0:
        text = 'Opponent'
    else:
        text = 'AI'
    opponent = font65.render(text, 1, (0, 0, 0))
    screen.blit(user, (270, 720))
    screen.blit(opponent, (655, 720))


    cgs.draw_records(screen, 1, mode, logged_in, difficulty)  # draws left panel


def get_move():
    """This function references the global variable 'turn' to determine data about current turn and their data."""
    if turn % 2 == 0:  # if the global turn variable is odd then its player 2's turn
        color = (0, 0, 0)
        piece = 2
        word = 'BLACK'
    else:  # or else its player1's turn
        color = (255, 250, 250)
        piece = 1
        word = 'WHITE'
    return color, piece, word


def update_board(board):
    """This function acts as the viewing modeler by accepting the board and painting its changes throughout
    the game. It also updates the piece counters at the the bottom of the screen"""
    global neighbors, sandwiches, turn, previous_state

    for i in range(8):  # iterates through list and draws out each number/circle
        for j in range(8):
            color = (0, 65, 0)  # determines color to draw based off of number. Default is background color.
            if board[i][j] == 1:
                color = (255, 255, 255)
            elif board[i][j] == 2:
                color = (0, 0, 0)
            pg.draw.circle(screen, color, (288 + (j * 75), 613 - (i * 75)), 36)

    color, piece, word = get_move()
    if piece == 1:
        opp = 2
    else:
        opp = 1

    neighbors, sandwiches = get_valid_moves(board, piece, opp)  # gets neighbors/potential moves

    if len(neighbors) == 0:  # if the user has no options, then his turn is skipped
        previous_state += 1
        print(turn%2, ' Plskip turn', previous_state)
        pg.time.delay(3000)
        turn += 1
    else:
        previous_state = 0

    for neighbor in neighbors:  # draws out each option and the number of pieces that it adds to player's total
        i, j = neighbor[0], neighbor[1]
        pg.draw.circle(screen, (75, 75, 75), (288 + (j * 75), 613 - (i * 75)), 12)
        repeats = get_total_sandwiches(neighbor)  # attains number of pieces that are gained
        color = get_move()[0]
        options = font27.render(str(repeats), 1, color)
        screen.blit(options, (283 + (j * 75), 605 - (i * 75)))  # paints message

    check_winner(board)

    pg.display.update()  # update the window with changes


def get_valid_moves(board, piece, opp):

    def check_line(dx, dy, x, y, sandwiches):
        """Function that recursively checks the depth of a neighbors path. After a neighbor with another adjacent
        piece is found then this function is called to see how long the line of pieces runs for. Accepts the previous
        delta values (the same) to aid in finding directionality and also default x and y values which have had two
        delta values added to them. Continuing EX (from def is_line) - accepts [0, 1, 2, 5] because it has been
        determined that [4, 2] is an opposite player's piece so now need to check [5, 2]."""
        if x > 7 or x < 0:   # checks to make sure next piece in line is on board (x)
            return [False, 0]
        if y > 7 or y < 0:  # checks to make sure next piece in line is on board (y)
            return [False, 0]
        if board[y][x] == 0:  # if a 0 is found in line then sandwich is over so return True
            return [True, [y, x], sandwiches]
        if board[y][x] == piece:  # ***if player's piece is found in line then sandwich is ruined so return False ***
            return [False, 0]
        if x + dx < 0 or x + dx > 7:  # return False if next piece in line is off the board (x)
            return [False, 0]
        if y + dy < 0 or y + dy > 7:  # return False if next piece in line is off the board (y)
            return [False, 0]
        sandwiches.append([y, x])  # before deepening recursion, add spot to sandwiches list
        return check_line(dx, dy, dx + x, dy + y, sandwiches)  # recursively call function until 0 is found and True is returned

    def is_line(x, y, dx, dy):
        """Function that checks to make sure neighbor and the piece after it (in same direction) are both on board. If
        piece that is not the opp is found then also return False. Weeds out bad neighbors by accepting the base
        x and y values as well as the delta x and y values, which indicate the intended direction, and checking to
         ensure that a direct line of the opposite player's pieces exist adjacent to the current player's piece.
          EX- accepts (2, 3, 0, 1). This means we are checking the piece [3, 2] (inversely modeled grid)
          by moving up/veritically by 1 incrementally."""
        if x + dx > 7 or x + dx < 0:  # checks to make sure next piece in line is on board (x)
            return [False, 0]
        if y + dy > 7 or y + dy < 0:  # checks to make sure next piece in line is on board (y)
            return [False, 0]
        if board[y + dy][x + dx] != opp:  # checks to make sure adjacent piece is equal to opposite player's piece
            return [False, 0]
        sandwiches = [[y + dy, x + dx]]  # before deepening recursion, add spot to sandwiches list
        # Neighbor with direct line of pieces found so now have to find depth of line/how far it continues
        return check_line(dx, dy, x + dx + dx, y + dy + dy, sandwiches)

    def is_on_board(move):
        """Function that accepts a move and ensures that it is on the board."""
        if 0 < move[0] < 7 and 0 < move[1] < 7:
            return True
        return False

    def get_neighbors(board, x, y):
        """perhaps list with [[i+1, j], [i - 1, j]], etc. of all checking. Iterate through all of them (first check to
         see if it is on the board) then compare it to the opp"""

        neighbors = []  # store temporary master list of neighbors and sandwiches only for this piece
        sandwiches_all = []

        # movements includes eight different directions and their simple numbers as well
        movements = [[y + 1, x, 1, 0], [y - 1, x, -1, 0], [y, x + 1, 0, 1], [y, x - 1, 0, -1], [y + 1, x + 1, 1, 1],
                     [y + 1, x - 1, 1, -1], [y - 1, x + 1, -1, 1], [y - 1, x - 1, -1, -1]]
        for movement in movements:  # for each direction if it is the opposite piece then start checking for sandwiches
            on_board = is_on_board(movement)
            if on_board and board[movement[0]][movement[1]] == opp:
                response = is_line(x, y, movement[3], movement[2])  # checks to see if this 'lead' actually is sandwich
                state = response[0]
                pair = response[1]
                if state:
                    sandwiches = response[2]
                    neighbors.append(pair)
                    sandwiches_all.append(sandwiches)

        return neighbors, sandwiches_all

    # sets master lists for neighbors and their parallel sandwiches
    neighbors_master = []
    sandwiches_master = []
    # sets who the opponent is based off whose turn it currently is

    for y in range(8):
        for x in range(8):
            if board[y][x] == piece:
                neighbors, sandwiches = get_neighbors(board, x, y)  # for each piece, get its neighbors and sandwiches
                for i in range(len(neighbors)):  # add everything found to master lists
                    neighbors_master.append(neighbors[i])
                    sandwiches_master.append(sandwiches[i])

    return neighbors_master, sandwiches_master


def check_winner(board):
    """Function that checks if the board has a winner by seeing if there are any available spots or if there are no
    neighbors and the previous turn there were no neighbors (stalemate)."""
    global winner, game_over, turn

    p1_pieces, p2_pieces = count_pieces(board)[0], count_pieces(board)[1]   # gets number of pieces for each player on board
    maxed = 0
    for column in board:
        if column.count(0) == 0:
            maxed += 1  # tallies available spots on board

    if maxed == 8 or previous_state > 1:  # if no available spots and repeat of no neighbor
        if p1_pieces > p2_pieces:  # if p1 has more pieces then he won
            winner = 1
            if not checking:  # if not checking (AI scanning) then add to counters and declare game is over
                if mode == 0:
                    logged_in['othello_record'][0] += 1
                elif mode == 1:
                    logged_in['othello_record_ai'][0] += 1
                game_over = True
        elif p1_pieces == p2_pieces:  # if p2 equal pieces then tie game (winner = 0 but game is over)
            winner = 0
            if not checking:  # if not checking (AI scanning) then add to counters and declare game is over
                if mode == 0:
                    logged_in['othello_record'][2] += 1
                elif mode == 1:
                    logged_in['othello_record_ai'][2] += 1
                game_over = True
        elif p2_pieces > p1_pieces:
            winner = 2  # if p2 has more pieces then he won
            if not checking:  # if not checking (AI scanning) then add to counters and declare game is over
                if mode == 0:
                    logged_in['othello_record'][1] += 1
                elif mode == 1:
                    logged_in['othello_record_ai'][1] += 1
                game_over = True

        if not checking:  # if not checking (AI scanning) then update score board
            update_score_board(p1_pieces, p2_pieces)

        return True  # return true that a winner was found

    else:
        winner = 0  # if no special state determined then winner remains = 0

        if not checking or previous_state > 1:  # if not checking (AI scanning) then update score board
            update_score_board(p1_pieces, p2_pieces)

        return False  # return false that no winner was found


def count_pieces(board):
    """Function used to count number of pieces each player has on the board at any given time."""
    p1_pieces = 0
    p2_pieces = 0
    for i in range(8):  # iterates through board and adds to counters accordingly
        for j in range(8):
            if board[i][j] == 1:
                p1_pieces += 1
            elif board[i][j] == 2:
                p2_pieces += 1

    return [p1_pieces, p2_pieces]


def update_score_board(p1_pieces, p2_pieces):
    """This function updates the scoreboard -- how many pieces each player has on the board -- and also whose
    turn it is."""
    global font70
    color, piece, word = get_move()
    pg.draw.circle(screen, (250, 250, 250), (490, 740), 36)  # draws p1 circle
    pg.draw.circle(screen, (0, 0, 0), (590, 740), 36)  # draws p2 circle
    # paints scores for each and adjust for double digit formatting
    p2 = font70.render(str(p2_pieces), 1, (150, 150, 150))
    p1 = font70.render(str(p1_pieces), 1, (150, 150, 150))
    if p1_pieces < 10:
        p1x = 477
    else:
        p1x = 462

    if p2_pieces < 10:
        p2x = 577
    else:
        p2x = 562

    screen.blit(p2, (p2x, 718))
    screen.blit(p1, (p1x, 718))
    if mode == 0 or (mode == 1 and piece == 1):
        pg.draw.rect(screen, (150, 150, 150), (250, 0, 800, 50))  # draws gray box on top
        current_turn = font70.render(word + "'S TURN", 1, color)
        screen.blit(current_turn, (375, 5))  # prints whose turn it is up top
    else:
        pg.draw.rect(screen, (150, 150, 150), (250, 0, 800, 50))  # draws gray box on top
        current_turn = font70.render("AI THINKING...", 1, color)
        screen.blit(current_turn, (375, 5))  # prints whose turn it is up top


def get_total_sandwiches(neighbor):
    """Function used to count how many of the opponent's pieces would be 'eaten' if the given
    neighbor was selected."""
    repeats = neighbors.count(neighbor)
    n_copy = neighbors.copy()
    s_copy = sandwiches.copy()
    eaten = 1  # start at 1 because player automatically places one piece
    for i in range(repeats):  # iterates through however many occurrence of the neighbor there are in the neighbors list
        index = n_copy.index(neighbor)  # indexes where it is
        # finds that spot in the parallel list of sandwiches and adds the len of it to the number of eaten
        eaten += len(s_copy[index])
        n_copy.pop(index)  # removes sandwich and neighbor from duped lists
        s_copy.pop(index)

    return eaten


def get_coordinates(x, y):
    """This function accepts coordinate points and re-formats them into column designations."""
    x = (x - 250) // 75
    y = (650 - y) // 75
    return [y, x]


def make_move(board, box, piece, options, middles):
    """This function accepts a board and box/neighbor and executes the move by altering the model/board."""

    board[box[0]][box[1]] = piece  # sets specified neighbor equal to current player's piece number
    repeats = options.count(box)  # counts how many times the neighbor is in the master list of neighbors
    for i in range(repeats):  # iterates through that number of times
        index = options.index(box)  # finds where the neighbor is in the list
        for middle in middles[index]:  # goes to that spot in the parallel list of sandwiches
            board[middle[0]][middle[1]] = piece  # makes each sandwich that is parallel to neighbor = piece
        # remove neighbor and sandwich from master lists so they can be re-indexed without duplication
        options.pop(index)
        middles.pop(index)
    return board


def display_winner():
    """This function is called when the game is over in order to display the winner onscreen."""
    if winner == 1:  # if the global variable winner is 1 then print that up top
        pg.draw.rect(screen, (150, 150, 150), (250, 0, 800, 50))  # grey box
        turn = font70.render('WHITE WINS', 1, (250, 250, 250))
        screen.blit(turn, (375, 5))  # paint message
    elif winner == 2:  # if the global variable winner is 2 then print that up top
        pg.draw.rect(screen, (150, 150, 150), (250, 0, 800, 50))  # grey box
        turn = font70.render("BLACK WINS", 1, (0, 0, 0))
        screen.blit(turn, (375, 5))  # paint message
    elif winner == 0:  # if the global variable winner is 2 then print that up top
        pg.draw.rect(screen, (150, 150, 150), (250, 0, 800, 50))  # grey box
        turn = font70.render("TIE GAME", 1, (250, 0, 0))
        screen.blit(turn, (375, 5))  # paint message
    cgs.draw_records(screen, 1, mode, logged_in, difficulty)  # update left panel with new record for game


def make_ai_move(array):
    """Function called when mode is set to AI and it is the AI's turn."""
    global turn, game_over, checking, previous_state

    def minimax(board, depth, alpha, beta, maximizingPlayer):
        """Function used to determine which column the AI should place their piece in. For any given board, it creates
        a copy and then deepens until specified depth (2, 4, 6). After reaches max depth it starts to build its way back
        up (out of the hole) and extend back down in next column."""
        global checking

        checking = True

        is_terminal = check_winner(board)  # checks to see if board is terminal node/ winner determined
        if depth == 0 or is_terminal:  # if end of recursion or terminal node
            if is_terminal:
                if check_winner(board) and winner == 2:  # if terminal node and winner is AI then return huge number
                    return None, 3000000000
                elif check_winner(
                        board) and winner == 1:  # if terminal node and winner is human then return tiny number
                    return None, -3000000000
                else:  # Game is over, no more valid moves
                    return None, 0  # if terminal node and winner is 0 then return 0 (game is over)
            if depth == 0:  # Depth is zero
                return None, count_pieces(board)[1]  # if end of recursion return score of the board (# of ai pieces)

        if maximizingPlayer:  # Even number in recursion/tree (want to maximize AI score)
            temp_neighbors, temp_sandwiches = get_valid_moves(board, 2, 1)  # gets the neighbors for given board
            if printing:
                if depth == 4:
                    print(len(temp_neighbors), temp_neighbors)
                elif depth == 2:
                    print('-------', len(temp_neighbors), temp_neighbors)

            value = 0
            if len(temp_neighbors) == 0:
                return [0, -3000]
            else:
                best_neighbor = temp_neighbors[0]
            for neighbor in temp_neighbors:
                b_copy1 = [x[:] for x in board]  # make a copy of the board
                b_copy1 = make_move(b_copy1, neighbor, 2, temp_neighbors.copy(), temp_sandwiches.copy())  # drop a piece in the copied board in current column in iteration
                if printing:
                    if depth == 4:
                        print('MAX--', neighbor, value, best_neighbor)
                    elif depth == 2:
                        print('-----------MAX--', neighbor, value, best_neighbor)
                new_score = minimax(b_copy1, depth - 1, alpha, beta, False)[1]  # alternate to min/next level in tree
                if printing:
                    if depth == 4:
                        print('MAX++', neighbor, 'score', new_score)
                    elif depth == 2:
                        print('-----------MAX++', neighbor, 'score', new_score)
                if new_score > value:  # if the minimax returns a score higher than default reset it to one found
                    value = new_score
                    best_neighbor = neighbor
                alpha = max(alpha, value)  # set alpha variable to alpha or value (whichever is higher)
                if alpha >= beta:  # ALPHA BETA PRUNING
                    break  # if winning move found or column found with score greater then beta, break out of loop
            return best_neighbor, value

        else:  # Odd number in recursion/tree (want to minimize Human score)
            temp_neighbors, temp_sandwiches = get_valid_moves(board, 1, 2)  # gets the neighbors for given board
            if printing:
                if depth == 3:
                    print('---', len(temp_neighbors), temp_neighbors)
                elif depth == 1:
                    print('--------------', len(temp_neighbors), temp_neighbors)
            value = 64
            if len(temp_neighbors) == 0:
                return [0, 3000]
            else:
                best_neighbor = temp_neighbors[0]
            for neighbor in temp_neighbors:  # iterate over all open columns
                b_copy2 = [x[:] for x in board]  # make a copy of the board
                b_copy2 = make_move(b_copy2, neighbor, 1, temp_neighbors.copy(), temp_sandwiches.copy())  # drop a piece in the copied board in current column in iteration
                if printing:
                    if depth == 3:
                        print('------MIN', neighbor, value, best_neighbor)
                    elif depth == 1:
                        print('--------------------MIN', neighbor, value, best_neighbor)
                new_score = minimax(b_copy2, depth - 1, alpha, beta, True)[1]  # alternate to max/next level in tree
                if printing:
                    if depth == 3:
                        print('++++++MIN++', neighbor, 'score', new_score)
                    elif depth == 1:
                        print('--------------------MIN++', neighbor, 'score', new_score)
                if new_score < value:  # if the minimax returns a score less than default reset it to one found
                    value = new_score
                    best_neighbor = neighbor  # set best_column to current iteration too
                beta = min(beta, value)  # set beta variable to beta or value (whichever is lower)
                if alpha >= beta:
                    break  # if winning move found or column found with score greater then beta, break out of loop
            return best_neighbor, value

    current_board = array.copy()  # copy the board for the minimax function
    move = minimax(current_board, difficulty, 2, 40, True)[0] # call the minimax to determine best column
    if move != 0:
        previous_state = 0
        pg.time.delay(2000)
        board = make_move(array, move, 2, neighbors, sandwiches)  # make the move that minimax determined
    else:
        color, piece, word = get_move()
        previous_state += 1
        pg.draw.rect(screen, (150, 150, 150), (250, 0, 800, 50))  # draws gray box on top
        current_turn = font70.render("SKIPPED" + str(word) + "'s TURN", 1, color)
        screen.blit(current_turn, (375, 5))  # prints whose turn it is up top
        pg.display.update()  # update the window with changes
        pg.time.delay(2000)

    if printing:
        print('[', move, ']')

    checking = False

    return board


def make_fonts_global():
    """Function that makes all of the fonts into global variables."""
    global font70, font50, font65, font27
    font70 = pg.font.SysFont('Comic Sans MS', 70)
    font50 = pg.font.SysFont('Comic Sans MS', 50)
    font65 = pg.font.SysFont('Comic Sans MS', 65)
    font27 = pg.font.SysFont('Comic Sans MS', 27)


def playing_game(board):
    """This function is called to commence the game and handles all interactions with the screen. It redirects events
    to their relevant functions. This is the brain of the game that re-formats and redirects data to be used in a
    meaningful manner."""
    global winner, turn, game_over, checking, previous_state, printing, logged_in, difficulty

    printing = False  # printing variable set up for when testing model changes
    # designate essential game variables
    game_over, turn, winner, previous_state = False, logged_in['current_othello'][1], 0, 0
    checking = False  # checking variable set to false when AI is not searching for move

    update_board(board)

    while True:

        for event in pg.event.get():
            piece = get_move()[1]

            if game_over:
                display_winner()
                cgs.dump(logged_in)

            if mode == 1 and turn % 2 == 0 and not game_over:  # if AI turn
                pg.mouse.set_visible(False)  # hide mouse while AI thinks
                board = make_ai_move(board)  # commence AI process
                pg.mouse.set_visible(True)
                turn += 1  # next turn
                update_board(board)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[0] < 190:
                    cgs.left_panel_event(1, screen, event, logged_in, mode, difficulty, board, turn, game_over)
                    difficulty = logged_in['current_othello'][3]

                else:
                    if not game_over:
                        box = get_coordinates(event.pos[0], event.pos[1])  # get the usable coordinates of click

                        if box in neighbors:
                            # if one of neighbors then make move
                            board = make_move(board, box, piece, neighbors, sandwiches)
                            turn += 1
                            update_board(board)

                        else:
                            break

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # if the user clicks esc
                if not game_over:  # saves data with function in cgs b4 exiting
                    logged_in = cgs.save_data(board, turn, 1, logged_in, difficulty, mode)
                cgs.dump(logged_in)  # dumps the newly updated user account
                cgs.main()  # calls cgs.main function to return to game option window (homepage when logged in)

            pg.display.update()


def main(pg):
    """This is the main function that is called to start/restart othello. It designates essential global variables
    and opens up the game data from files. It then commences the game by calling the playing_game function"""
    global screen, logged_in, mode, difficulty

    pickle_in_logged_in = open("logged_in", "rb")  # opens logged_in data
    logged_in = pickle.load(pickle_in_logged_in)

    screen = pg  # passed screen from cgs
    mode = logged_in['current_othello'][2]  # sets important user values/data
    difficulty = logged_in['current_othello'][3]

    # screen = pg.display.set_mode((700, 800))  # screen before cgs implementation

    make_fonts_global()  # globalizes all font surfaces to be used

    if logged_in['current_othello'][0] == []:  # if current user has no ongoing game then create a new board
        board = build_board()
    else:
        build_board_raw()  # because we are importing our own board, we need to specifically draw the board
        board = logged_in['current_othello'][0]  # import the board to resume from the (logged_in) user data

    playing_game(board)  # commence the game by calling the playing_game function


if __name__ == '__main__':
    main()