import redis
import time
import user_interface as ui


def create_chat(pubsub, user1, user2):
    pubsub.subscribe()

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