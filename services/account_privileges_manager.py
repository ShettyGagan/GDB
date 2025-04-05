from models.privileges import Privilege
import json

# Class to manage Privileges
class AccountPrivilegesManager:
    # Path to the file containing daily transfer limits
    daily_path = "..\\gdbfinal\\resources\\dailyLimits.json"
    
    # Load privileges and their respective transfer limits from the JSON file
    with open(
        daily_path,
        "r",
    ) as f:
        privileges = json.load(f)

    @classmethod
    def get_transfer_limit(cls, privilege):
        # Returns the daily transfer limit for a given privilege
        return cls.privileges.get(privilege, 0)

    @classmethod
    def set_daily_transfer_limit(cls, privilege, new_limit):
        # Updates the daily transfer limit for a given privilege
        cls.privileges[privilege] = new_limit
        
        # Save the updated limits back to the JSON file
        with open(
            cls.daily_path,
            "w",
        ) as f:
            json.dump(cls.privileges, f, indent=2)
