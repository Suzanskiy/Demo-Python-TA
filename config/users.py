#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

class Users:
    VALID_USERS = {
        "standard_user": "secret_sauce",
        "problem_user": "secret_sauce",
        "performance_glitch_user": "secret_sauce",
        "error_user": "secret_sauce",
        "visual_user": "secret_sauce"
    }
    
    LOCKED_USER = {
        "locked_out_user": "secret_sauce"
    }
    
    ALL_USERS = {**VALID_USERS, **LOCKED_USER}
    
    @staticmethod
    def get_password(username):
        return Users.ALL_USERS.get(username, "secret_sauce") 