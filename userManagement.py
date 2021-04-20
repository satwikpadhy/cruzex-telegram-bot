import pickle
import requests
import os
from userStatus import userStatus

class userInfo:
    def __init__(self, user_id, chat_id, warns):
        self.user_id = user_id
        self.chat_id = chat_id
        self.warns = warns


def banUser(message,endpoint):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        try:
            if 'reply_to_message' in message:
                chat_id = message['chat']['id']
                user_id = message['reply_to_message']['from']['id']
                if 'username' in message['reply_to_message']['from']:
                    spec_user = '@' + message['reply_to_message']['from']['username']
                else:
                    spec_user = message['reply_to_message']['from']['first_name']
                method_resp = 'kickChatMember'
                query_resp = {'chat_id' : chat_id, 'user_id' : user_id}
                response = requests.get(endpoint + '/' + method_resp, params=query_resp)
                json = response.json()
                if(json['ok'] == True):
                    reply_text = spec_user + " Banned!"
                else:
                    reply_text = str(json['description'])
            else:
                reply_text = 'Please reply to a message of the user you want to ban'
        except:
            reply_text = "Unexpected error."
    else:
        reply_text = "Who this non-admin telling me what to do"
    return reply_text

def unbanUser(message,endpoint):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        try:
            if 'reply_to_message' in message:
                chat_id = message['chat']['id']
                user_id = message['reply_to_message']['from']['id']
                if 'username' in message['reply_to_message']['from']:
                    spec_user = '@' + message['reply_to_message']['from']['username']
                else:
                    spec_user = message['reply_to_message']['from']['first_name']
                method_resp = 'unbanChatMember'
                query_resp = {'chat_id' : chat_id, 'user_id' : user_id}
                response = requests.get(endpoint + '/' + method_resp, params=query_resp)
                json = response.json()
                if(json['ok'] == True):
                    reply_text = spec_user + " UnBanned!"
                else:
                    reply_text = str(json['description'])
            else:
                reply_text = 'Please reply to a message of the user you want to unban'
        except:
            reply_text = "Unexpected error."
    else:
        reply_text = "Who this non-admin telling me what to do"
    return reply_text

def kickUser(message,endpoint):
    
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        try:
            if 'reply_to_message' in message:
                banUser(message,endpoint)
                unbanUser(message, endpoint)
                reply_text = ''
            else:
                reply_text = 'Please reply to a message of the user you want to kick'
        except:
            reply_text = "Unexpected error."
    else:
        reply_text = "Who this non-admin telling me what to do"
    return reply_text

def noOfWarns(message):
    if 'reply_to_message' in message:
        chat_id = message['chat']['id']
        user_id = message['reply_to_message']['from']['id']
        if 'username' in message['reply_to_message']['from']:
            spec_user = '@' + message['reply_to_message']['from']['username']
        else:
            spec_user = message['reply_to_message']['from']['first_name']
        save_name = "saved_files/" + str(chat_id) + '_' + str(user_id) + '_warns.txt'
        try:
            with open(save_name, 'rb') as f:
                user = pickle.load(f)
                reply_text = spec_user + " has " + str(user.warns) + ' warnings'
        except FileNotFoundError:
            reply_text = spec_user +' has never been warned'
    else:
        reply_text = 'Please reply to a message of the user you want to ban'

    return reply_text

def warnUser(message, endpoint):
    status = userStatus(message,endpoint)
    reply_text = ''
    if(status == 'administrator' or status == 'creator'):
        try:
            if 'reply_to_message' in message:
                chat_id = message['chat']['id']
                user_id = message['reply_to_message']['from']['id']
                if 'username' in message['reply_to_message']['from']:
                    spec_user = message['reply_to_message']['from']['username']
                else:
                    spec_user = message['reply_to_message']['from']['first_name']
                
                save_name = "saved_files/" + str(chat_id) + '_' + str(user_id) + '_warns.txt'
                try:
                    with open(save_name, 'rb') as f:
                        user = pickle.load(f)
                        user.warns += 1
                        warns = user.warns

                    with open(save_name, 'wb') as f:
                        pickle.dump(user, f)
                    
                except FileNotFoundError: 
                    #If file is not found then the user was never warned in the chat before.
                    user = userInfo(user_id, chat_id, 1)
                    with open(save_name, 'wb') as f:
                        pickle.dump(user, f)
                        warns = 1
                if(warns == 3):
                    reply_text = kickUser(message, endpoint)
                    os.remove(save_name)
                else:
                    reply_text = spec_user + ' has ' + str(warns) + " warnings"
            else:
                reply_text = 'Please reply to a message of the user you want to ban'
        except:
            reply_text = "Unexpected error."
    else:
        reply_text = "Who this non-admin telling me what to do"
    return reply_text

def removeWarn(message):
    if 'reply_to_message' in message:
        chat_id = message['chat']['id']
        user_id = message['reply_to_message']['from']['id']
        if 'username' in message['reply_to_message']['from']:
            spec_user = '@' + message['reply_to_message']['from']['username']
        else:
            spec_user = message['reply_to_message']['from']['first_name']
        save_name = "saved_files/" + str(chat_id) + '_' + str(user_id) + '_warns.txt'
        try:
            with open(save_name, 'rb') as f:
                user = pickle.load(f)
                
            user.warns -= 1
            with open(save_name, 'wb') as f:
                pickle.dump(user,f)
            reply_text = spec_user + " has " + str(user.warns) + ' warnings'

        except FileNotFoundError:
            reply_text = spec_user +' has never been warned'
    else:
        reply_text = 'Please reply to a message of the user you want to ban'

    return reply_text