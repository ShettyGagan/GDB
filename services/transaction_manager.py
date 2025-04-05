import datetime
import json
from repositories.account_repository import AccountRepository


# Class to manage Transaction
class TransactionManager:
    # Static variable to hold transaction logs in memory
    transaction_log = []
    # Path to the transaction logs file
    log_file_path = "..\\gdbfinal\\resources\\transaction_logs.json"

    @staticmethod
    def get_current_timestamp():
        # Returns the current date and time
        return datetime.datetime.now()

    @classmethod
    def log_transaction(
        cls, account_number, amount, transaction_type, to_account_number=None
    ):
        # Logs a transaction with the given details
        transaction_record = {
            "account_number": account_number,
            "amount": amount,
            "transaction_type": transaction_type,
            "date": cls.get_current_timestamp().isoformat(),
            "to_account_number": to_account_number,
        }
        cls.transaction_log.append(transaction_record)
        try:
            # Write the transaction log to the file
            with open(cls.log_file_path, "w") as f:
                json.dump(cls.transaction_log, f, indent=2)
        except Exception as e:
            # Handle file write errors
            print("Error writing transaction log: ", e)

    @classmethod
    def view_transaction_logs(cls):
        # Displays all transaction logs
        print("Transaction Logs:")

        try:
            # Read and display the transaction logs from the file
            with open(cls.log_file_path, "r") as f:
                log_reader = json.load(f)
                for line in log_reader:
                    print("-" * 30)
                    print(f"Account Number   : {line.get('account_number', 'N/A')}")
                    print(f"Amount           : {line.get('amount', 'N/A')}")
                    print(f"Transaction Type : {line.get('transaction_type', 'N/A')}")
                    print(f"Date             : {line.get('date', 'N/A')}")
                    print(f"To Account       : {line.get('to_account_number', 'N/A')}")
                    print("-" * 30)
        except IOError as e:
            # Handle file read errors
            print(f"Error reading transaction log file: {e}")

    @classmethod
    def view_transactions_by_date(cls, account_number, start_date, end_date):
        # Displays transactions for a specific account within a date range
        print(f"Transactions from {start_date} to {end_date}")

        try:
            # Read and filter transactions from the file
            with open(cls.log_file_path, "r") as f:
                data = f.read()
                transaction = json.loads(data)
                for transaction in transaction:
                    transaction_date = datetime.datetime.fromisoformat(
                        transaction["date"]
                    )
                    if (
                        start_date <= transaction_date <= end_date
                        and transaction["account_number"] == account_number
                    ):
                        print("-" * 30)
                        print(
                            f"Account Number   : {transaction.get('account_number', 'N/A')}"
                        )
                        print(f"Amount           : {transaction.get('amount', 'N/A')}")
                        print(
                            f"Transaction Type : {transaction.get('transaction_type', 'N/A')}"
                        )
                        print(f"Date             : {transaction.get('date', 'N/A')}")
                        print(
                            f"To Account       : {transaction.get('to_account_number', 'N/A')}"
                        )
                        print("-" * 30)

        except IOError as e:
            # Handle file read errors
            print(f"Error reading transaction log file: {e}")

    @classmethod
    def view_transactions_by_type(cls, account_number, type):
        # Displays transactions of a specific type for a specific account
        print(f"Transactions of type {type} of account {account_number}: ")
        try:
            # Read and filter transactions by type from the file
            with open(cls.log_file_path, "r") as f:
                log_reader = json.load(f)
                for line in log_reader:
                    if (
                        line["transaction_type"] == type
                        and line["account_number"] == account_number
                    ):
                        print("-" * 30)
                        print(f"Account Number   : {line.get('account_number', 'N/A')}")
                        print(f"Amount           : {line.get('amount', 'N/A')}")
                        print(
                            f"Transaction Type : {line.get('transaction_type', 'N/A')}"
                        )
                        print(f"Date             : {line.get('date', 'N/A')}")
                        print(
                            f"To Account       : {line.get('to_account_number', 'N/A')}"
                        )
                        print("-" * 30)
        except Exception as e:
            # Handle file read errors
            print(f"Error reading transaction log file: {e}")

    @classmethod
    def count_of_withdrawals_by_date(cls, target_date):
        # Counts the number of withdrawal transactions on a specific date
        try:
            # Read and count withdrawals from the file
            with open(cls.log_file_path, "r") as f:
                transaction = json.load(f)
                withdrawal_count = 0
                for transaction in transaction:
                    transaction_date = datetime.datetime.fromisoformat(
                        transaction["date"]
                    )
                    if (
                        target_date.date() == transaction_date.date()
                        and transaction.get("transaction_type") == "withdraw"
                    ):
                        withdrawal_count += 1

                print(f"Total withdrawals on {target_date} is {withdrawal_count}")
        except Exception as e:
            # Handle file read errors
            print(f"Error reading transaction log file: {e}")
