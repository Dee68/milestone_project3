import datetime
import sys
import time
from random import randint
from accounts import Account as account
from texttable import Texttable
import gspread
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore
colorama.init()


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
        time.sleep(0.01)


def greet():
    """ Displays a welcome message. """
    word_wrap(f"""{Fore.CYAN}
    =========================================================
    █░█░█ █▀▀ █░░ █▀▀ █▀█ █▀▄▀█ █▀▀   ▀█▀ █▀█
    ▀▄▀▄▀ ██▄ █▄▄ █▄▄ █▄█ █░▀░█ ██▄   ░█░ █▄█

    ▄▀█ █▄▄ █▀▀   ▄▀█ ▀█▀ █▀▄▀█
    █▀█ █▄█ █▄▄   █▀█ ░█░ █░▀░█

    █▄▄ ▄▀█ █▄░█ █▄▀ █ █▄░█ █▀▀
    █▄█ █▀█ █░▀█ █░█ █ █░▀█ █▄█

    █▀ █▄█ █▀ ▀█▀ █▀▀ █▀▄▀█
    ▄█ ░█░ ▄█ ░█░ ██▄ █░▀░█
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++""")


def ask_to_continue(current_user):
    """Asks user to continue or exit. """
    while True:
        choice = input("Do you wish to continue?(Y/N): ")
        if choice and choice.strip().lower()[0] == 'y':
            if current_user:
                p = show_menu()
                do_options(p, current_user)
                break
            else:
                p = controller()
                break
        elif choice and choice.strip().lower()[0] == 'n':
            print(f"""{Fore.GREEN}\n\nTHANK YOU FOR USING OUR SERVICES.""")
            if current_user:
                greet()
                p = controller()
            # sys.exit()
            break
        else:
            print(f"{Fore.RED}Enter only yes or no!!!\n")


def show_menu():
    """ Displays the menu to a user and takes in option input,
        validates it and return an integer of it.
        Returns:(Integer) the value of the option chosen.
    """
    word_wrap(f"""{Fore.CYAN}
    |====================================================|\n
    ********* WELCOME TO Abc ATM BANKING SYSTEM ********
    **** Please choose one of the following options: ****\n
    ****** 1.Enter Deposit ******************************\n
    ****** 2. Withdraw amount ***************************\n
    ****** 3. Show Account Details **********************\n
    ****** 4. Show Transactions *************************\n
    ****** 5. EXIT **************************************\n
    |====================================================|\n""")
    print("\n")
    while True:
        try:
            option = input(f"""{Fore.WHITE}Enter option(1-5): """).strip()
            print("\n\n")
            if not option:
                raise ValueError("Enter a value")
            if not option.isnumeric() and option not in [1, 2, 3, 4, 5]:
                raise ValueError(f"!Please follow the instructions: {option}.")
            break
        except ValueError as e_rr:
            print(f"""{Fore.RED}{e_rr}\n""")
            print("Try again\n")
    return int(option)


def welcome_message():
    """ Asks user if user has an account or not and
        returns first letter in lower case of user input.
        Returns:
            string: either y or n
     """
    while True:
        try:
            print("\n")
            abc_user = input(f"{Fore.WHITE}Do you have an account with us?:  ")
            abc_user = abc_user.lower()
            if not abc_user:
                raise ValueError("Enter a value")
            if not abc_user[0].isalpha():
                raise ValueError("Spaces or special characters not allowed")
            if abc_user and abc_user[0] in ('y', 'n'):
                break
            raise ValueError(f"Answer only: yes or no - {abc_user}")
        except ValueError as e_rr:
            print("\n")
            print(f"""{Fore.RED}{e_rr}.\n\n""")
            print("Try again.\n")
    return abc_user


def create_user():
    """Collects input,validate input values and creates an account for user.
    Returns:
        object: instance of the Account class.
    """
    time.sleep(2)
    print("\n\n")
    word_wrap(f"""{Fore.WHITE}    ============= ACCOUNT CREATION =============
    |===========================================|\n\n""")
    user_account = []
    acc_num = "ac" + str(randint(10000000000000, 99999999999999))
    user_account.append(acc_num)
    while True:
        f_name = input("\033[1m" + f"""{Fore.WHITE}Enter first name: """)
        print("\n")
        if not f_name:
            print(f"{Fore.RED}{f_name}!Please enter a value\n")
            print("Try again\n")
        elif not f_name.isalpha():
            msg1 = "Enter a single name only"
            msg = "Numbers, spaces and special characters "
            print(f"{Fore.RED}!{msg1} {f_name}\n")
            print(f"!{msg} \n")
            print("Not allowed,please try again\n")
        elif len(f_name) < 2 or len(f_name) > 20:
            print(f"{f_name}\n")
            print(f"{Fore.RED}!Only 2 to 20 letters allowed.\n")
            print(f"{Fore.RED}Please try again\n")
        else:
            break
    while True:
        l_name = input("\033[1m" + f"""{Fore.WHITE}Enter last name: """)
        print("\n")
        if not l_name:
            print(f"{Fore.RED}{l_name}!Please enter a value\n")
            print("Try again\n")
        elif not l_name.isalpha():
            msg1 = "Enter a single name only"
            msg = "Numbers, spaces and special characters "
            print(f"{Fore.RED}!{msg1} {l_name}\n")
            print(f"!{msg} \n")
            print("Not allowed please try again.\n")
        elif len(l_name) < 2 or len(l_name) > 20:
            print(f"{l_name}\n")
            print(f"{Fore.RED}!Only 2 to 20 letters allowed\n")
            print(f"{Fore.RED}Please try again\n")
        else:
            break
    while True:
        pin_code = input(f"{Fore.WHITE}Please enter PIN: ")
        print("Take a note of this number for later use\n")
        if not pin_code:
            print(f"{Fore.RED}!Enter value for PIN\n")
            print(f"{Fore.RED}Try again\n")
        elif not pin_code.isnumeric() or len(pin_code) != 4:
            print(f"{Fore.RED}!Only four digit number allowed -{pin_code}\n")
            print(f"{Fore.RED}Try again\n")
        else:
            break
    while True:
        deposit = input(f"{Fore.WHITE}Enter amount to lodge:💵 $ ")
        print("\n")
        if not deposit.isnumeric():
            print(f"{Fore.RED} Only numbers allowed - {deposit}\n")
            print(f"{Fore.RED}Please try again")
        else:
            break
    user_account.append(f_name)
    user_account.append(l_name)
    user_account.append(pin_code)
    user_account.append(float(deposit))
    time.sleep(3)
    print(f"{Fore.GREEN}Creating your account...\n")
    msg = "your account has been created successfully"
    word_wrap(f"{f_name} {l_name} {msg}.\n\n")
    print(f"Please take note of your Account number and your PIN: \n")
    word_wrap(f"Account Number: {acc_num}, PIN: {pin_code}.\n")
    a_1 = user_account[0]
    a_2 = user_account[1]
    a_3 = user_account[2]
    a_4 = user_account[3]
    a_5 = user_account[4]
    debit_account_holder = account(a_1, a_2, a_3, a_4, a_5)
    SHEET.worksheet('accounts').append_row(user_account)
    return debit_account_holder


def validate__acc_num():
    """ Validates validity of user account number
        and terminates after 3 unsuccessfull attempts.
        Returns false on failure or returns account object on success.
        Returns:
            object: Instance of the Account class.
    """
    print("\n\n")
    word_wrap("============== ACCOUNT VALIDATION ==============\n\n")
    account_holders = SHEET.worksheet('accounts').get_all_values()[1:]
    tries = 0
    while tries < 3:
        tries += 1
        num = input(f"{Fore.WHITE}Enter account number here:💳 ")
        print("\n")
        cur_user = [h for h in account_holders if num == h[0]]
        if not num:
            print(f"{Fore.RED}Enter account number\n")
        elif len(cur_user) == 0:
            print(f"""{Fore.RED}Account not recognized {num} \n""")
        else:
            break
    else:
        print(f"{Fore.RED}You have exceeded trial limit.\n")
        print(f"{Fore.RED}Please contact the bank officials.\n")
        print(f"{Fore.YELLOW}Or create an account.\n")
        print(f"""{Fore.GREEN}Thank you for using our services.\n\n""")
        time.sleep(2)
        return False
    time.sleep(3)
    print(f"{Fore.GREEN}Checking validity of account ...\n")
    word_wrap(f"Account valid proceed to enter PIN ...\n\n")
    t_1 = cur_user[0][0]
    t_2 = cur_user[0][1]
    t_3 = cur_user[0][2]
    t_4 = cur_user[0][3]
    t_5 = cur_user[0][4]

    return account(t_1, t_2, t_3, t_4, t_5)


def validate_pin(acc_holder):
    """Validates user input for PIN,terminates after 3 unsuccessfull attempts.
    Args:
        acc_holder (Account): instance of the Account class
    Returns:
        bool: True if successfull else False
    """
    print("\n\n")
    word_wrap(f"{Fore.GREEN}=========== PIN VALIDATION ============\n\n")
    tries = 0
    while tries < 3:
        tries += 1
        code = input(f"{Fore.GREEN}Enter PIN: ").strip()
        print("\n")
        if code == acc_holder.pin:
            word_wrap("valid PIN, you have successfully logged in.\n\n")
            break
        if not code:
            print(f"{Fore.RED}!Enter a value for pin")
        elif code != acc_holder.get_pin():
            print(f"{Fore.RED}!Pin code is not correct - {code}.\n")
    else:
        print(f"{Fore.YELLOW}You have exceeded trial limit.\n")
        print("Contact bank officials by phone.\n")
        time.sleep(2)
        return False
    return True


def deposit(acc_holder):
    """Deposit amount of money to own account,
        updates the transaction worksheet and terminates
        after 3 unsuccessfull attempts.

    Args:
        acc_holder (Account): instance of the class Account

    Returns:
        bool: (status)True if successful or else False
    """
    word_wrap("========== DEPOSIT OPERATION =============\n\n")
    transact = []
    td = str(int(datetime.datetime.now().timestamp()))
    trans_id = "D" + str(randint(0, 101)) + td
    transact.append(trans_id)
    transact.append(acc_holder.acc_num)
    transact.append(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    tries = 0
    while tries < 3:
        tries += 1
        amount = input(f"{Fore.GREEN}Enter amount here 💵:$ ")
        print("\n")
        word_wrap("Checking the input amount ...\n")
        time.sleep(2)
        if not amount.isnumeric():
            print(f"{Fore.RED}Only figures of amount allowed - {amount}\n")
            status = False
            new_balance = float(acc_holder.balance)
        else:
            status = True
            new_balance = float(acc_holder.balance) + float(amount)
            break
    else:
        print(f"{Fore.YELLOW}Sorry you've reached your trial limit.\n")
        print("Consult bank officials by phone for further instructions.\n")
    if not amount.isnumeric():
        new_balance = float(acc_holder.balance)
    else:
        new_balance = float(acc_holder.balance) + float(amount)
    acc_holder.balance = new_balance
    bal = str(int(acc_holder.balance))
    print(f"{Fore.WHITE}Your current balance is {bal} \n")
    card_holder = SHEET.worksheet('accounts').find(acc_holder.acc_num)
    SHEET.worksheet('accounts').update_cell(card_holder.row, 5, bal)
    if status:
        transact.append('SUCCESS')
        print(f"{Fore.GREEN}Successfully deposited ${str(amount)}.\n")
    else:
        transact.append('FAILURE')
    transact.append(amount)
    SHEET.worksheet('transaction').append_row(transact)
    return status


def withdraw(acc_holder):
    """Withdraws amount of money from account
        if availabe or shows corresponding error,
        and updates the transaction worksheet, returns status.

    Args:
        acc_holder (Account): instance of the Account class

    Raises:
        Exception: invalid input(ValueError)
        Exception: valid input value but insufficent fund

    Returns:
        bool: True if successful else False
    """
    word_wrap("========== WITHDRAWAL OPERATION ==============\n\n")
    transact = []
    trans_id = "W"
    trans_id += str(randint(0, 101))
    trans_id += str(int(datetime.datetime.now().timestamp()))
    transact.append(trans_id)
    transact.append(acc_holder.acc_num)
    transact.append(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    try:
        amount = input(f"{Fore.GREEN}Amount to withdraw:$ ")
        print("\n")
        if not amount.isnumeric():
            status = False
            raise Exception(f"Only figures of amount allowed {amount}")
        if float(acc_holder.balance) < float(amount):
            status = False
            raise Exception(f"Insufficient funds: {acc_holder.balance}")
        word_wrap(f"You are good to go! Thank you:💵 \n")
        acc_holder.set_balance(float(acc_holder.balance) - float(amount))
        print(f"Your current balance is : {str(acc_holder.balance)}\n")
        card_holder = SHEET.worksheet('accounts').find(acc_holder.acc_num)
        bal = str(int(acc_holder.balance))
        SHEET.worksheet('accounts').update_cell(card_holder.row, 5, bal)
        status = True
    except Exception as e_rr:
        print(f"{Fore.RED}{e_rr}, {Fore.GREEN}perhaps you need  a credit.\n\n")
        print(f"{Fore.GREEN}Call the bank and talk things over with them.\n\n")
        status = False
    if status:
        transact.append('SUCCESS')
    else:
        transact.append('FAILURE')
    camount = "-" + str(amount)
    transact.append(camount)
    SHEET.worksheet('transaction').append_row(transact)
    return status


def display_account_details(acc_holder):
    """Displays account details of a logged in user.

    Args:
        acc_holder (Account): instance of Account class.
    """
    acc_holders = SHEET.worksheet('accounts').get_all_values()[1:]
    cur_user = [h for h in acc_holders if acc_holder.acc_num == h[0]]
    table = Texttable()
    h_1 = ['Account Number', 'First Name', 'Last Name', 'PIN', 'Balance']
    table.header(h_1)
    for user in cur_user:
        table.add_row(user)
    print(table.draw())
    print("\n\n")
    ask_to_continue(acc_holder)


def transcript_receipt(acc_holder):
    """Displays all transactions of a user if any

    Args:
        acc_holder (Account): instance of the Account class.
    """
    transactions = SHEET.worksheet('transaction').get_all_values()[1:]
    user_transacts = [tr for tr in transactions if acc_holder.acc_num == tr[1]]
    if len(user_transacts) == 0:
        word_wrap(f"{Fore.CYAN}You've no transactions done yet\n")
        ask_to_continue(acc_holder)
    else:
        table = Texttable()
        h_1 = ['TransactionId', 'AccountId', 'Date & Time', 'Status', 'Amount']
        table.header(h_1)
        for transcript in user_transacts:
            t_1 = transcript[4][0]
            t_2 = transcript[4][1:]
            t_3 = transcript[3]
            if t_1 == '-' and t_2.isnumeric() and t_3 == 'FAILURE':
                transcript[4] += ' Insufficient fund.'
            elif not transcript[4][-1].isnumeric():
                transcript[4] += ' Invalid input'
            table.add_row(transcript)
        print(f"YOUR TRANSACTIONS\n")
        print(table.draw())
        print("\n\n")
        ask_to_continue(acc_holder)


def do_options(p, abc_user):
    """ implements different operational functions
        depending on the value of p.

    Args:
        p (Integer):
            the value of option chosen by the user
            abc_user (Account): Instance of the Account class.
    """
    if p == 1:
        time.sleep(3)
        deposit(abc_user)
        ask_to_continue(abc_user)
    elif p == 2:
        time.sleep(3)
        withdraw(abc_user)
        ask_to_continue(abc_user)
    elif p == 3:
        time.sleep(3)
        display_account_details(abc_user)
    elif p == 4:
        time.sleep(3)
        transcript_receipt(abc_user)
        print(chr(27) + "[2J")
    elif p == 5:
        print(f"{Fore.GREEN}Thank you for using our services.\n")
        sys.exit()
    else:
        ask_to_continue(abc_user)


def controller():
    """ Controls the functions sequesnces.
    """
    new_user = welcome_message()
    if new_user.strip().lower()[0] == 'y':
        abc_user = validate__acc_num()
        if abc_user:
            if validate_pin(abc_user):
                p = show_menu()
                do_options(p, abc_user)
            else:
                print(chr(27) + "[2J")
                greet()
                controller()
        else:
            greet()
            controller()
    if new_user.strip().lower()[0] == 'n':
        create_user()
        controller()


def main():
    """ Run all functions of program. Controls the flow of the system """
    controller()


if __name__ == "__main__":
    greet()
    print("\n\n")
    main()
