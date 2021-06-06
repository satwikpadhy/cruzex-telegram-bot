import requests
from userStatus import userStatus
import sys

def pin_msg(message, spl, endpoint):
    try:
        status = userStatus(message,endpoint)
        if(status == 'administrator' or status == 'creator'):
            if('reply_to_message' in message):
                chat_id = message['chat']['id']
                message_id = message['reply_to_message']['message_id']
                method_resp = 'pinChatMessage'
                chk=0
                
                if(len(spl) == 1):
                    query_resp = {'chat_id' : chat_id, 'message_id' : message_id, 'disable_notification' : True}   
                else:
                    if(spl[1] == 'loud'):
                        query_resp = {'chat_id' : chat_id, 'message_id' : message_id}
                        chk = 1
                    else:
                        query_resp = {'chat_id' : chat_id, 'message_id' : message_id, 'disable_notification' : True}
                json = requests.get(endpoint + '/' + method_resp, params=query_resp).json()
                if json['ok'] == True:
                    reply_text = ''
                else:
                    reply_text = json['description']
            else:
                reply_text = "Please reply to an message while using this command."
        else:
            reply_text = "Sorry, non-admins cannot use this command"
    except:
        reply_text = str(sys.exc_info())
    return reply_text

def unpin_msg(message, endpoint):
    try:
        status = userStatus(message,endpoint)
        if(status == 'administrator' or status == 'creator'):
            chat_id = message['chat']['id']
            method_resp = 'unpinChatMessage'
            query_resp = {'chat_id' : chat_id}
            response = requests.get(endpoint + '/' + method_resp, params=query_resp)
            json = response.json()
            if json['ok'] == True:
                reply_text = 'Last pinned message unpinned successfully.'
            else:
                reply_text = json['description']
        else:
            reply_text = "Sorry, non-admins cannot use this command"
    except:
        reply_text = str(sys.exc_info())
    return reply_text