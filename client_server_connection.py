import redis as rd

# Change this values if you want to use your own server
HOST_NAME = 'redis-13428.c328.europe-west3-1.gce.redns.redis-cloud.com'
PORT_NUMBER = 13428
PASSWORD = 'kve34LU6Z6t9Wd5I09caDiHQOe7bNL5r'
DB_NUMBER = 0

class Client:
    def __init__(self):
        self.host_name = HOST_NAME
        self.port_number = PORT_NUMBER
        self.db_number = DB_NUMBER
        self.password = PASSWORD

        self.redis_client = rd.Redis(host=self.host_name, port=self.port_number, db=self.db_number, charset="utf-8", decode_responses=True, password=self.password)
        self.pubsub = self.redis_client.pubsub()

def get_client(): 
    return Client()