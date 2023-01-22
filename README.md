# Abc ATM - Banking System
- [INTRODUCTION](#introduction)
- [USER EXPERIENCE UX](#user-experience-ux)
- [SCOPE](#scope)
- [STRUCTURE](#structure)
- [SCOPE](#scope)
- [FLOWCHART](#flowchart)
- [FEATURES](#features)
  + [EXISTING FEATURES](#existing-features)
  + [FUTURE FEATURES](#future-features)
- [BUGS OR ERRORS](#bugs-or-errors)
- [TESTING](#testing)
- [DEPLOYMENT](#deployment)
- [CREDITS](#credits)
- [ACKNOWLEDGEMENTS](#acknowledgements)


## INTRODUCTION
The Abc ATM Banking System is a fictional ATM that combines the partial functionality of a bank and an ATM. The system simulates the creation of a bank account, validates a customer or client account number with a four digit pin and enables logged in customer to deposit or withdraw money. It also displays customer account details and transaction information on a table.

[The live project can be viewed here](https://natty-congo.herokuapp.com/)


## USER EXPERIENCE UX
### USER STORIES
As a developer I want to create:
* a model of an ATM that will ease clients from the hassle of creating a bank account in addition to its normal functions.

As a general user I want to:
1. Easily navigate through the application
2. Be able to understand the purpose of the application
3. See the correctness of the validation of my input values

During this phase of the project design test repositories were created to try out visuals and initial features before establishing the final respository.

## SCOPE
For the implementation of the ATM system I have planned the following features:
- Data from spreadsheet that contains users account and transactions to be displayed to user in tables.
- Account creation starts from the begining of the program, if user has no account.
- User account will be validated, if correct an option screen will be displayed to user otherwise user will be refered back to create an accoount.
- The deposit option enables the user to add money to his/her account on passing the validation of the input data. The value of the amount, status and date time are inserted to the transaction spreadsheet table.
- The withdraw option like the deposit option enables user to remove money from his/her account if the amount input is valid. The amount requested by user, status and date time are inserted to the transactions spreadsheet table.
- The program displays warnings in all stages if input values are not given in the correct format.
- On demand a transaction table is displayed to the account holder if any, showing all his/her transactions with date time, amount and status with reasons if status is failure.

## STRUCTURE


### FLOWCHART
![alt-text](assets/images/readme/flowchart.png)














  