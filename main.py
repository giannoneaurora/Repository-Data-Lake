import redis as rd
import bcrypt as bc
import time
import chat_functions as cf
import password_hashing as ph
import system_functions as sf
import user_interface as ui
import client_server_connection as csc

redis_client = csc.get_client().redis_client
pubsub = csc.get_client().pubsub

# Function to see all users of the app
# This function is for maintenance
def users_list():
    u_pattern = 'User:*' # Used to search all users
    users = redis_client.keys(pattern = u_pattern, decode_response = True)
    print(users)

# Function to get all users info
# This function is for maintenance
def get_user_info(username):
    user_key = f'User:{username}'
    return redis_client.hgetall(user_key)

# users_list()
# get_user_info()

if __name__ == "__main__":
  pubsub.run_in_thread(sleep_time=0.001)