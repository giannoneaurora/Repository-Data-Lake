import redis
import system_functions as sf
import random
import time


usernames_test = ['TEST1','TEST2','TEST3','TEST4','TEST5']

dummy_hashed_passwords = ['1234','5678','abcd','wxyz','lmno']

dummy_messages = ['Hi T1!',
                'Hello T2!',
                'Greetings T3!',
                'Hey T4!',
                'Welcome T5!']

dummy_mappings_list = []
for item in zip(usernames_test,dummy_hashed_passwords):
    dummy_mappings_list.append(sf.create_mapping(item[0],item[1]))


