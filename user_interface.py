import redis as rd
import time
import password_hashing as ph


def register_user(client):
    print("Benvenuto nella chat!\n Iscriviti!\n")
    username = str(input("Scrivi il nome utente: "))
    if client.exists(username): #if username in client:
        return False
    password = str(input("Scrivi la password: "))
    hashed_password = ph.hash_password(password)
    client.hmset()
    client.set()
    return True

def get_contact_dnd(client, contact):
    dnd_state = client.hget('Users'+ contact, 'DoNotDisturb')
    try:
        if dnd_state == 'OFF':
            return False
        elif dnd_state == 'ON':
            return True
    except Exception as err:
        return f"Errore di sistema: {err}"

def set_dnd(client, username):
    dnd_status = get_contact_dnd(client, username)
    print(f'Attualmente sei {dnd_status}.\n')
    try:
        if dnd_status == 'OFF':
            client.hset('Users'+ username, 'DoNotDisturb', 'ON')
            print('Stato aggiornato ad Attivo!')
        elif dnd_status == 'ON':
            client.hset('Users'+ username, 'DoNotDisturb', 'OFF')
            print('Stato aggiornato a Non Disturbare!')
    except Exception as ee:
        return f"Errore di sistema: {ee}"
        
    


def search_user(searched_user, client):
    users = [u for u in client.keys() if searched_user in str(u)]
    return users
    
def save_user_info(user_id, user_info, client):
    client.hmset(user_id, user_info)

# Funzione per recuperare le informazioni dell'utente
def get_user_info(user_id, client):
    return client.hgetall(user_id)
    