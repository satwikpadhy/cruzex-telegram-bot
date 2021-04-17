#!/usr/bin/env python3
import requests
import sys
from random_rekt import random_rekt
import time
from decouple import config
from promote import promote
from demote import demote
from notes import notes, save, del_note, get
from time_convert import time_convert
from pin_message import *

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

                        if(text[:1] == '#'):
                            temp = text.split('#')[1]
                            temp = temp.split(' ')[0]
                            inp = ['/get']
                            inp.append(temp)
                            reply_text = get(message,endpoint,inp,token)
                        
                        if(command[:6] == '/start'):
                            reply_text = 'Hello I am @cruzex_bot. Send /help to get a list of commands.'
                        elif(command[:5] == '/help'):
                            f = open('help')
                            lines= f.readlines()
                            for line in lines:
                                reply_text += line
                        elif(command[:5] == '/rekt'):
                            reply_text = random_rekt(spl,message)
                        elif(command[:8] == '/promote'):
                            reply_text = promote(message,endpoint)
                        elif(command[:7] == '/demote'):
                            reply_text = demote(message, endpoint)
                        elif(command[:5] == '/save'):
                            reply_text = save(message,endpoint,spl,token)
                        elif(command[:4] == '/get'):
                            reply_text = get(message,endpoint,spl,token)
                        elif(command[:6] == '/notes'):
                            reply_text = notes(message['chat']['id'])
                        elif(command[:7] == '/delete'):
                            reply_text = del_note(spl, message['chat']['id'],message,endpoint)
                        elif(command[:8] == '/convert'):
                            reply_text = time_convert(message,spl)
                        elif(command[:4] == '/pin'):
                            reply_text = pin_msg(message, spl, endpoint)
                        elif(command[:6] == '/unpin'):
                            reply_text = unpin_msg(message, endpoint)
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