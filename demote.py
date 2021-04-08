import requests

def demote(message,endpoint):
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
            
            if(status == 'administrator'):
                method_resp = 'promoteChatMember'
                query_resp = {'chat_id' : chat_id, 'user_id' : user_id, 'can_delete_messages' : False, 'can_restrict_members' : False, 'can_change_info' : False, 'can_pin_messages' : False}
                response = requests.get(endpoint + '/' + method_resp, params=query_resp)
                json = response.json()

                if(str(json['ok']) == 'False'):
                    reply_text = str(json['description'])
                else:
                    reply_text = "Successfully Demoted!"
            elif(status == 'creator'):
                reply_text = "Sorry, cannot demote the Owner  of this group"
            else:
                reply_text = "Sorry, The specified person is not an admin"
            
        else:
            reply_text = "Please reply the the person's text while writing the command for this to work"
    else:
        reply_text = "Sorry, non-admins cannot use this command"

    return reply_text