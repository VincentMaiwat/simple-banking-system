from BankClient import BankClient 
from BankAccount import BankAccount
import time as t
import os
import mysql.connector  

client = BankClient(0,0,0,0,0,0) # Create instance
account = BankAccount(0,0,0) 
connection = mysql.connector.connect(host = 'localhost', database = 'db_banksystem', username ='root', password = '')
cur = connection.cursor()
delay = t.sleep


# New Client
def createClient():
    print('''
          PLBank
=============================
---- Register New CLient ----''')
    print("")
    client_id = client.getClientid()  # Get client ID
    checker = f"SELECT * FROM tbl_client WHERE client_id = {client_id}" # Check validity of ID
    cur.execute(checker)
    record = cur.fetchone()
    if record is None:
        password = client.getPassword() 
        
        name = client.getName()
        
        dob = client.getDob()
        
        city = client.getCity()
        
        contact = client.getContact()
        
        query = "INSERT INTO tbl_client (client_id, password, name, date_of_birth, city, contact_number) VALUES (%s,%s,%s,%s,%s,%s)"
        data = (client_id,password,name,dob,city,contact)
        cur.execute(query, data)
        connection.commit()
        print("=============================")
        print("\nProcessing application...")
        delay(2)
        print("\nCLIENT ACCOUNT HAS BEEN CREATED")
        input("\nEnter any key to continue: ")
        os.system('cls')
        management() 
    else:
        print("\nERROR: Client ID is already taken. Please try again.")
        delay(1.5)
        os.system('cls')
        createClient()

# List all clients
def listClients():
    print('''
          PLBank
=============================
------ PLBank CLients ------''')
    print("")
    query = "SELECT * FROM tbl_client"
    cur.execute(query)
    client_records = cur.fetchall() # Fetch all rows to check if there are existing records.
    
    if client_records: # If there are existing records, print the first column 
        for record in client_records:
            print("Client ID: ", record[0])
            delay(0.75)
    else:
        print("ERROR: No Client Found")
    print("=============================")
    input("\nEnter any key to go back: ")
    os.system('cls')
    clientManagement()
        
# Search client and print their data
def findClient():
    checker = f"SELECT * FROM tbl_client" 
    cur.execute(checker)
    record = cur.fetchall()
    
    if record:
        print('''
          PLBank
=============================
------ Client Details ------''')
        print("")
        # Access data from tbl_client
        client_id = client.getClientid()
        query = f"SELECT * FROM tbl_client where client_id = {client_id}"
        cur.execute(query)
        client_record = cur.fetchone()
        # Access data from tbl_account
        id_holder = client.clientid_holder() 
        query_acct = f"SELECT * FROM tbl_account WHERE client_id = {id_holder}"
        cur.execute(query_acct)
        acct_records = cur.fetchall()
        
        if client_record: # Display data from tbl_client if there are records
            
            print("\nID: ",client_record[0])
            delay(.5)
            print("Name: ", client_record[2])
            delay(.5)
            print("Date of Birth: ", client_record[3])
            delay(.5)
            print("City: ", client_record[4])
            delay(.5)
            contact = client_record[5]
            delay(.5)
            print("Contact Number: ", contact.zfill(11))
            
            if acct_records: # Display the savings accounts
                for record in acct_records:
                    print("Account ID: ", record[0])
            else:
                print("=============================")    
                print("\nERROR: No Savings Account Found.")
        else:
            print("=============================")     
            print("\nERROR: Client ID doesn't exist. Please try again.")
            delay(1.25)
            os.system('cls')
            findClient()
    else:
        print("=============================")    
        print("\nERROR: There are no registered clients.")   
    input("\nEnter any key to go back: ")
    os.system('cls')
    clientManagement()
   
# New savings account creation        
def newAccount():
    print('''
          PLBank
=============================
---- New Savings Account ----''')
    print("")
    account_id = account.getAccountID()
    checker = f"SELECT * FROM tbl_account WHERE account_id = {account_id}"
    cur.execute(checker)
    record = cur.fetchone()
    if record is None: # If the account_id is not yet taken
        pin = account.getPin()
        balance = account.getBalance()
        client_id = client.clientid_holder()
        
        query = f"INSERT INTO tbl_account (account_id, account_pin, balance, client_id) VALUES ('{account_id}','{pin}','{balance}','{client_id}')"
        cur.execute(query)
        connection.commit()
        print("=============================")
        print("\nCreating Savings Account...")
        delay(.75)
        print("\nNEW SAVINGS ACCOUNT HAS BEEN CREATED.")
        input("\nEnter any key to go back: ")
        os.system('cls')
        accManagement()
    else:
        print("\nERROR: Account ID is already taken.")
        delay(1.25)
        os.system('cls')
        newAccount()

# Display all savings account from a specific client
def listAccount():
    print('''
          PLBank
=============================
----- Savings Account/s -----''')
    print("")
    id_holder = client.clientid_holder()
    query = f"SELECT * FROM tbl_account WHERE client_id = {id_holder}"
    cur.execute(query)
    records = cur.fetchall()
    if records:
        for record in records:
            print("Account ID: ", record[0])
            delay(.75)
    else:
        print("\nERROR: No Account Found.")
    print("=============================")
    input("\nEnter any key to go back: ")
    os.system('cls')
    accManagement()

# Prints details of savings account
def checkBalance():
    id_holder = client.clientid_holder() 
    first_checker = f"SELECT * FROM tbl_account where client_id = {id_holder}" # Check for existing savings account of client
    cur.execute(first_checker)
    record = cur.fetchall()
    if record: # If there is existing savings account
        print('''
          PLBank
=============================
-- Savings Account Balance --''')
        print("")
        account_id = account.getAccountID()
        checker = f"SELECT * FROM tbl_account WHERE account_id = {account_id}"
        cur.execute(checker)
        records = cur.fetchone()
        if records: 
            client_record = records[3] # Get client_id on tbl_account
            if client_record == id_holder: # Checks if the current client_id is equal to the gotten id from tbl_account
                flag = True
                while flag:
                    current_pin = records[1]
                    try:
                        pin = int(input("Enter Pin: "))
                        if pin == current_pin:
                            flag = False
                            print("")
                            print("Account ID: ", records[0])
                            print("Balance: ₱", records[2])
                            print("")
                            print("=============================") 
                        else:
                            print("\nERROR: Incorrect Pin.")
                    except ValueError:
                        print("\nERROR: Enter a 4-digit pin")
            else:
                print("=============================") 
                print("\nERROR: Savings Account ID is already taken exist.")
                delay(1)
                os.system('cls')
                checkBalance()
        else:
            print("=============================") 
            print("\nERROR: Savings Account ID does not exist.") 
            delay(1)
            os.system('cls')
            checkBalance()
    else:
        print('''
          PLBank
=============================
-- Savings Account Balance --''')
        print("")
        print("\nERROR: No Savings Account Found.")
        print("\n=============================") 
    input("\nEnter any key to go back: ")
    os.system('cls')
    accManagement()

# Deposit to savings account
def depositAccount():
    print('''
          PLBank
=============================
------ Account Deposit ------''')
    print("")
    id_holder = client.clientid_holder() 
    first_checker = f"SELECT * FROM tbl_account where client_id = {id_holder}" # Checks if client_id exists
    cur.execute(first_checker)
    record = cur.fetchall()
    if record:
        account_id = account.getAccountID()
        checker = f"SELECT * FROM tbl_account WHERE account_id = {account_id}" # Checks if account_id exists
        cur.execute(checker)
        records = cur.fetchone()
        if records:
            client_record = records[3] # Sets client_record equal to the foreign key client id
            if client_record == id_holder:
                flag = True
                while flag:
                    current_pin = records[1]
                    try:
                        pin = int(input("\nEnter Pin: "))
                        if pin == current_pin:
                            flag = False
                            while True:
                                current_amount = records[2]
                                amount = float(input("Enter amount to deposit: ₱"))
                                final_amount = current_amount + amount
                                query = f"UPDATE tbl_account SET balance = {final_amount} WHERE account_id = {account_id}"
                                cur.execute(query)
                                connection.commit()
                                print("=============================") 
                                print("₱",amount," has been added to your balance.")
                                break                 
                        else:
                            print("\nERROR: Incorrect Pin.")
                    except ValueError:
                        print("\nERROR: Enter a 4-digit pin.")
            else:
                print("=============================") 
                print("\nERROR: Account doesn't exist.")
                delay(1.25)
                os.system('cls')
                depositAccount()
        else:
            print("=============================") 
            print("\nERROR: Savings Account with that ID doesn't exist.")
            delay(1.25)
            os.system('cls')
            depositAccount()
    else:
        print("\nERROR: No Savings Account Found.")
    
    input("\nEnter any key to go back: ")
    os.system('cls')
    accManagement()

# Withdraw from savings account    
def withdrawAccount():
    print('''
          PLBank
=============================
---- Account Withdrawal ----''')
    print("")
    id_holder = client.clientid_holder()
    first_checker = f"SELECT * FROM tbl_account where client_id = {id_holder}"
    cur.execute(first_checker)
    record = cur.fetchall()
    if record:
        account_id = account.getAccountID()
        checker = f"SELECT * FROM tbl_account WHERE account_id = {account_id}"
        cur.execute(checker)
        records = cur.fetchone()
        if records:
            client_record = records[3]
            if client_record == id_holder:
                flag = True
                while flag:
                    current_pin = records[1]
                    try:
                        pin = int(input("Enter Pin: "))
                        if pin == current_pin:
                            flag = False
                            while True:
                                current_amount = records[2]
                                print("\nCurrent Balance: ₱",current_amount)
                                amount = float(input("Enter amount to withdraw: ₱"))
                                if amount < current_amount:
                                    final_amount = current_amount -  amount
                                    query = f"UPDATE tbl_account SET balance = {final_amount} WHERE account_id = {account_id}"
                                    cur.execute(query)
                                    connection.commit()
                                    print("=============================") 
                                    print("\n₱",amount,"has been withdrawn successfully.")
                                    print("\nUpdated Balance: ₱",final_amount,"\n")
                                    delay(1.75)
                                    os.system('cls')
                                    accManagement()
                                elif amount == current_amount:
                                    choice = input("\nRemaining balance will be ₱0.00 and the savings account will be closed. Continue?[Y/N] ")
                                    if choice.upper() == 'Y':
                                        final_amount = current_amount -  amount
                                        query = f"UPDATE tbl_account SET balance = {final_amount} WHERE account_id = {account_id}"
                                        cur.execute(query)
                                        connection.commit()
                                        print("=============================") 
                                        print("\n₱",amount,"has been withdrawn successfully.")
                                        print("\nUpdated Balance: ₱",final_amount,"\n")
                                        query1 = f"DELETE FROM tbl_account WHERE account_id = {account_id}"
                                        cur.execute(query1)
                                        connection.commit()
                                        print("\nSavings Account has been closed.")
                                        input("\nEnter any key to go back: ")
                                        os.system('cls')
                                        accManagement()
                                    else:
                                        os.system('cls')
                                        withdrawAccount()
                                else:
                                    print("\nERROR: Insufficient funds.")
                        else:
                            print("\nERROR: Incorrect Pin.")
                    except ValueError:
                        print("\nEnter a 4-digit pin")
            else:
                print("=============================") 
                print("\nERROR: Account doesn't exist.")
                delay(1.25)
                os.system('cls')
                withdrawAccount()
        else:
            print("=============================") 
            print("\nERROR: Savings Account with that ID doesn't exist.")
            delay(1.25)
            os.system('cls')
            withdrawAccount()
    else:
        print("\nERROR: No Savings Account Found.")
        print("=============================")
            
        input("\nEnter any key to go back: ")
        os.system('cls')    
        accManagement()

# Checks if theres a savings account
def savingsChecker():
    id_holder = client.clientid_holder()
    first_checker = f"SELECT * FROM tbl_account where client_id = {id_holder}"
    cur.execute(first_checker)
    record = cur.fetchall()
    if record:
        return True
    else:
        return False

# Delete a savings account  
def deleteAccount():
    print('''
          PLBank
=============================
-- Delete Savings Account --''')
    print("")
    id_holder = client.clientid_holder()
    first_checker = f"SELECT * FROM tbl_account where client_id = {id_holder}"
    cur.execute(first_checker)
    record = cur.fetchall()
    if record:
        account_id = account.getAccountID()
        checker = f"SELECT * FROM tbl_account WHERE account_id = {account_id}"
        cur.execute(checker)
        records = cur.fetchone()
        if records:
            client_record = records[3]
            current_amount = records[2]
            if client_record == id_holder:
                if current_amount == 0.00:
                    query = f"DELETE FROM tbl_account WHERE account_id = {account_id}"
                    cur.execute(query)
                    connection.commit()
                    print("=============================")   
                    print("\nSavings Account Has Been Deleted.")
                else:
                    print("=============================")   
                    print("\nERROR: Cannot delete account with remaining balance.")
                    delay(1.25)
                    os.system('cls')
                    accManagement()
            else:
                print("=============================")   
                print("\nERROR: Account doesn't exist.")
                delay(1.25)
                os.system('cls')
                deleteAccount()
        else:
            print("=============================")   
            print("\nERROR: Account doesn't exist.")
            delay(1.25)
            os.system('cls')
            deleteAccount()
    else: 
        print("\nERROR: No Savings Account Found.")
        print("=============================")   

 
    input("\nEnter any key to go back: ")
    os.system('cls')
    accManagement()

# Client account deletion    
def deleteClient():
    print('''
          PLBank
=============================
--- Delete Client Account ---''')
    print("")
    id_holder = client.clientid_holder()
    checker = f"SELECT * FROM tbl_account WHERE client_id = {id_holder}"
    cur.execute(checker)
    record = cur.fetchone()
    cur.fetchall()
    if record is None:
        query = f"DELETE FROM tbl_client WHERE client_id = {id_holder}"
        cur.execute(query)
        connection.commit()
        print("=============================") 
        print("\nClient Account Has Been Deleted.")
        delay(2)
        main()
    else:
        print("\nERROR: Cannot delete client account with existing bank account.")
        delay(1.75)  
        os.system('cls') 
        clientManagement()
        

# Print details of current client account
def clientAccount():
    print('''
          PLBank
=============================
--- PLBank CLient Profile ---''')
    print("")
    id_holder = client.clientid_holder()
    checker = f"SELECT * FROM tbl_client WHERE client_id = {id_holder}"
    cur.execute(checker)
    record = cur.fetchone()
    print("Client ID: ", record[0])
    print("Client Pin: ", record[1])
    print("\nName: ", record[2])
    print("Date of Birth: ", record[3])
    print("City of Address: ", record[4])
    contact = record[5]
    print("Contact Number: ", contact.zfill(11))
    
    print("=============================") 
    input("\nEnter any key to go back: ")
    os.system('cls')
    clientManagement()

# Change client password
def changepass():
    print('''
          PLBank
=============================
------ Change Password ------''')
    print("")
    id_holder = client.clientid_holder()
    
    checker = f"SELECT * FROM tbl_client WHERE client_id = {id_holder}"
    cur.execute(checker)
    record = cur.fetchone()
    current_password = record[1]
    while True:
        current_password_checker = input("Current Password: ")
        if current_password_checker == current_password:
            new_password = client.getPassword()
            query = f"UPDATE tbl_client SET password = %s WHERE client_id = %s"
            values = (new_password, id_holder)
            cur.execute(query, values)
            connection.commit()
            print("=============================")    
            print("\nPassword is successfully changed.")
            break
        else:
            print("\nERROR: Incorrect Passwird ")
         
    input("\nEnter any key to go back: ")
    clientManagement()
    
# For returning Clients
def oldClient():
    print('''
          PLBank
=============================
------- Client LogIn --------''')
    print("")
    print("Enter 00 to Cancel")
    client_id = client.getClientid()
    
    if client_id == 00:
        main()
        
    checker = f"SELECT * FROM tbl_client WHERE client_id = {client_id}"
    cur.execute(checker)
    record  = cur.fetchone()
    if record:
        client_password = record[1]
        while True:
            password = input("Enter Password: ")
            if client_password == password:
                print("=============================") 
                print("\nLogging you in...")
                delay(1.5)
                os.system('cls')
                management()
                return
            else:
                print("\nERROR: Incorrect Password\n")
    else:
        print("=============================") 
        print("\nERROR: Client ID doesn't exists.")
        delay(1.2)
        os.system('cls')
        oldClient() 

# List savings accounts from all clients       
'''def listallAccount():
    query = f"SELECT * FROM tbl_account"
    cur.execute(query)
    records = cur.fetchall()
    if records:
        for record in records:
            print("Account ID: ", record[0])
    else:
        print("No Account Found.")

    input("Enter any key to continue: ")
    os.system('cls')
    accManagement()'''
    
# Prints specific savings account details
def listAccountDetails():
    print('''
          PLBank
=============================
------ Savings Account ------''')
    print("")
    checker = "SELECT * FROM tbl_account"
    cur.execute(checker)
    record = cur.fetchall()
    if record:
        client_id = client.clientid_holder()
        account_id = account.getAccountID()
        query = f"Select * FROM tbl_account WHERE account_id = {account_id}"
        cur.execute(query)
        records = cur.fetchone()

        if records:
            query1 = f"Select * FROM tbl_client WHERE client_id = {client_id}"
            cur.execute(query1)
            record_client = cur.fetchone()
            print("Client Name : ", record_client [2])
            print("\nAccount ID: ", records[0])
            print("Account Pin: ", records[1])
            print("Balance: ₱", records[2])
            print("\n=============================") 
        else:
            print("ERROR: Account ID Doesn't exists.")
    else:
        print("ERROR: No Savings Account Found.")
    
    input("\nEnter any key to go back: ")
    os.system('cls')
    accManagement()

# Menu for client options 
def clientManagement():
    
    while True:
        try:
            print('''
          PLBank
=============================
-- Client Management Menu --
          
[1] Register a New Client
[2] List All Client
[3] Find Client
[4] Delete Client Account
[5] Client Profile
[6] Change Password
[7] Back 
          
=============================''')
            choice = int(input("\nWhat would you like to do? "))
            if 1 <= choice <= 7:
                break
            else:
                print("\nERROR: Please enter a number from 1-7.")
        except ValueError:
                print("\nERROR: Enter a numerical value.")
    
    if choice == 1:
        os.system('cls')
        createClient()
    if choice == 2:
        os.system('cls')
        listClients()
    elif choice == 3:
        os.system('cls')
        findClient()
    elif choice == 4:
        os.system('cls')
        deleteClient()
    elif choice == 5:
        os.system('cls')
        clientAccount()
    elif choice == 6:
        os.system('cls')
        changepass()
    elif choice == 7:
        os.system('cls')
        management()       

# Menu for savings account options        
def accManagement():
    print('''
          PLBank
=============================
--- Savings Account Menu ---         
[1] Open New Savings Account
[2] List All Savings Accounts
[3] Find Savings Account
[4] Check Balance
[5] Deposit to Account
[6] Withdraw to Account
[7] Delete Account
[8] Back
=============================''')
    while True:
        try:
            choice = int(input("\nWhat would you like to do? "))
            if 1 <= choice <= 8:
                break
            else:
                print("\nERROR: Please enter a number from 1-8.")
        except ValueError:
                print("\nERROR: Enter a numerical value.")
                
    if choice == 1:
        os.system('cls')
        newAccount()
    elif choice == 2:
        os.system('cls')
        listAccount()
    elif choice == 3:
        os.system('cls')
        listAccountDetails()
    elif choice == 4:
        os.system('cls')
        checkBalance()
    elif choice == 5:
        os.system('cls')
        depositAccount()
    elif choice == 6:
        os.system('cls')
        withdrawAccount()
    elif choice == 7:
        os.system('cls')
        deleteAccount()
    elif choice == 8:
        os.system('cls')
        management()

# Main Menu
def management():
    id_holder = client.clientid_holder()
    checker = f"SELECT * FROM tbl_client WHERE client_id = {id_holder}"
    cur.execute(checker)
    record = cur.fetchone()
    print("\nGlad to have you back, ",record[2],"!" )
    print('''==========================
------ PLBank Menu -------
[1] Account Management
[2] Client Management
[3] Log Out
==========================''')
    while True:
        try:
            choice = int(input("\nWhat would you like to do? "))
            if 1 <= choice <= 3:
                break
            else:
                print("\nERROR: Please eneter a number from 1-3.")
        except ValueError:
                print("\nERROR: Enter a numerical value.")
                
    if choice == 1:
        os.system('cls')
        accManagement()
    elif choice == 2:
        os.system('cls')
        clientManagement()
    elif choice == 3:
        if savingsChecker():
            print("Thank you for trusting PLBank!")
            delay(1.5)
            os.system('cls')
            main()
        else:
            while True:
                print("\nA Client Account couldn't exist without a Savings Account.")  
                confirm = input("\nClient Account will be deleted. Continue? [Y/N]")
                if confirm.upper() == 'Y':
                    deleteClient()
                    main()
                elif confirm.upper() == 'N':
                    os.system('cls')
                    management()
                else:
                    print ("\nERROR: Invalid Input. Try again.")

def main():
        print('''
===============================
------ Welcome to PLBank ------
              
[1] Register as New Client
[2] Login to existing Account
[3] Quit
===============================''')
        while True:
            try:
                choice = int(input("\nWhat would you like to do? "))
                if 1 <= choice <= 3:
                    break
                else:
                    print("\nERROR: Option out of scope.")
            except ValueError:
                print("\nEnter a numeric value")
            
        if choice == 1:
            os.system('cls')
            createClient()
        elif choice == 2:
            os.system('cls')
            oldClient()
        elif choice == 3:
            print("Exiting program...")
            delay(1.5)
            exit(0)
       
main()