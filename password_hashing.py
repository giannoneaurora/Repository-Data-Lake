import bcrypt 

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def check_password(password):
    entered_password = str(print('Reinserisci la password: '))
    if entered_password != password:
        return False
    return True




