import redis
import time
import user_interface as ui


def create_chat(user1, user2, client):
    room_id = create_room_id(user1, user2)

    client.sadd(f'Rooms:{user1}', room_id)
    client.sadd(f'Rooms:{user2}', room_id)
    return({'id': room_id, 'names': [f'{user1}', f'{user2}']})





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


def create_room_id(user1, user2):
    try:
        sorted_id = sorted(user1, user2) 
        return f"{sorted_id[0]}:{sorted_id[1]}"
    except Error as x:
        print(f'Errore: {x}')


