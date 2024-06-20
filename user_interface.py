import redis as rd
import time


def register_user(client):
    print("Benvenuto nella chat!\n Iscriviti!\n")
    username = str(input("Scrivi il nome utente: "))
    if client.exists(username): #if username in client:
        return False
    password = str(input("Scrivi la password: "))
    hashed_password = hash_password(password)
    client.hmset()
    client.set()



def search_user(searched_user):
    users = [u for u in redis_client.keys() if searched_user in str(u)]
    
    return users
    
def save_user_info(user_id, user_info):
    redis_client.hmset(user_id, user_info)

# Funzione per recuperare le informazioni dell'utente
def get_user_info(user_id):
    return redis_client.hgetall(user_id)
    