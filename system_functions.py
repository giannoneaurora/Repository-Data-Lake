import redis
import time
import password_hashing as ph
import client_server_connection as csc

redis_client = csc.get_client().redis_client

def register_user():
    new_username = str(input('Scrivi il tuo nome utente: '))
    if redis_client.exists(f"User:{new_username}"):
        return f"Utente già registrato!"
    new_password = str(input('Crea la tua password: '))
    hashed_password = ph.hash_password(new_password)
    new_user_mapping = create_user_mapping(new_username, hashed_password)
    create_user(redis_client, new_username, new_user_mapping)
    


def create_user(client, username, new_user_mapping):
    try:
        client.hmset(f"User:{username}", new_user_mapping)
        return "Utente registrato correttamente"
    except Exception as eee:
        return f"Errore nella registrazione: {eee}"

def create_user_mapping(username, hashed_password):
    user_mapping = {"Username": username, "Hashed-Password": hashed_password, "DoNotDisturb": "OFF"}
    return user_mapping

def search_user(searched_user, client):
    u_pattern = f'User:{searched_user}*'
    users = [u for u in client.keys(pattern = u_pattern, decode_response = True)]
    return users


def contact_list(username):
  personal_c_pattern = f'Contacts:{username}'
  book = [cc for cc in redis_client.smembers(personal_c_pattern)] 
  return book

def add_contact(username):
    new_contact = 'User:' + str(input('Aggiungi un utente alla lista contatti: '))
    if redis_client.sismember(f"Contacts:{username}", new_contact):
        return "Utente già registrato!"
    else:
        redis_client.sadd('Contacts:'+ username, new_contact)
        return 'Aggiunto contatto!'