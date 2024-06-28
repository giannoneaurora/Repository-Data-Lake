import redis as rd


class Client:
    def __init__(self):
        self.host_name = 'redis-13428.c328.europe-west3-1.gce.redns.redis-cloud.com'
        self.port_number = 13428
        self.db_number = 0

        self.redis_client = rd.Redis(host=self.host_name, port=self.port_number, db=self.db_number, charset="utf-8", decode_responses=True, password='kve34LU6Z6t9Wd5I09caDiHQOe7bNL5r')

def get_client(): 
    return Client()