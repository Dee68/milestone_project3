import datetime
import sys
import time
from random import randint
from rich.table import Table
from rich.console import Console
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('atm_abc')


def word_wrap(words):
    """ Delays the output of characters on terminal by some milliseconds"""
    for c in words:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)


def show_menu():
    """ Displays the menu to a user """
    word_wrap(f"""{Fore.YELLOW}
        |====================================================|
        |                                                    |
        |     WELCOME TO ABC ATM BANKING SYSTEM              |
        |                                                    |
        |   Please choose one of the following options:      |
        |                                                    |
        |     1. Create an account                           |
        |     2. Enter a deposit to account                  |
        |     3. Withdraw from account                       |
        |     4. Show account details                        |
        |     5. Show Transactions                           | 
        |     6. Exit                                        |    
        |====================================================|""")
    print("\n\n")

    