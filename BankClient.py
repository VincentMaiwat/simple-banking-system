class BankClient:
    def __init__(self, client_id, password, name, dob, city, contact):
        self.client_id = client_id
        self.password = password
        self.name = name
        self.dob = dob
        self.city = city
        self.contact = contact

    def getClientid(self):
        while True: 
            try:
                self.client_id = int(input("Enter Client ID: "))
            except ValueError: 
                print("\nERROR: Only numerical values are allowed.\n")
            else:
                return self.client_id
    
    def getPassword(self):
        while True:
            self.password = str(input("Set Password: ")).strip()
            if not self.password:
                print("\nERROR: Password can't be empty.\n")
            else:
                return self.password 
        
    def getName(self):
        while True:
            self.name = str(input("Enter Name: ")).strip()
            if not self.name:
                print("\nERROR: Name can't be empty.\n")
            else:
                return self.name 
    
    def getDob(self):
        self.dob = input("Enter Date of Birth (YYYY-MM-DD): ")
        return self.dob 
    
    def getCity(self):
        while True:
            self.city = str(input("Enter City of Address: ")).strip()
            if not self.city:
                print("\nERROR: City of Address can't be empty.\n")
            else:
                return self.city 
            
    def getContact(self):
        while True:
            try:  
                self.contact = int(input("Enter Contact: "))
                if len(str(self.contact)) == 10:
                    return self.contact
                elif len(str(self.contact)) > 10 or len(str(self.contact)) < 10:
                    print("\nERROR: Enter an 11-digit contact number.")  
                else:
                    print("\nERROR: Invalid Input.")
            except ValueError:
                print("\nERROR: Please enter a numerical value.\n")
       
    def clientid_holder(self): 
        return self.client_id
    
    def getIDNumber(self):
        self.cursor.execute('SELECT idNumber FROM BankClient')
        allIDs = [record[0] for record in self.cursor.fetchall()]
        return allIDs

    def getAccount(self):
        self.cursor.execute("SELECT accountID FROM BankAccount WHERE clientID = %s", (self.idNumber,))
        Accounts = [record[0] for record in self.cursor.fetchall()]
        return Accounts

    def printDetails(self):
        self.self.cursor.execute("SELECT * FROM BankClient WHERE clientID = %s", (self.idNumber,))
        Values = self.cursor.fetchone()
        if Values:
            print("Client ID: ", Values[0])
            print("Name: ", Values[2])
            print("BirthDate: ", Values[3])
            print("ContactNo: ", Values[4])
            self.cursor.execute("SELECT accountID FROM BankAccount WHERE clientID = %s", (self.idNumber,))
            Accounts = [record[0] for record in self.cursor.fetchall()]
            print("Account Details: ", Accounts)
