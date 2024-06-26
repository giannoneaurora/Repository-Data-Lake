import datetime
import redis
import hashlib
import json

# Connessione a Redis

r = redis.Redis(host='redis-19153.c15.us-east-1-2.ec2.redns.redis-cloud.com',
                    port=19153, db=0, charset="utf-8", decode_responses=True,
                    password="FutfU3TjZa2sP4ne24aaVExF8A6oVn81")

print(r.ping())

