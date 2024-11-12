# exceptions.py

class AccountNotActiveException(Exception):
    pass

class InsufficientFundsException(Exception):
    pass

class InvalidPinException(Exception):
    pass

class TransferLimitExceededException(Exception):
    pass