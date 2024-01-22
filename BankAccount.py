class BankAccount:
    def __init__(self, account_id, pin, balance): 
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        
    def getAccountID(self):
        while True:
            try:
                self.account_id = int(input("Enter Account ID: "))
                return self.account_id
            except ValueError:
                print("\nERROR: Only numerical values are allowed.\n")
                
    def getBalance(self):
        while True:
            try:
                self.balance = float(input("Enter Balance: ₱"))
                if self.balance != 0:
                    return self.balance
                else:
                    print("\nOpening balance can not be ₱0.00\n")
            except ValueError:
                print("\nERROR: Please enter a numerical value.\n")

    def getPin(self):
        while True:
            try: 
                self.pin = int(input("Set 4-digit pin: "))
                if len(str(self.pin)) == 4:
                    return self.pin
                elif len(str(self.pin)) > 4 or len(str(self.pin)) < 4 :
                    print("\nERROR: Please enter a 4-digit pin\n")
                else:
                    print("\nERROR: Invalid Input.")
            except ValueError:
                print("\nERROR: Please enter a numeric value.\n")

    def getIDNumber(self):
        self.cursor.execute(f'SELECT accountID FROM BankAccount WHERE clientID = {self.clientID}')
        allAccounts = [account[0] for account in self.cursor.fetchall()]
        return allAccounts

    def printDetails(self):
        self.cursor.execute("SELECT Balance FROM BankAccount WHERE accountID = %s", (self.accountID,))
        balance = self.cursor.fetchone()
        if balance:
            print("ID Number:", self.accountID)
            print("Current Balance:", balance[0])
        self.close_connection()

    def deposit(self):
        accountID = int(input('Enter your Account ID: '))
        Amount = float(input('Enter amount to Deposit: '))
        if Amount > 0:
            self.cursor.execute(f"SELECT Balance FROM BankAccount WHERE accountID = {accountID}")
            currentBalance = self.cursor.fetchone()
            if currentBalance:
                currentBalance = currentBalance[0]
                newBalance = currentBalance + Amount
                self.cursor.execute(f"UPDATE BankAccount SET Balance = {newBalance} WHERE accountID = {accountID}")
                self.dbconn.commit()
                return True
        return False

    def withdraw(self):
        Amount = float(input('Enter amount to Withdraw: '))
        currentBalance = self.getBalance()
        if currentBalance and Amount > 0 and Amount <= currentBalance:
            newBalance = currentBalance - Amount
            self.cursor.execute("UPDATE BankAccount SET Balance = %s WHERE accountID = %s", (newBalance, self.accountID))
            self.dbconn.commit()
            self.close_connection()
            return True
        self.close_connection()
        return False

        

        