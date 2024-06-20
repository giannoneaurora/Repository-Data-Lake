import redis
import time

def create_mapping(username, hashed_password):
    user_mapping = {"Username": username, "Hashed-Password": hashed_password, "DoNotDisturb": "OFF"}
    return user_mapping

