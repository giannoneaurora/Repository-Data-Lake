import redis
import time
import password_hashing as ph
import client_server_connection as csc

redis_client = csc.get_client().redis_client

def register_user():
    new_username = str(input('Scrivi il tuo nome utente: '))
    if redis_client.exists(new_username):
        return False
    while True:
        new_password = str(input('Crea la tua password: '))
        if ph.check_password(new_password):
            print('Password corretta!')
            break
    hashed_password = ph.hash_password(new_password)
    new_user_mapping = create_user_mapping(new_username, hashed_password)
    create_user(new_username, new_user_mapping)
    

def create_user(username, new_user_mapping):
    redis_client.hset(f"User:{username}", new_user_mapping)

def create_user_mapping(username, hashed_password):
    user_mapping = {"Username": username, "Hashed-Password": hashed_password, "DoNotDisturb": "OFF"}
    return user_mapping

def search_user(searched_user, client):
    u_pattern = 'User:*'
    partial_users = [u for u in client.keys(pattern = u_pattern, decode_response = True) if searched_user in u[0:]]
    users = [uu for uu in partial_users if uu[0:len(searched_user)]==searched_user[0:]]
    return users
