import datetime
import sys
import time
from random import randint
from accounts import Account as account
from texttable import Texttable
# from rich.table import Table
# from rich.console import Console
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
        time.sleep(0.05)


def ask_to_continue():
    """ Asks user to continue or exit system. """
    while True:
            choice = input("Do you wish to continue or exit?(C/E): ")
            if not choice == "" and choice.strip().lower()[0] == 'c':
                controller()
                break
            elif not choice == "" and choice.strip().lower()[0] == 'e':
                sys.exit()
                break
            else:
                print("Enter only continue or exit!!!\n")


def show_menu():
    """ Displays the menu to a user """
    word_wrap(f"""{Fore.CYAN}
        |====================================================|
        |                                                    |
        |        WELCOME TO ABC ATM BANKING SYSTEM           |
        |                                                    |
        |   Please choose one of the following options:      |
        |                                                    |
        |        1. ENTER DEPOSIT TO ACCOUNT                 |
        |        2. WITHDRAW FROM ACCOUNT                    |
        |        3. SHOW ACCOUNT DETAILS                     |
        |        4. SHOW TRANSACTIONS                        |
        |        5. EXIT                                     | 
        |                                                    |    
        |====================================================|""")
    print("\n\n")
    option = int(input("\033[1m" +f"""{Fore.WHITE}    Enter option(1-5): """))
    print("\n\n")
    return option


def welcome_message():
    """ Asks user if user is a customer or not """
    while True:
        try:
            abc_user = input("\033[1m" + f"""\n{Fore.WHITE}    Do you have an account with us ?(YES/NO):  """)
        except EOFError:
            break
        if abc_user.strip().lower()[0] == 'y':
            break  
        elif abc_user.strip().lower()[0] == 'n':
            break
        else:
            print("\n")
            print(f"""{Fore.RED}    You are required to answer only: yes or no.\n\n""")

    return abc_user


def create_user():
    """
    Collects user input, validate input values and creates an account for user.
    Returns an account object.
    """
    time.sleep(2)
    print("\n\n")
    word_wrap(f"""    ============= ACCOUNT CREATION =============
    |===========================================|\n\n""")
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
    print("\n\n")
    word_wrap(f"""    ============== ACCOUNT VALIDATION ==============\n\n""")
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
        print(f"""{Fore.GREEN}    Thank you for using our services.\n\n""")
        ask_to_continue()
        time.sleep(2)
        return False
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
    print("\n\n")
    word_wrap(f"""{Fore.GREEN}    =========== PIN VALIDATION ============\n\n""")
    tries = 0
    while tries < 3:
        tries += 1
        code = input(f"""{Fore.GREEN}    Enter four digit pin: """).strip()
        print("\n")
        if code == account_holder.get_pin():
            word_wrap(f"""    valid PIN, you have successfully logged in.\n\n""")
            break
        elif code != account_holder.get_pin():
            print(f"{Fore.RED}    !Pin code is not correct - {code}.\n")  
    else:
        print(f"""{Fore.YELLOW}   You have exceeded trial limit, please contact bank officials by phone.\n\n""")
        print(f"""{Fore.GREEN}    Thank you for using our services.\n""")
        return False
    return True


def deposit(account):
    """ Deposit amount of money to own account,
        updates the transaction worksheet and terminates
        after 3 unsuccessfull attempts.
     """
    transact = []
    trans_id = "D"+str(randint(0, 101))+str(int(datetime.datetime.now().timestamp()))
    transact.append(trans_id)
    transact.append(account._acc_num)
    transact.append(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    tries = 0
    while tries < 3:
        tries += 1
        amount = input(f"""{Fore.GREEN}    Please enter how much money you want to lodge:$ """)
        print("\n")
        word_wrap(f"""   Checking the input amount ...\n""")
        time.sleep(2)
        if not amount.isnumeric():
            print(f"""{Fore.RED}    Only figures of amount allowed - {amount}\n""")
            status = False
            new_balance = float(account.get_balance())
        else:
            status = True
            new_balance = float(account.get_balance()) + float(amount)
            break
    else:
        print(f"""{Fore.YELLOW}    Sorry you've reached your trial limit.\n""")
        print(f"""    Consult bank officials by phone for further instructions.\n""")
    if not amount.isnumeric():
        new_balance = float(account.get_balance())
    else:
        new_balance = float(account.get_balance()) + float(amount)
    account.set_balance(new_balance)
    print(f"""{Fore.WHITE}    Your current balance is {str(account.get_balance())} \n""")
    card_holder = SHEET.worksheet('accounts').find(account._acc_num)
    SHEET.worksheet('accounts').update_cell(card_holder.row, 5, str(int(account.get_balance())))
    if status:
        transact.append('SUCCESS')
        print(f"""{Fore.GREEN}    Thank you {account.first_name} {account.last_name} for your deposit.\n""")
    else:
        transact.append('FAILURE')       
    transact.append(amount)
    SHEET.worksheet('transaction').append_row(transact)
    return status


def withdraw(account):
    """ withdraws amount of money from account
        if availabe or shows corresponding error,
        and updates the transaction worksheet, returns status.
    """
    transact = []
    trans_id = "W"+str(randint(0, 101))+str(int(datetime.datetime.now().timestamp()))
    transact.append(trans_id)
    transact.append(account._acc_num)
    transact.append(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    try:
        amount = input(f"{Fore.GREEN}    How much money do you want to withdraw:$ ")
        print("\n")
        if not amount.isnumeric():
            status = False
            raise Exception(f"Only figures of amount allowed {amount}")
        if float(account.get_balance()) < float(amount):
            status = False
            raise Exception(f"Sorry insufficient funds: {account.get_balance()}")
        word_wrap(f"""    You are good to go! Thank you: \n""")
        account.set_balance(float(account.get_balance()) - float(amount))
        print(f"""    Your current balance is : {str(account.get_balance())}\n""")
        card_holder = SHEET.worksheet('accounts').find(account._acc_num)
        bal = str(int(account.get_balance()))
        SHEET.worksheet('accounts').update_cell(card_holder.row, 5, bal)
        status = True
    except Exception as e:
        print(f"""{Fore.RED}    {e}, {Fore.GREEN}perhaps you need  a credit.\n""")
        print(f"""{Fore.GREEN}    Call the bank and talk things over with them.\n""")
        status = False
    if status:
        transact.append('SUCCESS')
    else:
        transact.append('FAILURE')
        # transact.append(amount)
    camount = "-" + str(amount)       
    transact.append(camount)
    SHEET.worksheet('transaction').append_row(transact)
    return status
    


def display_account_details(account):
    """ Displays account details of a logged in user."""
    account_holders = SHEET.worksheet('accounts').get_all_values()[1:]
    current_user = [holder for holder in account_holders if account._acc_num == holder[0]]
    table = Texttable()
    table.header( ['Account Number','First Name', 'Last Name', 'PIN','Balance'])
    for user in current_user:
        table.add_row(user)
    print(table.draw())
    print("\n\n")
    ask_to_continue()


def transcript_receipt(account):
    """ Displays all transactions of a user if any """
    transactions = SHEET.worksheet('transaction').get_all_values()[1:]
    user_transacts = [transact for transact in transactions if account._acc_num == transact[1]]
    if len(user_transacts) == 0:
        word_wrap(f"""{Fore.CYAN}    You've no transactions done yet\n""")
        ask_to_continue()
    else:
        table = Texttable()
        table.header(['TransactionId', 'AccountId', 'Date & Time', 'Status', 'Amount'])
        for transcript in user_transacts:
            if transcript[4][0] == '-' and transcript[4][1:].isnumeric() and transcript[3] == 'FAILURE':
                transcript[4] += ' Insufficient fund.'
            elif not transcript[4][-1].isnumeric():
                transcript[4] += ' Invalid input'
            table.add_row(transcript)
        print(table.draw())
        print("\n\n")
        ask_to_continue()



def controller():
    """ Controls the functions sequesnces"""
    new_user = welcome_message()
    if new_user.strip().lower()[0] == 'y':
        # validate user
        abc_user = validate__acc_num()
        if abc_user:
            if validate_pin(abc_user):
                p = show_menu()
                if p == 1:
                    time.sleep(3)
                    deposit(abc_user)
                elif p == 2:
                    time.sleep(3)
                    withdraw(abc_user)
                elif p == 3:
                    time.sleep(3)
                    display_account_details(abc_user)
                elif p == 4:
                    time.sleep(3)
                    transcript_receipt(abc_user)
                elif p == 5:
                    sys.exit()
                else:
                    print(f"Unknown option, please follow the instructions.\n")
                    ask_to_continue() 
    elif new_user.strip().lower()[0] == 'n':
        create_user()
        show_menu()
        controller()
    else:
        print(f"Invalid iput to a yes/no question!\n")



def main():
    """ Run all functions of program. Controls the flow of the system """
    controller()

    
    
   

# p = show_menu()
# print(p)
# user = validate__acc_num()
# validate_pin(user)
# withdraw(user)
# # display_account_details(user)
# transcript_receipt(user)

word_wrap(f"""{Fore.CYAN}
        =================================================
        |             WELCOME TO ABC ATM                 |
        ++++++++++++++++++++++++++++++++++++++++++++++++++""")
print("\n\n")
main()