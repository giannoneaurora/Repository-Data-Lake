import redis as rd

def get_contact_dnd(client, contact):
    dnd_state = client.hget('User:'+contact, 'DoNotDisturb')
    try:
        if dnd_state == 'OFF':
            return False
        elif dnd_state == 'ON':
            return True
    except Exception as err:
        return f"Errore di sistema: {err}"

def set_dnd(client, contact):
    dnd_status = client.hget('User:' + contact, 'DoNotDisturb')
    print(f'Attualmente sei {dnd_status}.\n')
    try:
        if dnd_status == 'OFF':
            client.hset('User:'+ contact, 'DoNotDisturb', 'ON')
            print('Stato aggiornato ad Attivo!')
        elif dnd_status == 'ON':
            client.hset('User:'+ contact, 'DoNotDisturb', 'OFF')
            print('Stato aggiornato a Non Disturbare!')
    except Exception as ee:
        return f"Errore di sistema: {ee}"



