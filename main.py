# main.py

from views.account_ui import AccountUI
from views.admin_ui import AdminUI

if __name__ == "__main__":
    account_ui = AccountUI()
    admin_ui = AdminUI()
    adminInfo = {"rohith": "123", "admin": "ad12"}
    while True:
        choice = int(input("Enter your choice \n1. Admin\n2. User\n3. Exit : "))
        if choice == 1:
            adminID = input("Enter admin ID : ")
            password = input("Enter password : ")
            if adminID in adminInfo and adminInfo[adminID] == password:
                admin_ui.start()
            else:
                print("Invalid admin ID or password.")
        elif choice == 2:
            account_ui.start()
        elif choice == 3:
            break
