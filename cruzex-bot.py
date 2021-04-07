#!/usr/bin/env python3
import requests
import sys
import random_rekt
import time
from decouple import config

botapi_url = 'https://api.telegram.org/bot'
token = config('token')
endpoint = botapi_url + token
offset = 0
method = 'getUpdates'
request = endpoint + '/' + method

while(True):
    try:
        query = {'offset': offset}
        print("\n\nresponse :" + str(response) + "\n\n")
        json = response.json()
        if(json['result']):
            result = json['result']
            for update in result:
                if 'message' in update:
                    message = update['message']
                    if 'new_chat_participant' in message:
                        newguy = message['new_chat_participant']
                        chat_id = message['chat']['id']
                        reply_text = "Hi! "

                        if 'username' in newguy:
                            reply_text += "@" + newguy['username']
                        else:
                            reply_text += newguy['first_name']

                        reply_text += ", How are you? You are welcome to this group."
                        method_resp = 'sendMessage'
                        query_resp = {'chat_id' : chat_id, 'text' : reply_text}
                        requests.get(endpoint + '/' + method_resp, params=query_resp)
                    if 'left_chat_participant' in message:
                        thatguy = message['left_chat_participant']
                        chat_id = message['chat']['id']
                        reply_text = "User "

                        if 'username' in thatguy:
                            reply_text += "@" + thatguy['username']
                        else:
                            reply_text += thatguy['first_name']

                        reply_text += ", left the chat"
                        method_resp = 'sendMessage'
                        query_resp = {'chat_id' : chat_id, 'text' : reply_text}
                        requests.get(endpoint + '/' + method_resp, params=query_resp)
                    elif 'text' in message:
                        text = message['text']
                        spl = text.split(' ')
                        chat_id = message['chat']['id']
                        command = spl[0]
                        reply_text = ''
                        
                        if(command[:6] == '/start'):
                            reply_text = 'Hello I am @cruzex_bot. Send /help to get a list of commands.'
                        elif(command[:5] == '/help'):
                            reply_text = 'List of Commands : \n1. /rekt : Wreck someone in the chat'
                        elif(command[:5] == '/rekt'):
                            reply_text = random_rekt.random_rekt(spl,message)                          

                        method_resp = 'sendMessage'
                        query_resp = {'chat_id' : chat_id, 'text' : reply_text}
                        requests.get(endpoint + '/' + method_resp, params=query_resp)
                offset = int(update['update_id']) + 1


    except ValueError:
        print(time.ctime(), ": Broken response: ", response)
        time.sleep(60)        
    except KeyboardInterrupt:
        print(time.ctime(), ": Ctrl-C pressed - exiting")
        exit(1)
    except:
        print(time.ctime(), ": Unexpected error", sys.exc_info()[0])
        time.sleep(300)