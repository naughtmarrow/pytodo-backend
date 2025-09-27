from . import User
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(new_user: User, raw_text_password: str):
    """
    Simply takes the newly formed user and assigns it a hash password from the raw before saving to DB.
    Parameters:
        new_user: The user object with no password as obtained from the signup form.
        raw_text_password: The raw text password as obtained form the signup form.

    Usage:
        set_password(new_user, raw_text_password)
    """
    hash = generate_password_hash(raw_text_password)
    new_user.password = hash

def check_password(password_hash: str, raw_text_password: str) -> bool:
    """
    Takes in the password hash and raw password as given by the login form and compares them.
    Parameters: 
        password_hash: The password of the requested login as provided by get_user_password.
        raw_text_password: The raw password as provided by the login form.

    Returns:
        A boolean value representing whether or not the password is valid and correct.

    Usage:
        (after the login form has been validated)
        valid_user = check_password(password_hash, raw_text_password)
    """
    return check_password_hash(password_hash, raw_text_password)
