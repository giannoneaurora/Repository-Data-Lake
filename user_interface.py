import redis as rd
import time
import password_hashing as ph


def get_contact_dnd(client, contact):
    dnd_state = client.hget('User:'+contact, 'DoNotDisturb')
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
    u_pattern = 'User:*'
    users = [u for u in client.keys(pattern = u_pattern, decode_response = True) if searched_user in u[0:]]
    return users

    
def save_user_info(user_id, user_info, client):
    client.hmset(user_id, user_info)

# Funzione per recuperare le informazioni dell'utente
def get_user_info(user_id, client):
    return client.hgetall(user_id)

