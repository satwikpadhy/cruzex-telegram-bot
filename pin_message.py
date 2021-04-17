import requests

def pin_msg(message, spl, endpoint):
    try:
        chat_id = message['chat']['id'] #chat_id of the group
        user_id = message['from']['id'] #user_id of the sender
        method_resp = 'getChatMember'
        query_resp = {'chat_id' : chat_id, 'user_id' : user_id}
        response = requests.get(endpoint + '/' + method_resp, params=query_resp)
        json = response.json()
        status = str(json['result']['status']) #status of the sender
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
                requests.get(endpoint + '/' + method_resp, params=query_resp)
                reply_text = 'Message pinned successfully'
                if(chk == 1):
                    reply_text += ' and everyone has been notified.'
            else:
                reply_text = "Please reply to an message while using this command."
        else:
            reply_text = "Sorry, non-admins cannot use this command"
    except:
        reply_text = "Unexpected Error"
    return reply_text

def unpin_msg(message, endpoint):
    try:
        chat_id = message['chat']['id']
        method_resp = 'unpinChatMessage'
        query_resp = {'chat_id' : chat_id}
        response = requests.get(endpoint + '/' + method_resp, params=query_resp)
        json = response.json()
        if(json['result'] == True):
            reply_text = 'Last pinned message unpinned successfully'
        else:
            reply_text = str(json)
    except:
        reply_text = "unexpected error."
    return reply_text