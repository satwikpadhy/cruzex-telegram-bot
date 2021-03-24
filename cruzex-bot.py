#!/usr/bin/env python3
import requests
import sys

botapi_url = 'https://api.telegram.org/bot'
token = "Enter Your Bot Token here"
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
            print("result : " + str(result) + "\n\n")
            for update in result:
                if 'message' in update:
                    message = update['message']
                    if 'text' in message:
                        text = message['text']
                        spl = text.split(' ')
                        chat_id = message['chat']['id']
                        command = spl[0]
                        reply_text = ''

                        if(command[:6] == '/start'):
                            reply_text = 'Hello I am cruzex-bot. Send /help to get a list of commands.'
                        elif(command[:5] == '/help'):
                            reply_text = 'List of Commands : \n1. /rekt : Wreck someone in the chat'
                        elif(command[:5] == '/rekt'):
                            if 'username' in message['from']:
                                user_from = '@' + message['from']['username']
                            else:
                                user_from = '@' + message['from']['first_name']

                            reply_text += user_from + ' throws a bowl of hot soup on '

                            if(len(spl) == 1):
                                reply_text += 'themselves'
                            else:
                                user_rekt = spl[1]
                                reply_text += user_rekt

                        method_resp = 'sendMessage'
                        query_resp = {'chat_id' : chat_id, 'text' : reply_text}
                        requests.get(endpoint + '/' + method_resp, params=query_resp)
                offset = int(update['update_id']) + 1


    except KeyboardInterrupt:
        exit(1)
