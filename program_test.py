import redis as rd
import system_functions as sf
import client_server_connection as csc
from main import users_list
import chat_functions as cf
import user_interface as ui

# Questo file serve solo per testare la connessione al server e il funzionamento del programma

redis_client = csc.get_client().redis_client

redis_client.ping()

usernames_test = ['TEST1','TEST2','TEST3','TEST4','TEST5']

dummy_hashed_passwords = ['1234','5678','abcd','wxyz','lmno']

dummy_messages = ['Hi T1!',
                'Hello T2!',
                'Greetings T3!',
                'Hey T4!',
                'Welcome T5!']

dummy_mappings_list = []
for item in zip(usernames_test,dummy_hashed_passwords):
    dummy_mappings_list.append(sf.create_user_mapping(item[0],item[1]))
 
for u, map in zip(usernames_test,dummy_mappings_list):
    try:
        redis_client.hset(f'User:{u}', mapping = map)
    except Exception as e:
        print(f"An Error has occurred: {e}")  

# Usa per controllare tutta la lista di utenti presenti nel server
# users_list()

# cf.create_chat(usernames_test[0], usernames_test[1], redis_client)

def search_user(searched_user, client):
    u_pattern = 'User:*'
    users = [u for u in client.keys(pattern = u_pattern, decode_response = True) if searched_user in u[:]]
    return users

search_user('T', redis_client)



