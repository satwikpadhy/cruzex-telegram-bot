import requests
def userStatus(message,endpoint):
    chat_id = message['chat']['id'] #chat_id of the group
    user_id = message['from']['id'] #user_id of the sender
    method_resp = 'getChatMember'
    query_resp = {'chat_id' : chat_id, 'user_id' : user_id}
    response = requests.get(endpoint + '/' + method_resp, params=query_resp)
    json = response.json()
    status = str(json['result']['status']) #status of the sender
    return status