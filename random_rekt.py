import random
import time
import requests

def random_rekt(spl,message):
    if 'username' in message['from']:
        user_from = '@' + message['from']['username']
    else:
        user_from = message['from']['first_name']
                            
    if('reply_to_message' in message):
        reply = message['reply_to_message']
        if('username' in reply['from']):
            user_rekt = '@' + reply['from']['username'] + "'s"
        else:
            user_rekt = reply['from']['first_name']
    elif(len(spl) == 1):
        user_rekt = 'his own'
    else:
        user_rekt = spl[1]

    #n = random.randint(0,2)  #will be uncommented when there will be multiple rekt sentences.
    n=0
    if(n == 0):
        reply_text = user_from + " throws a hot pot on " + user_rekt + " face."
    #insert suitable statements for each rekt sentence.

    return reply_text