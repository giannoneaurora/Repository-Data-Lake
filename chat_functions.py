import redis
import time


def create_chat(client, user1, user2):
    pass

def send_message(client, user_send, user_receive):
    pass


def write_msg(client):
    msg_text = str(input("Scrivi il messaggio: "))
    msg_time = time.time()
    msg_time_conv = time.strftime('%H:%M:%S', time.gmtime(msg_time))
    chat_mapping = {"Messaggio: " + msg_text,"OrarioInvio: " + msg_time_conv}
    return chat_mapping