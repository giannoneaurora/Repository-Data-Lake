import redis
import time
import user_interface as ui


def create_chat(client, user1, user2):
    pass

def send_message(client, user_send, user_receive):
    can_send_msg = ui.get_contact_dnd(client, user_receive)
    if not can_send_msg:
        return f"L'utente ha la modalità DND attiva. Riprova più tardi!" 
    pass
    


def write_msg(client):
    msg_text = str(input("Scrivi il messaggio: "))
    msg_time = time.time().strftime('%H:%M:%S')
    chat_mapping = {"Messaggio: " + msg_text,"OrarioInvio: " + msg_time}
    return chat_mapping