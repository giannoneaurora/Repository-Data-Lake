import redis
import time
import user_interface as ui
import client_server_connection as csc

redis_client = csc.get_client().redis_client

# Creiamo una stanza tra due utenti, nel nostro caso user 1 e user 2.
# Diamo un identificativo alla stanza, aggiungiamo questo identificativo
# alle stanze accessibili di ciascun utente, e infine
# come output abbiamo un dizionario contenente l'identificativo della stanza


def create_chat(user1, user2, client):
    room_id = create_room_id(user1, user2)

    client.sadd('Rooms:'+user1, room_id)
    client.sadd('Rooms:'+user2, room_id)
    return {'id': room_id, 'names': [user1, user2]}


def send_message(client, channel):
    if not ui.get_contact_dnd(client):
        return f"L'utente ha la modalità Do Not Disturb attiva! Riprova più tardi!" 
    message = write_msg(client)
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
        # Combine user IDs (order doesn't matter)
        room_id_part1 = user1
        room_id_part2 = user2
        if user1 > user2:  # Or use any other comparison logic
            room_id_part1 = user2
            room_id_part2 = user1

        # Create room ID with a separator and hash the combined string
        room_id = f"{room_id_part1}:{room_id_part2}"

        return room_id
    except TypeError:
        return "User IDs cannot be sorted for room creation."


