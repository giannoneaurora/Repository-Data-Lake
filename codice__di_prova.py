import redis
import json
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
    user_data = json.dumps({"password": password_hash, "status": "offline", "dnd": "off"})
    redis_client.set(f"user:{username}", user_data)
    print("User registered successfully.")

def add_contact(username, contact):
    if not redis_client.exists(f"user:{contact}"):
        print("Contact does not exist.")
        return
    redis_client.sadd(f"contacts:{username}", contact)
    print("Contact added successfully.")

def send_message(sender, recipient, message):
    if redis_client.sismember(f"contacts:{sender}", recipient) and redis_client.exists(f"user:{recipient}"):
        dnd_status = json.loads(redis_client.get(f"user:{recipient}"))["dnd"]
        if dnd_password:
            print("Recipient is in Do Not Disturb mode.")
            return
        message_data = {
            "from": sender,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        redis_client.rpush(f"messages:{recipient}", json.dumps(message_data))
        print("Message sent successfully.")
    else:
        print("Recipient not in your contacts or does not exist.")

def read_messages(username):
    messages = redis_client.lrange(f"messages:{username}", 0, -1)
    for message in messages:
        message_data = json.loads(message)
        print(f"{message_data['timestamp']} - From {message_data['from']}: {message_data['message']}")


register_user("")
add_contact("", "")
send_message("", "", "")
read_messages("")

def search_users(query):
    all_users = [key.split(':')[1] for key in redis_client.keys("user:*")]
    matched_users = [user for user in all_users if query in user]
    if matched_users:
        print("Found users:")
        for user in matched_user:
            print(user)
    else:
        print("No users found matching the query.")

def set_do_not_disturb(username, status):
    if redis_client.exists(f"user:{username}"):
        user_data = json.loads(redis_client.get(f"user:{username}"))
        user_data['dnd'] = status  # 'on' or 'off'
        redis_client.set(f"user:{username}", json.dumps(user_data))
        print(f"Do Not Disturb has been turned {'on' if status == 'on' else 'off'} for {username}.")
    else:
        print("User not found.")

def view_chat_history(user, contact):
    if not redis_client.exists(f"user:{contact}"):
        print("Contact does not exist.")
        return

    messages = redis_client.lrange(f"messages:{user}", 0, -1)
    formatted_messages = []

    print(f"Chat con {contact} <<")
    for msg_json in messages:
        msg = json.loads(msg_json)
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
