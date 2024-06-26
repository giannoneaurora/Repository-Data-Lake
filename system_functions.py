import redis
import time
import password_hashing as ph

def register_user(client):
    new_username = str(input('Scrivi il tuo nome utente: '))
    if client.exists(new_username):
        return False
    while True:
        new_password = str(input('Crea la tua password: '))
        if ph.check_password(new_password):
            print('Password corretta!')
            break
    hashed_password = ph.hash_password(new_password)
    new_user_mapping = create_user_mapping(new_username, hashed_password)
    create_user(client, new_username, new_user_mapping)
    

def create_user(client, username, new_user_mapping):
    client.hset(f"User:{username}", new_user_mapping)

def create_user_mapping(username, hashed_password):
    user_mapping = {"Username": username, "Hashed-Password": hashed_password, "DoNotDisturb": "OFF"}
    return user_mapping

