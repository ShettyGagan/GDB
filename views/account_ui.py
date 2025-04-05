# account_ui.py

from datetime import datetime
from services.account_manager import AccountManager
from services.transaction_manager import TransactionManager
from repositories.account_repository import AccountRepository
from services.account_privileges_manager import AccountPrivilegesManager
from exceptions.exceptions import AccountDoesNotExistException
from exceptions.exceptions import AccountAlreadyActiveException
from exceptions.exceptions import AccountAlreadyDeactivatedException

class AccountUI:
    def start(self):
        while True:
            print('\nWelcome to Global Digital Bank')
            print('\nSelect an option:')
            print('1. Open Account')
            print('2. Close Account')
            print('3. Withdraw Funds')
            print('4. Deposit Funds')
            print('5. Transfer Funds')
            print("6. View Account by Type")
            print("7. View Account by ID")
            print("8. View All Accounts")
            print('9. Activate account')
            print('10. Deactivate account')
            print('11. Edit account')
            print('12. Check Transfer Limit')
            print('13. View all Transaction Logs')
            print('14. View Transaction by date')
            print('15. View Transaction by type')
            print('16. View withdrawal count by date')
            print('17. Back to Main Menu')

            choice = int(input('Enter your choice: '))

            if choice == 1:
                self.open_account()
            elif choice == 2:
                self.close_account()
            elif choice == 3:
                self.withdraw_funds()
            elif choice == 4:
                self.deposit_funds()
            elif choice == 5:
                self.transfer_funds()
            elif choice == 6:
                self.view_accounts_by_type()
            elif choice == 7:
                self.view_account_by_id()
            elif choice == 8:
                self.view_all_accounts()
            elif choice== 9:
                self.activate_account()
            elif choice== 10:
                self.deactivate_account()
            elif choice== 11:
                self.edit_account()
            elif choice == 12:
                self.check_transfer_limit()
            elif choice == 13:
                self.view_all_transactions()
            elif choice == 14:
                self.view_transactions_by_date()
            elif choice == 15:
                self.view_transactions_by_type()
            elif choice == 16:
                self.count_of_withdrawals_by_date()
            elif choice == 17:
                return
            else:
                print('Invalid choice. Please try again')



    def open_account(self):
        account_type = input('Enter account type (savings/current): ').strip().lower()
        name = input('Enter your name: ')
        amount = float(input('Enter initial deposit amount: '))
        pin_number = int(input('Enter your pin number: '))
        privilege = input('Enter account privilege (PREMIUM/GOLD/SILVER): ').strip().upper()

        if account_type == 'savings':
            date_of_birth = input('Enter your date of birth (YYYY-MM-DD): ')
            gender = input('Enter your gender (M/F): ')
            account = AccountManager().open_account(account_type, name=name, balance=amount,
            date_of_birth=date_of_birth, gender=gender, pin_number=pin_number, privilege=privilege)

        elif account_type == 'current':
            registration_number = input('Enter your registration number: ')
            website_url = input('Enter your website URL: ')
            account = AccountManager().open_account(account_type, name=name, balance=amount, 
            registration_number=registration_number, website_url=website_url, pin_number=pin_number,
            privilege=privilege)

        else:
            print('Invalid account type. Please try again')
            return

        print(account_type.capitalize(), 'Account opened successfully. Account Number: ',account.account_number)

 
    def close_account(self):
        account_number = int(input('Enter your account number: '))
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)

        if account:
            try:
                AccountManager().close_account(account)
                print('Account closed successfully')
            except Exception as e:
                print("Error: ", e)
        else:
            print('Account Not Found. Please try again')

    def withdraw_funds(self):
        account_number = int(input('Enter your account number: '))
        amount = float(input('Enter amount to withdraw: '))
        pin_number = int(input('Enter your pin number: '))
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)

        if account:
            try:
                AccountManager().withdraw(account, amount, pin_number)
                print('Amount withdrawn successfully')
            except Exception as e:
                print('Error: ', e)
        else:
            print('Account Not Found. Please try again')

    def deposit_funds(self):
        account_number = int(input('Enter your account number: '))
        amount = float(input('Enter amount to deposit: '))
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)

        if account:
            try:
                AccountManager().deposit(account, amount)
                print('Amount deposited successfully')
            except Exception as e:
                print('Error: ', e)
        else:
            print('Account Not Found. Please try again')

    def transfer_funds(self):
        from_account_number = int(input('Enter your account number: '))
        to_account_number = int(input('Enter recipient account number: '))
        amount = float(input('Enter amount to transfer: '))
        pin_number = int(input('Enter your pin number: '))

        from_account = next((acc for acc in AccountRepository.accounts if acc.account_number == from_account_number), None)
        to_account = next((acc for acc in AccountRepository.accounts if acc.account_number == to_account_number), None)

        if from_account and to_account:
            try:
                AccountManager().transfer(from_account, to_account, amount, pin_number)
                print('Amount transferred successfully')
            except Exception as e:
                print('Error: ', e)
        else:
            print('One or Both Account(s) Not Found. Please try again')

        
    def check_transfer_limit(self):
        account_number = int(input('Enter your account number: '))
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)
        if account:
            try:
                print("Your transfer limit per day is", AccountPrivilegesManager().get_transfer_limit(account.privilege))
            except Exception as e:
                print('Error: ', e)
        else:
            print('Account Not Found. Please try again')

    def view_all_transactions(self):
        TransactionManager.view_transaction_logs()

    def view_transactions_by_date(self):
        account_number = int(input('Enter your account number: '))
        start_date_str = input('Enter start date(YYYY-MM-DD): ')
        end_date_str = input('Enter end date(YYYY-MM-DD: ')
        start_date = datetime.strptime(start_date_str,"%Y-%m-%d")
        end_date = datetime.strptime(end_date_str,"%Y-%m-%d")
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)
        if account:
            try:
                TransactionManager.view_transactions_by_date(account_number,start_date,end_date)
            except Exception as e:
                print('Error: ', e)
        else:
            print('\nAccount Not Found. Please try again')

    def view_transactions_by_type(self):
        account_number = int(input('Enter your account number: '))
        transaction_type = input("Enter transaction type (withdraw,deposit,transfer): ").lower()
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)
        
        if account:
            try:
                TransactionManager.view_transactions_by_type(account_number,transaction_type)
            except Exception as e:
                print('Error: ', e)
        else:
            print('\nAccount Not Found. Please try again')

    def count_of_withdrawals_by_date(self):
        target_date_str=input('Enter the date to view total withdrawals (YYYY-MM-DD): ')
        target_date=datetime.strptime(target_date_str,"%Y-%m-%d")

        try:
            TransactionManager.count_of_withdrawals_by_date(target_date)
        except Exception as e:
                print('Error: ', e)

    def view_accounts_by_type(self):
        account_type = input("Enter account type (savings/current): ").strip().lower()
        AccountManager().view_accounts_by_type(account_type)

    def view_account_by_id(self):
        account_number = int(input("Enter account number: "))
        AccountManager().view_account_by_id(account_number)

    def view_all_accounts(self):
        AccountManager().view_all_accounts()
    
    def activate_account(self):
        try:
            account_number = int(input("Enter the account number :"))
            account = next((acc for acc in AccountRepository.accounts if acc.account_number==account_number),None)
            if account is None:
                raise AccountDoesNotExistException('Account does not exist')
            AccountManager().activate_account(account)
        except AccountDoesNotExistException as e:
            print("Error :",e)
        except AccountAlreadyActiveException as e:
            print("Error :",e)


    def deactivate_account(self):
        try:
            account_number = int(input("Enter the account number :"))
            account = next((acc for acc in AccountRepository.accounts if acc.account_number==account_number),None)
            if account is None:
                raise AccountDoesNotExistException('Account does not exist')
            AccountManager().deactivate_account(account)
        except AccountDoesNotExistException as e:
            print("Error :",e)
        except AccountAlreadyDeactivatedException as e:
            print("Error :",e)


    def edit_account(self):
        try:
            account_number = int(input("Enter the account number :"))
            existing_pin=int(input("Enter the pin number :"))
            account = next((acc for acc in AccountRepository.accounts if acc.account_number==account_number),None)
            if not account:
                raise AccountDoesNotExistException('Account does not exist')
            AccountManager().validate_pin(account, existing_pin)
            AccountManager().edit_account(account)

        except Exception as e:
            print("Error :",e)