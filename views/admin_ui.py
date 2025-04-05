from services.account_privileges_manager import AccountPrivilegesManager
from models.user import UserManager
from repositories.account_repository import AccountRepository


class AdminUI:
    def start(self):
        while True:
            print(
                """\t\t\tWelcome to GDB Admin Controller
Select an option:
1. Set Transfer Limit
2. Add User
3. Edit User
4. View User
5. Activate User
6. Inactivate User
7. View all Users
8. Back to Main Menu
"""
            )

            choice = int(input("Enter your choice: "))

            if choice == 1:
                self.set_transfer_limit()
            elif choice == 2:
                self.add_user()
            elif choice == 3:
                self.edit_user()
            elif choice == 4:
                self.view_user()
            elif choice == 5: 
                self.activate_user_id()
            elif choice == 6:
                self.inactivate_user_id()
            elif choice == 7:
                self.view_all_user()
            elif choice == 8:
                return
            else:
                print("Invalid choice. Please try again.")

    def set_transfer_limit(self):
        new_limit = int(input("Enter your new Limit :"))
        privilege = (
            input("Enter valid privilege (PREMIUM/GOLD/SILVER): ").strip().upper()
        )
        AccountPrivilegesManager().set_daily_transfer_limit(privilege, new_limit)

    def add_user(self):
        try:
            user_manager = UserManager()
            user_name = input("Enter the user name: ")
            user_id = input("Enter the user_id: ")
            user = user_manager.create_user(user_name, user_id)
            AccountRepository.users.append(user)
        except Exception as e:
            print(f"Error: {e}")

    def edit_user(self):
        pre_name = input("Enter previous username: ")
        pre_password = input("Enter previous User Id: ")
        print("Enter the updated info ")
        name = input("Enter the updated name: ")
        password = input("Enter updated password : ")
        try:
            for user in AccountRepository.users:
                if user.name == pre_name and user.check_password(pre_password):
                    user.name = name
                    user.password_hash = user._hash_password(password)
                    print("User info updated successfully")
        except:
            print("User not found")

    def view_user(self):
        account_number = int(input("Enter your Account no : "))
        pin_number = int(input("Enter your pin number: "))
        try:
            iter = 0
            for account in AccountRepository.accounts:
                iter = 1
                if (
                    account.account_number == account_number
                    and account.pin_number == pin_number
                ):
                    print("-" * 25)
                    print("Account Number: ", account.account_number)
                    print("User Name:      ", account.name)
                    # print("Account type:   ", account.account_type)
                    print("Account Balance:", account.balance)
                    print("-" * 25)
                else:
                    print("Incorrect Account number or Pin number")
            if iter == 0:
                print("\nAccount not found")
            iter = 0
        except Exception as e:
            print("Error occured", e)


    def activate_user_id(self):
        user_id = int(input("Enter the user ID to activate: "))
        try:
            UserManager().activate_user(user_id)
        except Exception as e:
            print("Error: ", e)
    
    def inactivate_user_id(self):
        user_id = int(input("Enter the user ID to Inactivate: "))
        try:
            UserManager().inactivate_user(user_id)
        except Exception as e:
            print("Error: ", e)
     
    def view_all_user(self):
        UserManager.view_all_users()      