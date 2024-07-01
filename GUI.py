import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import redis
import time
import client_server_connection as csc

# Connect to the Redis server
redis_client = csc.get_client().redis_client
pubsub = redis_client.pubsub()

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Redis Chat App")

        # Main frames
        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)
        self.chat_frame = tk.Frame(self.root)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.message_var = tk.StringVar()
        self.dnd_status = tk.StringVar(value="DND Status: OFF")
        self.recipient = tk.StringVar()

        self.create_login_page()

    def create_login_page(self):
        self.clear_frames()

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.login_frame, textvariable=self.username).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.login_frame, textvariable=self.password, show='*').grid(row=1, column=1, padx=10, pady=10)

        self.login_label = tk.Label(self.login_frame, text="")
        self.login_label.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(self.login_frame, text="Login", command=self.attempt_login).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Create New Account", command=self.create_register_page).grid(row=4, column=0, columnspan=2, pady=10)

        self.login_frame.pack(padx=20, pady=20)

    def create_register_page(self):
        self.clear_frames()

        tk.Label(self.register_frame, text="New Username").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.register_frame, textvariable=self.username).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.register_frame, text="New Password").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.register_frame, textvariable=self.password, show='*').grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.register_frame, text="Register", command=self.register).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.register_frame, text="Back to Login", command=self.create_login_page).grid(row=3, column=0, columnspan=2, pady=10)

        self.register_frame.pack(padx=20, pady=20)

    def create_chat_page(self):
        self.clear_frames()

        self.chat_display = tk.Text(self.chat_frame, state='disabled', width=50, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        tk.Entry(self.chat_frame, textvariable=self.message_var).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.chat_frame, text="Send", command=self.send_message).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.chat_frame, textvariable=self.dnd_status).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.chat_frame, text="Do Not Disturb", command=self.toggle_dnd).grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.chat_frame, text="Add Contact", command=self.add_contact).grid(row=2, column=2, padx=10, pady=10)
        tk.Button(self.chat_frame, text="View Contacts", command=self.view_contacts).grid(row=2, column=3, padx=10, pady=10)
        tk.Button(self.chat_frame, text="Create Temp Chat", command=self.create_temp_chat).grid(row=3, column=0, columnspan=4, pady=10)

        self.recipient_list = ttk.Combobox(self.chat_frame, textvariable=self.recipient)
        self.recipient_list.grid(row=1, column=2, padx=10, pady=10)
        self.recipient_list.bind("<<ComboboxSelected>>", self.load_last_messages)
        self.update_recipient_list()

        self.chat_frame.pack(padx=20, pady=20)

        # Update the DND status initially
        self.update_dnd_status()

        # Start the pubsub listener thread
        self.pubsub_thread = pubsub.run_in_thread(sleep_time=0.001)
        pubsub.psubscribe(**{f'Chat:*:{self.username.get()}': self.handle_message,
                             'temp_*': self.handle_message})

    def clear_frames(self):
        for frame in [self.login_frame, self.register_frame, self.chat_frame]:
            frame.pack_forget()

    def attempt_login(self):
        username = self.username.get()
        password = self.password.get()
        self.login(username, password)

    def login(self, username_input, password_input):
        logged_in = True
        if not redis_client.exists(f"User:{username_input}"):
            self.login_label.configure(text="L'utente non esiste!")
            logged_in = False
        else:
            user_password = redis_client.hget(f"User:{username_input}", 'Hashed-Password')
            if logged_in and password_input != user_password:
                self.login_label.configure(text="Password errata!")
                logged_in = False
        
        if logged_in:
            self.login_label.configure(text="Benvenuto nella chat!")
            self.create_chat_page()

    def register(self):
        username = self.username.get()
        password = self.password.get()
        if not redis_client.exists(f"User:{username}"):
            user_mapping = self.create_user_mapping(username, password)
            self.create_user(redis_client, username, user_mapping)
            messagebox.showinfo("Success", "User registered successfully")
            self.create_login_page()
        else:
            messagebox.showerror("Error", "User already exists")

    def create_user(self, client, username, new_user_mapping):
        try:
            client.hmset(f"User:{username}", new_user_mapping)
            return "Utente registrato correttamente"
        except Exception as e:
            return f"Errore nella registrazione: {e}"

    def create_user_mapping(self, username, hashed_password):
        user_mapping = {"Username": username, "Hashed-Password": hashed_password, "DoNotDisturb": "OFF"}
        return user_mapping

    def send_message(self):
        message = self.message_var.get()
        if message:
            recipient = self.recipient.get()  # Get the recipient from the combobox
            if recipient:
                if recipient.startswith("temp_"):
                    self.send_temp_message()
                else:
                    channel = self.create_room_id(self.username.get(), recipient)
                    time_1 = time.time()
                    msg_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_1))
                    formatted_msg = f"< {self.username.get()}: {message} [{msg_time}]"
                    encoded_message = self.write_msg(formatted_msg)
                    redis_client.publish(channel, encoded_message)
                    self.store_message(formatted_msg, channel)
                
                    # Update chat display immediately for sent message (on top)
                    self.update_chat_display(formatted_msg, top=True)
                
                    self.message_var.set("")

                    # Notify the user about sending the message
                    messagebox.showinfo("Sent Message", "Message sent successfully")


    def write_msg(self, msg_text):
        encoded_msg = msg_text
        return encoded_msg

    def store_message(self, formatted_msg, channel):
        redis_client.rpush(f'Messages:{channel}', formatted_msg)

    def create_room_id(self, user1, user2):
        room_id_part1 = min(user1, user2)
        room_id_part2 = max(user1, user2)
        room_id = f"Chat:{room_id_part1}:{room_id_part2}"
        return room_id

    def create_temp_chat_id(self, user1, user2):
        room_id_part1 = min(user1, user2)
        room_id_part2 = max(user1, user2)
        room_id = f"temp_Chat:{room_id_part1}:{room_id_part2}"
        return room_id

    def toggle_dnd(self):
        contact = self.username.get()
        current_dnd_status = redis_client.hget('User:' + contact, 'DoNotDisturb')

        try:
            if current_dnd_status == 'OFF':
                redis_client.hset('User:' + contact, 'DoNotDisturb', 'ON')
                messagebox.showinfo("Success", "You are now in Do Not Disturb mode.")
            else:
                redis_client.hset('User:' + contact, 'DoNotDisturb', 'OFF')
                messagebox.showinfo("Success", "You have exited Do Not Disturb mode.")
            self.update_dnd_status()
        except redis.RedisError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_dnd_status(self):
        contact = self.username.get()
        current_dnd_status = redis_client.hget('User:' + contact, 'DoNotDisturb')
        self.dnd_status.set(f"DND Status: {current_dnd_status}")

    def add_contact(self):
        partial_contact = simpledialog.askstring("Add Contact", "Enter the partial username of the contact:")
        if partial_contact:
            # Find all users that match the partial username
            matching_users = [user.split(':')[1] for user in redis_client.keys("User:*") if partial_contact in user.split(':')[1]]
        
            if matching_users:
                selected_contact = simpledialog.askstring("Select Contact", f"Multiple matches found: {', '.join(matching_users)}\nPlease enter the exact username of the contact:")
                if selected_contact and selected_contact in matching_users:
                    redis_client.sadd(f"Contacts:{self.username.get()}", selected_contact)
                    messagebox.showinfo("Success", "Contact added successfully.")
                    self.update_recipient_list()
                else:
                    messagebox.showerror("Error", "Contact does not exist.")
            else:
                messagebox.showerror("Error", "No matching contacts found.")

    def view_contacts(self):
        contacts = redis_client.smembers(f"Contacts:{self.username.get()}")
        contacts_list = "\n".join(contact for contact in contacts)
        messagebox.showinfo("Your Contacts", contacts_list)

    def load_last_messages(self, event=None):
        self.chat_display.configure(state='normal')
        self.chat_display.delete('1.0', tk.END)
    
        recipient = self.recipient.get()
        if recipient:
            channel = recipient if recipient.startswith("temp_") else self.create_room_id(self.username.get(), recipient)
            stored_messages = redis_client.lrange(f'Messages:{channel}', -10, -1)
            for message in reversed(stored_messages):
                self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.configure(state='disabled')

        # Update the recipient list to remove destroyed temporary chats
        self.update_recipient_list()

    def create_temp_chat(self):
        recipient = simpledialog.askstring("Create Temporary Chat", "Enter the username of the contact:")
        if recipient:
            if redis_client.exists(f"User:{recipient}"):
                temp_chat_id = self.create_temp_chat_id(self.username.get(), recipient)
                redis_client.sadd(f"TempChats:{self.username.get()}", temp_chat_id)
                redis_client.sadd(f"TempChats:{recipient}", temp_chat_id)
            
                # Set the recipient to the temp chat ID
                self.recipient.set(temp_chat_id)
                self.update_recipient_list()
            
                # Start the timer for destroying the temp chat
                if hasattr(self, 'temp_chat_timer_id'):
                    self.root.after_cancel(self.temp_chat_timer_id)
                self.temp_chat_timer_id = self.root.after(60000, self.destroy_temp_chat, temp_chat_id)
            
                messagebox.showinfo("Success", f"Temporary chat created with {recipient}.")
            else:
                messagebox.showerror("Error", "Contact does not exist.")


    def destroy_temp_chat(self, temp_chat_id):
        current_chat = self.recipient.get()
        redis_client.delete(f'Messages:{temp_chat_id}')
        users = redis_client.smembers(f"TempChats:{temp_chat_id}")
        for user in users:
            redis_client.srem(f"TempChats:{user}", temp_chat_id)
        redis_client.delete(f"TempChats:{temp_chat_id}")

        # Stop listening to this temp chat
        pubsub.unsubscribe(temp_chat_id)

        if current_chat == temp_chat_id:
            self.clear_chat_display()
            self.recipient.set('')  # Clear the recipient

        self.update_recipient_list()

        # Inform the user about the destruction
        messagebox.showinfo("Info", f"Temporary chat {temp_chat_id} destroyed due to inactivity.")

    def send_temp_message(self):
        message = self.message_var.get()
        temp_chat_id = self.recipient.get()
        if message and temp_chat_id.startswith("temp_"):
            # Check if the tempchat still exists before sending the message
            if redis_client.exists(f"Messages:{temp_chat_id}"):
                time_1 = time.time()
                msg_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_1))
                formatted_msg = f"< {self.username.get()}: {message} [{msg_time}]"
                encoded_message = self.write_msg(formatted_msg)
                redis_client.publish(temp_chat_id, encoded_message)
                self.store_message(formatted_msg, temp_chat_id)
                self.update_chat_display(formatted_msg)
                self.message_var.set("")
                # Reset the timer
                if hasattr(self, 'temp_chat_timer_id'):
                    self.root.after_cancel(self.temp_chat_timer_id)
                self.temp_chat_timer_id = self.root.after(60000, self.destroy_temp_chat, temp_chat_id)
            else:
                messagebox.showerror("Error", "Temporary chat no longer exists.")
                self.update_recipient_list()

    def handle_message(self, message):
        msg = message['data'].decode('utf-8')  # Decode the message
        sender_username = msg.split(':')[1].strip()  # Extract sender's username from the message
    
        # Update the chat display with the received message
        self.update_chat_display(msg)
    
        # Notify the user about the new message
        self.root.after(0, lambda: messagebox.showinfo("New Message", f"You have received a new message from {sender_username}"))

        # Reset the timer for temp chats
        temp_chat_id = self.recipient.get()
        if temp_chat_id.startswith("temp_"):
            if hasattr(self, 'temp_chat_timer_id'):
                self.root.after_cancel(self.temp_chat_timer_id)
            self.temp_chat_timer_id = self.root.after(60000, self.destroy_temp_chat, temp_chat_id)


    def update_chat_display(self, message, top=False):
        self.chat_display.configure(state='normal')
    
        if top:
            self.chat_display.insert('1.0', message + "\n")  # Insert at the beginning
        else:
            self.chat_display.insert(tk.END, message + "\n")  # Insert at the end
    
        self.chat_display.configure(state='disabled')

    def clear_chat_display(self):
        self.chat_display.configure(state='normal')
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.configure(state='disabled')

    def update_recipient_list(self):
        contact_set = redis_client.smembers(f"Contacts:{self.username.get()}")
        contacts = [contact for contact in contact_set]

        temp_chat_set = redis_client.smembers(f"TempChats:{self.username.get()}")
        temp_chats = [temp_chat for temp_chat in temp_chat_set if redis_client.exists(f"Messages:{temp_chat}")]

        # Update recipient list to include both contacts and temp chats
        self.recipient_list['values'] = contacts + temp_chats

        # Check if the current recipient is a destroyed temp chat and clear it if necessary
        current_recipient = self.recipient.get()
        if current_recipient.startswith("temp_") and current_recipient not in temp_chats:
            self.recipient.set('')
            self.clear_chat_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
