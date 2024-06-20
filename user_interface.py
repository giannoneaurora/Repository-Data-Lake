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

def set_dnd(client, username):
    dnd_status = client.hget('Users'+ username, 'DoNotDisturb')
    print(f'Attualmente sei {dnd_status}.\n')
    try:
        if dnd_status == 'OFF':
            client.hset('Users'+ username, 'DoNotDisturb', 'ON')
            print('Stato aggiornato ad Attivo!')
        elif dnd_status == 'ON':
            client.hset('Users'+ username, 'DoNotDisturb', 'OFF')
            print('Stato aggiornato a Non Disturbare!')
    except Exception as ee:
        print(f"Errore di sistema: {ee}")
        
    


def search_user(searched_user):
    users = [u for u in redis_client.keys() if searched_user in str(u)]
    return users
    
def save_user_info(user_id, user_info):
    redis_client.hmset(user_id, user_info)

# Funzione per recuperare le informazioni dell'utente
def get_user_info(user_id):
    return redis_client.hgetall(user_id)
    