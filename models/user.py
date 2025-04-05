import hashlib
import uuid
from repositories.account_repository import AccountRepository
    
class User:
    def __init__(self, user_id, name, password, status="inactive"):  
        self.name = name
        self.password_hash = self._hash_password(password) 
        self.user_id = user_id
        self.status = status
        self.accounts = [] 

    def _hash_password(self, password):
        salt = uuid.uuid4().hex  
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt
        return hashed_password

    def check_password(self, password):
        password_hash, salt = self.password_hash.split(':')
        return password_hash == hashlib.sha256((password + salt).encode()).hexdigest()

    def add_account(self, new_account):
        self.accounts.append(new_account)

class UserManager:
    def __init__(self): 
        self.users = {}

    def create_user(self, name, user_id):
        password = uuid.uuid4().hex  
        status = "active"
        new_user = User(user_id, name, password, status)
        print(f"User {name} created with Password {password}")
        return new_user

    def find_user(self, user_id):
        return self.users.get(user_id)

    @classmethod
    def activate_user(cls, user_id):
        for user in AccountRepository.users:
            if int(user.user_id) == int(user_id):
                user.status = "active"
                print(f"User {user_id} has been activated.")
                return  # Exit after updating
        print(f"User ID {user_id} not found.")

    # Function to inactivate a user
    @classmethod
    def inactivate_user(cls, user_id):
        for user in AccountRepository.users:
            if int(user.user_id) == int(user_id):
                user.status = "inactive"
                print(f"User {user_id} has been inactivated.")
                return  # Exit after updating
        print(f"User ID {user_id} not found.")

    @classmethod
    def view_all_users(cls):
        print("List of all users:")
        for user in AccountRepository.users:
            print(f"User_ID: {user.user_id}\tName: {user.name}\tStatus: {user.status}")
