import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))


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
    
    




