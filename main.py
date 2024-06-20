import redis as rd

host_name = 'localhost'
port_number = 6379
db_number = 0

redis_client = rd.StrictRedis(host = host_name, port = port_number, db = db_number, decode_responses=True)

username_test = 'TEST'

dummy_hash_password = "b'$2b$12$2Sy/LDvtWMHrmybvTpG4IuhtRiEgYvF3u58CSwyv5SAMOT.c7ECNW'"

redis_client.hset('Test_User', username_test, mapping = {'Username': username_test,'Hashed-Password': dummy_hash_password, 'DoNotDisturb': False})

