import pygame as pg, sys, pickle
import cgs_checkers, cgs_othello, cgs_connect4, cgs
from passlib.hash import pbkdf2_sha256
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ast


def left_panel_event(game, screen, event, logged_in, mode, difficulty, board, turn, game_over):
    """This function is not used in the cgs file but is used in all of the other games so is placed here to reference
    universally. It deals with any event in the left panel that occurs in any of the games."""
    def reset_progress(mode, logged_in, name):
        """Function that resets the user's currently saved game progress in their profile and then dumps that info back
        into the general game data."""
        logged_in['current_' + name][0] = []
        if mode == 0:  # if human mode than player 1 starts game
            logged_in['current_' + name][1] = 1
        elif mode == 1:  # if AI mode then player 2 (AI) starts game
            logged_in['current_' + name][1] = 0

    # sets names and files depending on which game function was called from
    if game == 0:
        name = 'connect4'
        file = cgs_connect4
    elif game == 1:
        name = 'othello'
        file = cgs_othello
    elif game == 2:
        name = 'checkers'
        file = cgs_checkers

    if 250 < event.pos[1] < 315:  # NEW GAME button clicked
        reset_progress(mode, logged_in, name)  # function that resets the user's current saved game position
        dump(logged_in)
        file.main(screen)  # calls the main function of game called from to restart the game
    elif 150 < event.pos[1] < 215:  # EXIT button is clicked
        if not game_over:  # saves data with function in cgs b4 exiting
            logged_in = cgs.save_data(board, turn, game, logged_in, difficulty, mode=mode)
        cgs.dump(logged_in)  # dumps the newly updated user account
        cgs.main()  # calls cgs.main function to return to game option window (homepage when logged in)
    elif 475 < event.pos[1] < 510:  # user wants to change MODE
        '''All data from ongoing game is lost when user switches mode'''
        if 10 < event.pos[0] < 95:  # user clicks on HUMAN
            if mode == 1:  # if the mode is currently AI then
                mode = 0  # switch mode to human
                logged_in['current_' + name][2] = mode  # save mode to profile
                logged_in['current_' + name][3] = 0  # save difficulty to profile
                reset_progress(mode, logged_in, name)  # function that resets the user's current saved game position
                cgs.dump(logged_in)  # saves edited logged_in data to file
                file.main(screen)  # calls the main function to restart the game
        elif 95 < event.pos[0] < 180:  # user clicks on AI
            if mode == 0:  # if the mode is currently HUMAN then
                mode = 1  # switch mode to AI
                logged_in['current_' + name][2] = mode  # save mode to profile
                logged_in['current_' + name][3] = 2  # save difficulty to profile
                reset_progress(mode, logged_in, name)  # reset progress in account
                cgs.dump(logged_in)  # saves edited logged_in data to file
                file.main(screen)  # calls the main function to restart the game
    elif 675 < event.pos[1] < 710:  # User changes difficulty
        if mode == 1:  # if in AI mode
            if 10 < event.pos[0] < 64:
                if difficulty != 2:
                    difficulty = 2  # changes difficulty and saves data
                    logged_in['current_' + name][3] = difficulty  # save difficulty to profile
                    cgs.dump(logged_in)
            if 64 < event.pos[0] < 128:  # user clicks on AI
                if difficulty != 4:
                    difficulty = 4  # changes difficulty and saves data
                    logged_in['current_' + name][3] = difficulty  # save difficulty to profile
                    cgs.dump(logged_in)
            if 128 < event.pos[0] < 190:  # user clicks on AI
                if difficulty != 6:
                    difficulty = 6  # changes difficulty and saves data
                    logged_in['current_' + name][3] = difficulty  # save difficulty to profile
                    cgs.dump(logged_in)
            cgs.draw_records(screen, game, mode, logged_in,
                             difficulty)  # draws left panel of game suite from cgs to re-draw updated difficulty
    return mode, difficulty


def draw_records(screen, game, mode, logged_in, difficulty):
    """This function is not used in the cgs file but is used in all of the other games so is placed here to reference
    universally. It draws the left panel of each game. It accepts the screen the game is using and all of the data
    printed on left panel."""
    pg.draw.rect(screen, (0, 0, 0), (0, 0, 200, 900))  # draws left black box
    make_fonts_global()

    pg.draw.rect(screen, (0, 150, 0), (10, 150, 180, 65))   # draws green new game box
    new_game = font50.render("New Game", 1, (250, 250, 250))
    pg.draw.rect(screen, (0, 150, 0), (10, 250, 180, 65))   # draws green EXIT box
    exit = font50.render("EXIT", 1, (250, 250, 250))
    screen.blit(exit, (65, 170))
    screen.blit(new_game, (12, 270))


    games = ['connect4', 'othello', 'checkers']  # game parameter --> (C4 = 0, O = 1, C= 2)

    record = font28.render('(Wins, Losses, Ties)', 1, (250, 50, 50), (0, 0, 0))  # shows counter place holders
    screen.blit(record, (8, 350))
    twoplayer = font20.render('vs Human', 1, (200, 200, 200), (0, 0, 0))  # human column for counter
    screen.blit(twoplayer, (30, 375))
    ai = font20.render('vs AI', 1, (200, 200, 200), (0, 0, 0))  # ai column for counter
    screen.blit(ai, (135, 375))

    display = str(games[game]) + '_record'  # alters record based on game
    record = font28.render(str(logged_in[display]), 1, (250, 0, 0), (0, 0, 0))
    screen.blit(record, (30, 395))  # shows human record
    record = font28.render(str(logged_in[display + '_ai']), 1, (250, 0, 0), (0, 0, 0))
    screen.blit(record, (118, 395))  # shows AI record

    mode_type = font30.render('MODE:', 1, (250, 250, 250), (0, 0, 0))  # mode selector (human/AI)
    screen.blit(mode_type, (67, 445))
    pg.draw.rect(screen, (90, 150, 240), (10, 475, 180, 35))  # blue box for mode selector
    pg.draw.rect(screen, (240, 240, 90), (95, 475, 2, 35))  # line dividing mode selector options
    if mode == 0:  # sets color for mode selector if in human mode
        ai_color = (250, 250, 250)
        human_color = (240, 240, 90)
        x1 = 10
        x2 = 95
    else:    # sets color for mode selector if in AI mode
        ai_color = (240, 240, 90)
        human_color = (250, 250, 250)
        x1 = 95
        x2 = 190
    human = font30.render('HUMAN', 1, human_color)  # puts text of human/AI into mode selector
    screen.blit(human, (14, 484))
    ai = font45.render('AI', 1, ai_color)
    screen.blit(ai, (125, 480))
    pg.draw.aalines(screen, (240, 240, 90), True, ((x1, 475),
                                                   (x1, 510),
                                                   (x2, 510),
                                                   (x2, 475)), 1)  # highlights which mode is active

    if difficulty > 0:
        mode_type = font30.render('DIFFICULTY:', 1, (250, 250, 250), (0, 0, 0))  # shows difficulty selector
        screen.blit(mode_type, (42, 650))
        pg.draw.rect(screen, (75, 0, 130), (10, 675, 180, 35))  # draws purple difficulty buttons
        easy = font50.render('*', 1, (240, 240, 90))  # first level
        med = font50.render('**', 1, (240, 240, 90))  # second level
        hard = font50.render('***', 1, (240, 240, 90))  # third level
        screen.blit(easy, (32, 685))
        screen.blit(med, (86, 685))
        screen.blit(hard, (143, 685))
        pg.draw.rect(screen, (90, 150, 240), (64, 675, 2, 35))  # dividers between difficulty options
        pg.draw.rect(screen, (90, 150, 240), (128, 675, 2, 35))

        # alters coordinates for highlighting box based on difficulty
        if difficulty == 2:
            x1 = 10
            x2 = 64
        elif difficulty == 4:
            x1 = 64
            x2 = 128
        elif difficulty == 6:
            x1 = 128
            x2 = 190

        pg.draw.aalines(screen, (90, 150, 240), True, ((x1, 675),
                                                       (x1, 710),
                                                       (x2, 710),
                                                       (x2, 675)), 1)  # highlights current difficulty box


def dump(logged_in):
    """This function is not directly used in the cgs file but is used in all of the other games so is placed here to
    reference universally. It accepts the logged_in variable/dictionary that is edited throughout the game and replaces
     whatever is in the saved file logged_in with the edited variable. This function ensures safe saving of progress.
     It is similar to the serial function but accepts a parameter instead of using a global variable."""
    pickle_out_logged_in = open("logged_in", "wb")  # opens logged_in file that holds currently logged in
    pickle.dump(logged_in, pickle_out_logged_in)  # replaces whatever is there with last saved data from game
    pickle_out_logged_in.close()  # closes file


# Above functions not directly used in cgs.py file


def draw_homescreen(box=None):
    """This function sets the window caption and also draws the homepage screen before selecting login or sign up"""
    pg.display.set_caption('CGS')
    pg.draw.rect(screen, (0, 0, 0), (0, 0, 700, 800))  # black box

    pg.draw.rect(screen, (255, 0, 0), (20, 20, 50, 50))  # red exit box
    exit = font85.render("X", 1, (250, 250, 250))
    screen.blit(exit, (25, 19))

    exit = font50.render("CAPSTONE GAME SUITE", 1, (250, 220, 90))  # yellow label
    screen.blit(exit, (135, 30))

    if box == 'login':  # if the
        pg.draw.rect(screen, (0, 100, 255), (140, 310, 140, 50))  # if hover over login then draw blue box around it
    elif box == 'create_account':
        pg.draw.rect(screen, (0, 100, 255), (330, 310, 275, 50))  # if hover over create acnt draw blue box around it

    login = font50.render("Login", 1, (250, 250, 250))
    screen.blit(login, (165, 320))

    exit = font50.render("Create Account", 1, (250, 250, 250))
    screen.blit(exit, (340, 320))


def draw_main_page():
    """This function draws the main menu page once the user is logged in. It displays the users records for each game,
    and has buttons to commence game play for each of the three games"""
    pg.draw.rect(screen, (0, 0, 0), (0, 80, 700, 800))  # black box

    name = font85.render(str('@' + logged_in['username']), 1, (200, 200, 200))
    screen.blit(name, (50, 100))  # @NAME

    pg.draw.rect(screen, (100, 255, 0), (550, 97, 95, 30))  # green box for log out button
    logout = font35.render("Logout", 1, (250, 250, 250))
    screen.blit(logout, (555, 100))

    record = font35.render('(Wins, Losses, Ties)', 1, (250, 50, 50))  # shows record place holders
    screen.blit(record, (410, 185))

    ai = font20.render('vs AI', 1, (200, 200, 200))  # small sub text
    screen.blit(ai, (560, 215))

    twoplayer = font20.render('vs Human', 1, (200, 200, 200))  # small sub text
    screen.blit(twoplayer, (440, 215))

    pg.draw.rect(screen, (0, 65, 0), (180, 250, 210, 65))  # green othello box
    exit = font50.render("OTHELLO", 1, (250, 250, 250))
    screen.blit(exit, (202, 270))

    pg.draw.rect(screen, (0, 100, 255), (180, 400, 210, 65))  # blue connect4 box
    exit = font50.render("CONNECT 4", 1, (250, 250, 250))
    screen.blit(exit, (185, 420))

    pg.draw.rect(screen, (90, 45, 0), (180, 550, 210, 65))  # red checkers box
    exit = font50.render("CHECKERS", 1, (250, 250, 250))
    screen.blit(exit, (185, 570))

    record = font35.render(str(logged_in['othello_record']), 1, (250, 0, 0))  # othello record
    screen.blit(record, (430, 270))
    record = font35.render(str(logged_in['othello_record_ai']), 1, (250, 0, 0))  # othello AI record
    screen.blit(record, (540, 270))

    record = font35.render(str(logged_in['connect4_record']), 1, (250, 0, 0))  # connect4 record
    screen.blit(record, (430, 420))
    record = font35.render(str(logged_in['connect4_record_ai']), 1, (250, 0, 0))  # connect4 AI record
    screen.blit(record, (540, 420))

    record = font35.render(str(logged_in['checkers_record']), 1, (250, 0, 0))  # checkers record
    screen.blit(record, (430, 570))
    record = font35.render(str(logged_in['checkers_record_ai']), 1, (250, 0, 0))  # checkers AI record
    screen.blit(record, (540, 570))


def save_data(board, turn, game, logged_in, difficulty, mode):
    """This function takes the current board from any game and whose turn it is and saves it to their account. It is
     called when the user exits a game in the middle (AUTO-SAVE FEATURE)"""

    if game == 0:  # if the function was called from connect4
        if board != [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]:  # generic connect4 board
            logged_in['current_connect4'][0] = board  # saves progress in profile
            logged_in['current_connect4'][1] = turn
            logged_in['current_connect4'][2] = mode
            logged_in['current_connect4'][3] = difficulty
    elif game == 1:
        if board != [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 1, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]:  # generic othello board
            logged_in['current_othello'][0] = board  # saves progress in profile
            logged_in['current_othello'][1] = turn
            logged_in['current_othello'][2] = mode
            logged_in['current_othello'][3] = difficulty
    elif game == 2:
        if board != [[0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 2, 0, 2, 0, 2, 0],
                     [0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0]]:  # generic checkers board
            logged_in['current_checkers'][0] = board  # saves progress in profile
            logged_in['current_checkers'][1] = turn
            logged_in['current_checkers'][2] = mode
            logged_in['current_checkers'][3] = difficulty

    return logged_in  # returns the edited/updated account dictionary (who ever is currently logged in)


def get_data_from_drive(username):
    """After a user logs in, this function is called to retrieve their data from their profile and turn it into a
    usable format for their stay in the app"""
    pos = sheet.find(username)  # finds their designated row in sheet
    row = sheet.row_values(pos.row)  # gets all of the values in their row
    variables = ['username', 'password', 'connect4_record_ai', 'connect4_record', 'checkers_record_ai',
                 'checkers_record', 'othello_record_ai', 'othello_record', 'current_checkers', 'current_connect4',
                 'current_othello']  # list of corresponding/parallel variable names
    dictionary = {}  # blank dictionary to add their data to
    for i in range(len(variables)):
        if i > 1:  # sets each variable in list equal to corresponding value from sheet
            dictionary[variables[i]] = ast.literal_eval(row[i + 1])  # (uses module to convert string to literal)
        else:
            dictionary[variables[i]] = row[i + 1]

    return dictionary


def submit_data(username, password):
    """This function accepts the data (username and password) that the user has provided in the login process and
    cross references it with the google sheet to see if their account exists, if they are logged in somewhere else
    already or if they entered the wrong password."""
    if username.lower() in users:  # if the global value of users (list of all users in sheet) contains this username:
        pos = sheet.find(username)  # then find the row that the user's data is in
        if sheet.cell(pos.row, 13).value == '0':  # if they are not logged in elsewhere then check password
            if not pbkdf2_sha256.verify(password, sheet.cell(pos.row, 3).value):
                # cross references password entered with de-hashed one their account on sheet
                return [False, 'Incorrect Password']  # if their password is wrong, return error message
            else:  # if their password is correct then update column of sheet stating that they are logged in somewhere
                sheet.update_cell(pos.row, 13, '1')
                return [True, "You're in!"]
        else:  # if last column of their profile is 1 then they are logged in elsewhere
            return [False, 'Already logged in somewhere']
    else:  # they do not have an account
        return [False, "No profile associated with that username. Try again"]


def create_account(name, password):
    """This function accepts the text for the username and password that the user entered. It then creates a profile
    for them."""
    if len(name) > 7 or len(name) < 2:  # if username length is out of boundary, return error
        return [False, 'Username must be longer than 2 characters and less than 7']
    elif name.lower() in users:  # if username already in database then return error
        return [False, 'User already exists. Try Logging In']
    else:
        username = name  # username variable is the submitted name
        name = name.lower()  # name variable is lowercase version of submitted name
        hash_key = pbkdf2_sha256.hash(password)  # hashed version of password

        # generic data for beginner account
        data = [name, str(username), str(hash_key), str([0, 0, 0]), str([0, 0, 0]), str([0, 0, 0]), str([0, 0, 0]),
                str([0, 0, 0]), str([0, 0, 0]), str([[], 1, 0, 0]), str([[], 1, 0, 0]), str([[], 1, 0, 0]), 1]

        row = len(sheet.col_values(1)) + 1  # designate next available row for new user

        cell_list = sheet.range('A' + str(row) + ':M' + str(row))  # Selects a cell range

        for i in range(len(cell_list)):  # updates local version of sheet with corresponding data
            cell_list[i].value = data[i]

        sheet.update_cells(cell_list)  # pastes local edited sheet to web one

        return [True, '']


def serial(exit=None):
    """This function serials the user data into the local logged_in file"""
    pickle_out_logged_in = open("logged_in", "wb")  # opens the logged_in file
    if exit: # if the optional exit parameter is specified then dump False (no user data) and the close app
        pickle.dump(False, pickle_out_logged_in)
        pickle_out_logged_in.close()
        sys.exit()
    else:  # otherwise pickle out their data (used for closing games but not entire app)
        pickle.dump(logged_in, pickle_out_logged_in)
        pickle_out_logged_in.close()


def login():
    """This function is called various times throughout the logging in process and creating account process. It draws
    the page according to the clicks that it the screen resopnds to."""
    pg.draw.rect(screen, (250, 250, 250), (0, 80, 700, 800))  # white box background

    pg.draw.rect(screen, (88, 140, 170), (30, 100, 60, 25))  # blue box for back button
    arrow = font50.render("<---", 1, (250, 250, 250))  # back button
    screen.blit(arrow, (32, 93))

    pg.draw.rect(screen, (190, 190, 190), (250, 197, 350, 40))  # grey box for text username
    username = font50.render("USERNAME:", 1, (0, 0, 0))
    screen.blit(username, (25, 200))
    if typing == 'username':  # if user is typing then highlight box
        pg.draw.aalines(screen, (250, 220, 90), True, ((250, 195),
                                                       (250, 235),
                                                       (600, 235),
                                                       (600, 195)), 1)

    pg.draw.rect(screen, (190, 190, 190), (250, 277, 350, 40))  # grey box for text password
    password = font50.render("PASSWORD:", 1, (0, 0, 0))
    screen.blit(password, (25, 280))
    if typing == 'password':  # if user is typing then highlight box
        pg.draw.aalines(screen, (250, 220, 90), True, ((250, 275),
                                                       (250, 315),
                                                       (600, 315),
                                                       (600, 275)), 1)

    if len(password_text) > 0:  # if the text entered for password is longer than 0, show the (show/hide) button
        pg.draw.rect(screen, (220, 220, 220), (550, 278, 49, 38))  # show/hide button background
        if show_text:  # if text is being shown, give hide option
            text = font20.render(" HIDE", 1, (200, 100, 50))
        else:  # if text is not being shown then give show option
            text = font20.render("SHOW", 1, (200, 100, 50))
        screen.blit(text, (555, 290))

    pg.draw.rect(screen, (20, 250, 20), (250, 363, 145, 40))  # draw green submit button
    if loggining_in:  # alter text depending on which option you chose
        username = font40.render("Login", 1, (250, 250, 250))
    elif creating_account:
        username = font40.render("Sign Up", 1, (250, 250, 250))
    screen.blit(username, (273, 370))


def save_progress():
    """This function takes the user's records and saved game progress and pastes it into their account file on the
    google sheet."""
    if logged_in != False:  # if the user is still logged in
        data = [*logged_in.values()]  # then turn the dictionary of their data into a list
        data.append('0')  # add a zero for the status column of the drive
        row = sheet.find(data[0])  # find their name in the drive and store the row of their name

        # Select a cell range to paste their content to
        cell_list = sheet.range('B' + str(row.row) +':M' + str(row.row))
        # Update values
        for i in range(len(cell_list)):
            cell_list[i].value = str(data[i])  # updates temporary local sheet

        sheet.update_cells(cell_list)  # replaces online sheet with it


def setup_drive():
    """This function sets (with the help of service account credentials)up the global variable that modifies the
     google sheet"""
    global sheet
    scope = ['https://www.googleapis.com/auth/drive']  # link of authorization
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)  # credentials of sheet

    client = gspread.authorize(credentials)  # authorizes credentials
    sheet = client.open('CGS_DATA').sheet1  # opens the sheet up into the sheet variable


def make_fonts_global():
    """This font instantiates the font options as global variables to be used throughout the program."""
    global font25, font40, font85, font50, font35, font20, font28, font45, font30
    pg.font.init()  # sets up fonts within pygame
    font40 = pg.font.SysFont('Comic Sans MS', 40)
    font25 = pg.font.SysFont('Comic Sans MS', 25)
    font85 = pg.font.SysFont('Comic Sans MS', 85)
    font50 = pg.font.SysFont('Comic Sans MS', 50)
    font35 = pg.font.SysFont('Comic Sans MS', 35)
    font20 = pg.font.SysFont('Comic Sans MS', 20)
    font28 = pg.font.SysFont('Comic Sans MS', 28)
    font45 = pg.font.SysFont('Comic Sans MS', 45)
    font30 = pg.font.SysFont('Comic Sans MS', 30)


def main():
    """This function is called when the app is opened and is the heart of the entire app. It sets default variables
    and then opens infinite loop that app is ran in."""
    global screen, game_over, logged_in, users, typing, loggining_in, creating_account, password_text, show_text

    make_fonts_global()   # makes fonts global throughout
    screen = pg.display.set_mode((700, 800))  # sets screen size
    loggining_in, creating_account, typing, show_text = False, False, False, False  # sets variables to defaults
    username, password, password_text, typing = '', '', '', ''  # sets temp text variables to blank

    setup_drive()  # sets up google sheet variable with credentials

    users = sheet.col_values(1)  # gets list of all user names
    try:
        pickle_in_logged_in = open("logged_in", "rb")  # try to pickle in logged_in data from local file
        logged_in = pickle.load(pickle_in_logged_in)
    except FileNotFoundError:
        logged_in = False  # if file does not exist then nobody is logged in

    draw_homescreen()  # draws the home screen before user selects login or create_account

    while True:  # opens infinite loop that app runs in
        for event in pg.event.get():
            if logged_in != False:    # IF THE USER IS LOGGED IN
                draw_main_page()  # draws main menu with all three game options
                if event.type == pg.MOUSEBUTTONDOWN:
                    if 200 < event.pos[0] < 450:  # if user selects to play game
                        if 250 < event.pos[1] < 315:  # reformat screen and start othello game
                            pg.display.set_mode((900, 800))
                            cgs_othello.main(screen)
                        elif 400 < event.pos[1] < 465:   # reformat screen and start connect4 game
                            pg.display.set_mode((900, 800))
                            cgs_connect4.main(screen)
                        elif 550 < event.pos[1] < 615:
                            pg.display.set_mode((900, 800))  # reformat screen and start othello game
                            cgs_checkers.main(screen)
                    elif 550 < event.pos[0] < 645 and 97 < event.pos[1] < 127:  # if user opts to log out
                        save_progress()  # save their progress to the google drive
                        logged_in = False  # set logged_in to False
                        serial()  # serial the logged_in variable out into its local file
                        draw_homescreen()  # draw the original homes creen with options to log in or create account
            else:  # IF THE USER IS NOT LOGGED IN
                if not loggining_in and not creating_account:  # IF THE USER IS ON HOMEPAGE
                    if event.type == pg.MOUSEMOTION:  # if user hovers over option
                        if 140 < event.pos[0] < 280 and 310 < event.pos[1] < 360:
                            draw_homescreen('login')  # if user hovers over login then it draws login page
                        elif 330 < event.pos[0] < 605 and 310 < event.pos[1] < 360:
                            draw_homescreen('create_account')  # if user hovers on create account then draws that page
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if 310 < event.pos[1] < 360:
                            if 140 < event.pos[0] < 280:
                                # if user clicks login then set variable
                                loggining_in = True
                            elif 330 < event.pos[0] < 605:
                                # if user clicks create account then set variable
                                creating_account = True
                            login()  # call login function
                elif loggining_in or creating_account:  # IF THE USER IS LOGGING IN
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if 250 < event.pos[0] < 600:  # if user clicks on text box
                            if 200 < event.pos[1] < 240:
                                typing = 'username'  # if user clicks username textbox then set variable
                            elif 277 < event.pos[1] < 317:
                                typing = 'password'    # if user clicks password textbox then set variable
                                if event.pos[0] > 545 and len(password_text) > 0:  # if click on show/hide button
                                    if show_text:  # flip the button's state if clicked
                                        show_text = False
                                    else:
                                        show_text = True
                            else:  # otherwise user has de-selected typing box
                                typing = ''
                            login()  # re-calls login function to re-draw page without text box highlighting

                        if 30 < event.pos[0] < 90 and 100 < event.pos[1] < 125:  # if user clicks back button then exit
                            main()

                        if 250 < event.pos[0] < 395 and 364 < event.pos[1] < 404:  # if user clicks submit
                            if loggining_in:  # if user is logging in then submit their data
                                response = submit_data(username.lower(), password)  # submits user data and gets status
                                show_text = False  # re-hide their text
                                if response[0]:  # if they have account and entered data correctly
                                    loggining_in = False  # user is no longer logging in
                                    logged_in = get_data_from_drive(username)  # gets dictionary of data to be used
                                    # sets variable to data from profile that will be edited during their stay
                                    serial()  # saves their newly logged_in state (and data) to the local file
                                else:
                                    error = font28.render(str(response[1]), True, (250, 0, 0), (250,250, 250))
                                    screen.blit(error, (100, 485))  # if wrong info entered print error message
                                username, password, password_text = '', '', ''  # reset type variables to empty
                            elif creating_account:
                                response = create_account(username, password)  # call function to create account
                                if not response[0]:  # if error in creating account
                                    username, password, password_text = '', '', ''  # clear text boxes
                                    error = font28.render(str(response[1]), True, (250, 0, 0), (250, 250, 250))
                                    screen.blit(error, (100, 485))  # print error message
                                else:
                                    creating_account = False  # no longer creating account
                                    logged_in = get_data_from_drive(username)  # gets dictionary of data to be used
                                    serial()  # saves their newly logged_in state (and data) to the local file

                    elif event.type == pg.KEYDOWN:  # if user clicks key on keyboard
                        if event.key == pg.K_ESCAPE:
                            main()  # if user clicks escape then exit to main/home screen
                        if event.key == pg.K_BACKSPACE:  # if user clicks backspace
                            if typing == 'username':  # and they are typing in username textbox
                                username = username[:-1]  # then delete one character from username variable
                            elif typing == 'password':   # or they are typing in password textbox
                                password = password[:-1]  # then delete one character from password variable
                                password_text = password_text[:-1]  # and delete one character from text variable (***)
                            else:
                                break
                        elif event.key == pg.K_TAB:  # if user clicks tab or enter
                            if typing == 'username':  # if they are typing username then switch to password
                                typing = 'password'
                                login()  # re-draw board

                        else:  # otherwise (if they are typing) add the character to their textbox
                            if typing == 'username':
                                username += event.unicode
                            elif typing == 'password':
                                password += event.unicode
                                if event.key != pg.K_LSHIFT and event.key != pg.K_RSHIFT:
                                    password_text += '*'  # if they hit any char except shift, add it to *** counter
                            else:
                                break
                        login()  # redraw login page

                    username_blit = font45.render(str(username), True, (250, 250, 250))  # paste username
                    if show_text:  # paste password or *** version
                        password_blit = font45.render(str(password), True, (250, 250, 250))
                    else:
                        password_blit = font45.render(str(password_text), True, (250, 250, 250))
                    screen.blit(username_blit, (260, 203))
                    screen.blit(password_blit, (260, 283))

            if event.type == pg.QUIT:  # if user tries to quit then save progress to drive and serial out
                save_progress()
                serial(True)

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                main()  # if they click

            if event.type == pg.MOUSEBUTTONDOWN:  # if user clicks app's red X button then save progress and serial out
                if 20 < event.pos[0] < 70 and 20 < event.pos[1] < 70:
                    save_progress()
                    serial(True)

            pg.display.update()  # update screen


if __name__ == '__main__':
    main()