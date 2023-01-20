import datetime
import sys
import time
from random import randint
from texttable import Texttable
# from rich.table import Table
# from rich.console import Console
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore
from accounts import Account as account


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


def create_user():
    """
    Collects user input, validate input values and creates an account for user.
    Returns an account object.
    """
    user_account = []
    _acc_num = "ac" + str(randint(10000000000000,99999999999999))
    user_account.append(_acc_num)
    while True:
        f_name = input("\033[1m" + f"""{Fore.WHITE}    Enter first name: """)
        print("\n")
        if not f_name.isalpha():
            print(f"""{Fore.RED}!    Only alphabets allowed {f_name}, please try again\n""")
        elif len(f_name) < 2 or len(f_name) > 20:
            print(f"""{Fore.RED}    !Only 2 to 20 letters allowed - {f_name}, please try again\n""")
        else:
            break
    while True:
        l_name = input("\033[1m" + f"""{Fore.WHITE}    Enter last name: """)
        print("\n")
        if not l_name.isalpha():
            print(f"""{Fore.RED}    !Only alphabets allowed {l_name}, please try again\n""")
        elif len(l_name) < 2 or len(l_name) > 20:
            print(f"""{Fore.RED}    !Only 2 to 20 letters allowed- {l_name}, please try again\n""")
        else:
            break
    while True:
        pin_code = input(f"""{Fore.WHITE}    Please enter four digit number and remember this number for later use: """)
        print("\n")
        if not pin_code.isnumeric() or len(pin_code) != 4:
            print(f"""{Fore.RED}    Only four digit number allowed - {pin_code}, please try again\n""")
        else:
            break
    while True:
        deposit = input(f"""{Fore.WHITE}    Enter amount of cash you want to lodge into account: $ """)
        print("\n")
        if not deposit.isnumeric():
            print(f"""{Fore.RED}    Only numbers allowed - {deposit}, please try again\n""")
        else:
            break

    user_account.append(f_name)
    user_account.append(l_name)
    user_account.append(pin_code)
    user_account.append(float(deposit))
    time.sleep(3)
    print(f"""{Fore.GREEN}   Creating your account...\n""")
    word_wrap(f"""   {f_name} {l_name} your account has been created successfully.\n\n""")
    print(f"""   Please take note of your Account number and your PIN: \n""")
    word_wrap(f"""   Account Number: {_acc_num}, PIN: {pin_code}.\n""")
    debit_account_holder = account(user_account[0], user_account[1], user_account[2], user_account[3], user_account[4])
    SHEET.worksheet('accounts').append_row(user_account)
    return debit_account_holder


def validate__acc_num():
    """ Validates validity of user account number
        and terminates after 3 unsuccessfull attempts.
        Returns false on failure or returns account object on success.
    """
    account_holders = SHEET.worksheet('accounts').get_all_values()[1:]
    tries = 0
    while tries < 3:
        tries += 1
        num = input("\033[1m" + f"""{Fore.WHITE}    Enter account number here: """).strip()
        print("\n")
        current_user = [holder for holder in account_holders if num == holder[0]]
        if len(current_user) == 0:
            print(f"""{Fore.RED}    Account not recognized {num} \n""")
        else:
            break
    else:
        print(f"""{Fore.RED}    You have exceeded trial limit, please create an account.\n\n""")
        print(f"""{Fore.GREEN}    Thank you for using our services.\n""")
        time.sleep(2)
        return False
        # show_menu()
        # sys.exit()
    time.sleep(3)
    print(f"""{Fore.GREEN}    Checking validity of card ...\n""")
    word_wrap(f"""    Account valid proceed to enter PIN ...\n\n""")
    t_1 = current_user[0][0]
    t_2 = current_user[0][1]
    t_3 = current_user[0][2]
    t_4 = current_user[0][3]
    t_5 = current_user[0][4]

    return account(t_1, t_2, t_3, t_4, t_5)


def validate_pin(account_holder):
    """ Validates user input for PIN
        and terminates after 3 unsuccessfull attempts.
        Returns false or true.
    """
    tries = 0
    while tries < 3:
        tries += 1
        code = input(f"""{Fore.GREEN}    Enter four digit pin: """).strip()
        print("\n")
        if code == account_holder.get_pin():
            word_wrap(f"""    valid pin code, you have successfully logged in.\n\n""")
            break
        elif code != account_holder.get_pin():
            print(f"{Fore.RED}    !Pin code is not correct - {code}.\n")  
    else:
        print(f"""{Fore.YELLOW}   You have exceeded trial limit, please contact bank officials by phone.\n\n""")
        print(f"""{Fore.GREEN}    Thank you for using our services.\n""")
        return False
    # show menu for user 
    # show_menu() 
    return True


def display_account_details(account):
    """ Displays account details of a logged in user."""
    account_holders = SHEET.worksheet('accounts').get_all_values()[1:]
    current_user = [holder for holder in account_holders if account._acc_num == holder[0]]
    table = Texttable()
    table.header( ['Account Number','First Name', 'Last Name', 'PIN','Balance'])
    # for column in columns:
    #     table.add_column(column)
    for user in current_user:
        table.add_row(user)
    # table.add_row(current_user[0])
    # console = Console()
    # console.print(table)
    print(table.draw())


user = validate__acc_num()
validate_pin(user)
display_account_details(user)