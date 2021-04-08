#!/usr/bin/env python3
import requests
import sys
import random_rekt
import time
from decouple import config
import promote
from demote import demote

botapi_url = 'https://api.telegram.org/bot'
token = config('token')
endpoint = botapi_url + token
offset = 0
method = 'getUpdates'
request = endpoint + '/' + method

while(True):
    try:
        query = {'offset': offset}
        response = requests.get(request, params=query)
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
                            reply_text = 'List of Commands : \n1. /rekt : Wreck someone in the chat by either replying to their text or writing their username after the command'
                            reply_text += '\n2. /promote : Promote a chat member by replying to their message with /promote'
                            reply_text += '\n3. /demote : Demote someone from admin by replying to their messages with /demote'
                            reply_text += '\n\nExtra Features : \nWelcome and Parting Messages when a user joins or leaves the group\n'
                        elif(command[:5] == '/rekt'):
                            reply_text = random_rekt.random_rekt(spl,message)
                        elif(command[:8] == '/promote'):
                            reply_text = promote.promote(message,endpoint)
                        elif(command[:7] == '/demote'):
                            reply_text = demote(message, endpoint)                          

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