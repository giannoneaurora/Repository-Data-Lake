import redis
import bcrypt 

from hashlib import sha256

def register_user(client):
    username = str(input("Scrivi il nome utente: "))
    if client.exists(username):
        return False
    password = str(input("Scrivi la password: "))
    hashed_password = hash_password(password)
    client.hmset()
    client.set()
    
# Si potrebbe aggiungere lo stato, online/offline
def create_hash_table(username, hashed_password):
    user_data = {"Username:": username, "Hashed-Password:": hashed_password, "DoNotDisturd": False}


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    
def save_user_info(user_id, user_info):
    client.hmset(user_id, user_info)

# Funzione per recuperare le informazioni dell'utente
def get_user_info(user_id):
    return client.hgetall(user_id)
    return True