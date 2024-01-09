import random
import time
import requests

def random_rekt(spl,message):
    reply_text = ''
    if 'username' in message['from']:
        user_from = '@' + message['from']['username']
    else:
        user_from = message['from']['first_name']
                            
    if('reply_to_message' in message):
        reply = message['reply_to_message']
        if('username' in reply['from']):
            user_rekt = '@' + reply['from']['username']
        else:
            user_rekt = reply['from']['first_name']
    elif(len(spl) == 1):
        user_rekt = user_from
    else:
        user_rekt = spl[1]

    n = random.randint(0,2)

    if(n == 0):
        reply_text = user_from + " throws a hot pot on " + user_rekt + "'s face."
    if(n == 1):
        reply_text = user_from + " whacks " + user_rekt + " with a toaster"
    if(n == 2):
        reply_text = user_from + " pins " + user_rekt + " down and repeatedly hits him with a fire extinguisher"

    return reply_text