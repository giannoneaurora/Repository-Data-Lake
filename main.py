import redis as rd
import bcrypt as bc
#import pipreqs
import chat_functions as cf


host_name = 'redis-13428.c328.europe-west3-1.gce.redns.redis-cloud.com'
port_number = 13428
db_number = 0

redis_client = rd.StrictRedis(host=host_name, port=port_number, db=db_number, charset="utf-8", decode_responses=True, password='kve34LU6Z6t9Wd5I09caDiHQOe7bNL5r')

try:
  # Use username_test as the field name itself
  redis_client.hset('User:'+ username_test, mapping = {'Username': username_test, 'Hashed-Password': dummy_hash_password, 'DoNotDisturb': 'OFF'})
except Exception as e:
  print(f"An Error has occurred: {e}")  # Print any errors encountered


print(redis_client.ping())

# Function to see all users of the app
def users_list():
    u_pattern = 'User:*' # Used to search all users
    users = redis_client.keys(pattern = u_pattern, decode_response = True)
    print(users)

contacts_test = ['user1', 'user2', 'user3']
username_test = 'username_test'

def contact_list(username):
  for contact in contacts:
      redis_client.sadd(f'Contacts:' + username_test, contact)
  book = redis_client.smembers(f'Contacts:' + username_test)
  print(book)

pubsub = redis_client.pubsub()

if __name__ == "__main__":
    channel = 'chat'
    while True:
        message = input("Enter message: ")
        cf.send_message(redis_client, channel, message)

while True:
    message = input("Enter message: ")
    send_message(channel, message)