import redis
import time
import user_interface as ui
import client_server_connection as csc

redis_client = csc.get_client().redis_client

# Creiamo una stanza tra due utenti, nel nostro caso user 1 e user 2.
# Diamo un identificativo alla stanza, aggiungiamo questo identificativo
# alle stanze accessibili di ciascun utente, e infine
# come output abbiamo un dizionario contenente l'identificativo della stanza


def create_chat_room(client, user1, user2):
    room_id = create_room_id(user1, user2)
    room_1 = f'Rooms:{user1}'
    room_2 = f'Rooms:{user2}'

    client.sadd(room_1, room_id)
    client.sadd(room_2, room_id)
    return({'id': room_id, 'names': [f'{user1}', f'{user2}']})


# Creiamo una funzione che invia un messaggio ad un canale specifico. 
# Se il destinatario ha attiva la modalità "Do Not Disturb", la funzione 
# ritorna un messaggio di avviso. Altrimenti, il messaggio viene pubblicato sul canale 
# utilizzando il client Redis.


def send_message(client, channel):
    if not ui.get_contact_dnd(client, user_receive):
        return f"L'utente ha la modalità Do Not Disturb attiva! Riprova più tardi!" 
    client.publish(channel, message)


def show_chat(pubsub):
    for msg in pubsub.listen():
        if msg['type'] == 'message':
            handle_message(message)

def handle_message(message):
    print(f"Received message: {message['data'].decode('utf-8')}")

def write_msg(client):
    msg_text = str(input("Scrivi il messaggio: "))
    msg_time = time.time().strftime('%H:%M:%S')
    chat_mapping = {"Messaggio: " + msg_text,"OrarioInvio: " + msg_time}
    return chat_mapping

# Creiamo una funzione che genera un identificativo di 
# stanza univoco per due utenti. Ordiniamo i nomi degli utenti e li 
# combiniamo in una stringa separata da due punti

def create_room_id(user1, user2):
    try:
        sorted_id = sorted(user1, user2) 
        return f"{sorted_id[0]}:{sorted_id[1]}"
    except Error as x:
        print(f'Errore: {x}')


