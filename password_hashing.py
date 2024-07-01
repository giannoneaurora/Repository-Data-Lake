import bcrypt 


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def check_password(password):
    entered_password = str(print('Reinserisci la password: '))
    while password != entered_password:
        print("Password non corretta!")
    return True


# This function makes sure the password is safe
def check_password_limitations(password, len_check = False):
    if len(password) >= 9:
        len_check = True
    uppercase_check = not password.islower() # If the password has at least uppercase letter the value is True
    digit_check = any(c.isdigit() for c in password) # If the password has at least one number the value is True
    has_symbol_check = not password.isalnum() # If the password has at least one symbol the value is True

    # If all password limitations check are True then the password is accepted
    if len_check and uppercase_check and digit_check and has_symbol_check:
        return True
    
    return False
    
    




