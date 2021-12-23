import cx_Freeze

executables = [cx_Freeze.Executable("cgs.py")]

cx_Freeze.setup(
    name= 'Capstone Game Suite APP',
    options= {"build_exe":
                   {"packages": ['pygame', 'sys', 'pickle', 'passlib.hash', 'gspread',
                                 'oauth2client.service_account', 'ast', 'math'],
                    "include_files": ['cgs_connect4.py', 'cgs_othello.py', 'cgs_checkers.py', 'credentials.json']
                    }
              },
    description= 'Capstone Game Suite built by Gilad Spitzer for final project in SAS Computer Science 2019',
    executables= executables
)