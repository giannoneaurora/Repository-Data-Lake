import redis
from hashlib import sha256
from getpass import getpass
from datetime import datetime

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def register_user(username):
    if redis_client.exists(f"user:{username}"):
        print("Username already taken.")
        return
    password = getpass("Enter your password: ")
    password_hash = sha256(password.encode()).hexdigest()
    user_data = {"password": password_hash, "status": "offline", "dnd": "off"}
    redis_client.hset(f"user:{username}", mapping=user_data)
    print("User registered successfully.")

def add_contact(username, contact):
    if not redis_client.exists(f"user:{contact}"):
        print("Contact does not exist.")
        return
    redis_client.sadd(f"contacts:{username}", contact)
    print("Contact added successfully.")


def send_message(sender, recipient, message):
    if not redis_client.sismember(f'user:{sender}:contacts', recipient):
        return "Recipient not in contacts list"
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dnd_status = redis_client.hget(f'user:{recipient}', 'dnd')
    
    if dnd_status == 'true':
        return "User is in Do Not Disturb mode"
    
    redis_client.rpush(f'chat:{sender}:{recipient}', f'>{message} [{timestamp}]')
    redis_client.rpush(f'chat:{recipient}:{sender}', f'<{message} [{timestamp}]')
    return "Message sent"

def read_messages(user, contact):
    chat_key = f'chat:{user}:{contact}'
    messages = redis_client.lrange(chat_key, 0, -1)
    return messages

def send_message(sender, recipient, message):
    if redis_client.sismember(f"contacts:{sender}", recipient) and redis_client.exists(f"user:{recipient}"):
        dnd_status = redis_client.hget(f"user:{recipient}", "dnd")
        if dnd_status == "on":
            print("Recipient is in Do Not Disturb mode.")
            return
        message_data = {
            "from": sender,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        redis_client.rpush(f"messages:{recipient}", message_data)
        print("Message sent successfully.")
    else:
        print("Recipient not in your contacts or does not exist.")

def read_messages(username):
    messages = redis_client.lrange(f"messages:{username}", 0, -1)
    for message in messages:
        print(f"{message['timestamp']} - From {message['from']}: {message['message']}")

def search_users(query):
    all_users = [key.split(':')[1] for key in redis_client.keys("user:*")]
    matched_users = [user for user in all_users if query in user]
    if matched_users:
        print("Found users:")
        for user in matched_users:
            print(user)
    else:
        print("No users found matching the query.")

def set_do_not_disturb(username, status):
    if redis_client.exists(f"user:{username}"):
        redis_client.hset(f"user:{username}", "dnd", status)
        print(f"Do Not Disturb has been turned {'on' if status == 'on' else 'off'} for {username}.")
    else:
        print("User not found.")

def view_chat_history(user, contact):
    if not redis_client.exists(f"user:{contact}"):
        print("Contact does not exist.")
        return

    messages = redis_client.lrange(f"messages:{user}", 0, -1)
    formatted_messages = []

    print(f"Chat with {contact} <<")
    for msg in messages:
        if msg['from'] == user:
            prefix = ">"
        else:
            prefix = "<"
        formatted_messages.append(f"{prefix} {msg['message']}\t[{msg['timestamp']}]")

    if formatted_messages:
        for message in formatted_messages:
            print(message)
    else:
        print("No messages in this chat.")

def main():
    while True:
        print("Commands: register, login, send, read, search, set_dnd, view_chat, exit")
        command = input("Enter command: ").strip().lower()
        if command == "register":
            username = input("Choose a username: ")
            register_user(username)
        elif command == "login":
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")
            login(username, password)
        elif command == "send":
            sender = input("Enter your username: ")
            recipient = input("Enter recipient's username: ")
            message = input("Write your message: ")
            send_message(sender, recipient, message)
        elif command == "read":
            username = input("Enter your username: ")
            read_messages(username)
        elif command == "search":
            query = input("Enter search query: ")
            search_users(query)
        elif command == "set_dnd":
            username = input("Enter your username: ")
            status = input("Enter status (on/off): ")
            set_do_not_disturb(username, status)
        elif command == "view_chat":
            user = input("Enter your username: ")
            contact = input("Enter contact's username: ")
            view_chat_history(user, contact)
        elif command == "exit":
            print("Exiting the application.")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()




import bcrypt
from app import redis_client

def hash_password(password):
    """Hash della password usando bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(stored_password, provided_password):
    """Verifica se la password fornita corrisponde all'hash memorizzato."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def register(username, password):
    if redis_client.hexists('users', username):
        return "User already exists"
    hashed_password = hash_password(password)
    redis_client.hset('users', username, hashed_password)
    redis_client.hset(f'user:{username}', 'contacts', '')
    redis_client.hset(f'user:{username}', 'dnd', 'false')
    return "User registered successfully"

def login(username, password):
    stored_password = redis_client.hget('users', username)
    if stored_password and check_password(stored_password.encode('utf-8'), password):
        return "Login successful"
    return "Invalid credentials"






def send_message(sender, recipient, message):
    if not redis_client.sismember(f'user:{sender}:contacts', recipient):
        return "Recipient not in contacts list"
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dnd_status = redis_client.hget(f'user:{recipient}', 'dnd')
    
    if dnd_status == 'true':
        return "User is in Do Not Disturb mode"
    
    redis_client.rpush(f'chat:{sender}:{recipient}', f'>{message} [{timestamp}]')
    redis_client.rpush(f'chat:{recipient}:{sender}', f'<{message} [{timestamp}]')
    return "Message sent"

def read_messages(user, contact):
    chat_key = f'chat:{user}:{contact}'
    messages = redis_client.lrange(chat_key, 0, -1)
    return messages
r = redis.Redis(host='redis-19153.c15.us-east-1-2.ec2.redns.redis-cloud.com',
                    port=19153, db=0, charset="utf-8", decode_responses=True,
                    password="FutfU3TjZa2sP4ne24aaVExF8A6oVn81")

print(r.ping())
