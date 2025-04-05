from models.savings import Savings
from models.current import Current
from repositories.account_repository import AccountRepository
from exceptions.exceptions import AccountNotActiveException
from exceptions.exceptions import InsufficientFundsException
from exceptions.exceptions import InvalidPinException
from exceptions.exceptions import TransferLimitExceededException
from services.transaction_manager import TransactionManager
from services.account_privileges_manager import AccountPrivilegesManager
from exceptions.exceptions import AccountAlreadyActiveException
from exceptions.exceptions import AccountAlreadyDeactivatedException

# Class to manage accounts
class AccountManager:
    def open_account(self, account_type, **kwargs):
        # Opens a new account of the specified type (savings or current)
        if account_type == 'savings':
            new_account = Savings(**kwargs)
        elif account_type == 'current':
            new_account = Current(**kwargs)
        else:
            # Raise an error for invalid account type
            raise ValueError('Invalid account type')

        # Save the new account in the repository
        AccountRepository.save_account(new_account)
        return new_account

    def check_account_active(self, account):
        # Checks if the account is active
        if not account.is_active:
            raise AccountNotActiveException('Account is not Active')

    def validate_pin(self, account, pin_number):
        # Validates the PIN for the given account
        if account.pin_number != pin_number:
            raise InvalidPinException('Invalid Pin')

    def withdraw(self, account, amount, pin_number):
        # Handles withdrawal from an account
        self.check_account_active(account)
        self.validate_pin(account, pin_number)

        # Check for sufficient funds
        if account.balance < amount:
            raise InsufficientFundsException('Insufficient funds')

        # Deduct the amount from the account balance
        account.balance -= amount
        # Log the transaction
        TransactionManager.log_transaction(account.account_number, amount, 'withdraw')

    def deposit(self, account, amount):
        # Handles deposit into an account
        self.check_account_active(account)

        # Add the amount to the account balance
        account.balance += amount
        # Log the transaction
        TransactionManager.log_transaction(account.account_number, amount, 'deposit')

    def transfer(self, from_account, to_account, amount, pin_number):
        # Handles transfer between two accounts
        self.check_account_active(from_account)
        self.check_account_active(to_account)
        self.validate_pin(from_account, pin_number)

        # Check for sufficient funds
        if from_account.balance < amount:
            raise InsufficientFundsException('Insufficient funds')

        # Check transfer limit based on privileges
        limit = AccountPrivilegesManager.get_transfer_limit(from_account.privilege)
        if amount > limit:
            raise TransferLimitExceededException('Transfer limit exceeded')

        # Deduct amount from source account and add to destination account
        from_account.balance -= amount
        to_account.balance += amount
        # Log the transaction
        TransactionManager.log_transaction(from_account.account_number, amount, 'transfer', to_account.account_number)

    def close_account(self, account):
        # Closes an account (marks it as inactive)
        if not account.is_active:
            raise AccountNotActiveException('Account is already Deactivated')

    def view_accounts_by_type(self, account_type):
        # Views all accounts of a specific type (savings or current)
        if account_type == 'savings':
            accounts = [acc for acc in AccountRepository.accounts if isinstance(acc, Savings)]
        elif account_type == 'current':
            accounts = [acc for acc in AccountRepository.accounts if isinstance(acc, Current)]
        else:
            print("Invalid account type")

        # Display account details if found, else notify no accounts exist
        if accounts:
            print(f"Accounts of type {account_type.capitalize()}:")
            for account in accounts:
                print(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}, Status: {'Active' if account.is_active else 'Inactive'}")
        else:
            print(f"No accounts found of type {account_type.capitalize()}.")

    def view_account_by_id(self, account_number):
        # Views details of a specific account by account number
        account = next((acc for acc in AccountRepository.accounts if acc.account_number == account_number), None)
        if account:
            print(f"Account Details:")
            print(f"Account Number: {account.account_number}")
            print(f"Name: {account.name}")
            print(f"Balance: {account.balance}")
            print(f"Privilege: {account.privilege}")
            print(f"Status: {'Active' if account.is_active else 'Inactive'}")
        else:
            print(f"No account found with account number: {account_number}")

    def view_all_accounts(self):
        # Views details of all accounts
        if AccountRepository.accounts:
            print("All Accounts:")
            for account in AccountRepository.accounts:
                print(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}, Type: {'Savings' if isinstance(account, Savings) else 'Current'}, Status: {'Active' if account.is_active else 'Inactive'}")
        else:
            print("No accounts available.")

    def edit_account(self, account):
        # Edits the details of an active account
        self.check_account_active(account)
        new_name = input("Enter the new name: ")
        new_pin = int(input("Enter the new PIN: "))

        # Update account details
        account.name = new_name
        account.pin_number = new_pin
        print("Account details updated successfully")

    def activate_account(self, account):
        # Activates an account
        if account.is_active:
            raise AccountAlreadyActiveException('Account is already activated')
        else:
            account.is_active = True
            print("Account activated successfully")

    def deactivate_account(self, account):
        # Deactivates an account
        if not account.is_active:
            raise AccountAlreadyDeactivatedException('Account is already deactivated')
        else:
            account.is_active = False
            print("Account deactivated successfully")
