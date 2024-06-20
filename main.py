import redis as rd

host_name = 'redis-13428.c328.europe-west3-1.gce.redns.redis-cloud.com'
port_number = 13428
db_number = 0

redis_client = rd.StrictRedis(host=host_name, port=port_number, db=db_number, charset="utf-8", decode_responses=True, password='kve34LU6Z6t9Wd5I09caDiHQOe7bNL5r')

username_test = 'TEST'

dummy_hash_password = '1234'

try:
  # Use username_test as the field name itself
  redis_client.hset('User:'+ username_test, mapping = {'Username': username_test, 'Hashed-Password': dummy_hash_password, 'DoNotDisturb': 'OFF'})
except Exception as e:
  print(f"Error setting hash: {e}")  # Print any errors encountered


print(redis_client.ping())

# Function to see all users of the app
def users_list():
    u_pattern = 'User:*' # Used to search all users
    users = redis_client.keys(pattern = u_pattern, decode_response = True)
    print(users)