import requests

def promote(message,endpoint):
    chat_id = message['chat']['id'] #chat_id of the group
    user_id = message['from']['id'] #user_id of the sender
    method_resp = 'getChatMember'
    query_resp = {'chat_id' : chat_id, 'user_id' : user_id}
    response = requests.get(endpoint + '/' + method_resp, params=query_resp)
    json = response.json()
    status = str(json['result']['status']) #status of the sender

    if(status == 'administrator' or status == 'creator'):
        if('reply_to_message' in message):
            user_id = message['reply_to_message']['from']['id'] #user_id of the member to be promoted
            method_resp = 'getChatMember'
            query_resp = {'chat_id' : chat_id, 'user_id' : user_id}
            response = requests.get(endpoint + '/' + method_resp, params=query_resp)
            json = response.json()
            status = str(json['result']['status']) #status of the member to be promoted

            if(status == 'administrator' or status == 'creator' ):
                reply_text = "Sorry, The specified user is already an admin"
            else:
                method_resp = 'promoteChatMember'
                query_resp = {'chat_id' : chat_id, 'user_id' : user_id, 'can_delete_messages' : True, 'can_restrict_members' : True, 'can_change_info' : True, 'can_pin_messages' : True}
                response = requests.get(endpoint + '/' + method_resp, params=query_resp)
                json = response.json()

                if(str(json['ok']) == 'False'):
                    reply_text = str(json['description'])
                else:
                    reply_text = "Successfully Promoted!"               
        else:
            reply_text = "Please reply to the person's text while writing the command for this to work"
    else:
        reply_text = "Sorry, non-admins cannot use this command"

    return reply_text