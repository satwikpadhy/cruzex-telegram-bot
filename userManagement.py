import sys
import pickle
import requests
import os
from userStatus import userStatus
import json

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
                admin_check = userStatus(message['reply_to_message'], endpoint)
                if(admin_check == 'administrator' or admin_check == 'creator'):
                    reply_text = 'Ah! these admins are too powerful for me :('
                else:
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

def unbanUser(message,endpoint,kick = False):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        try:
            if 'reply_to_message' in message:
                admin_check = userStatus(message['reply_to_message'], endpoint)
                if(admin_check == 'administrator' or admin_check == 'creator'):
                    reply_text = 'Ah! these admins are too powerful for me :('
                else:
                    chat_id = message['chat']['id']
                    user_id = message['reply_to_message']['from']['id']
                    if 'username' in message['reply_to_message']['from']:
                        spec_user = '@' + message['reply_to_message']['from']['username']
                    else:
                        spec_user = message['reply_to_message']['from']['first_name']
                    method_resp = 'unbanChatMember'
                    if kick == True:
                        query_resp = {'chat_id' : chat_id, 'user_id' : user_id,}
                    else:
                        query_resp = {'chat_id' : chat_id, 'user_id' : user_id, 'only_if_banned' : True}
                    response = requests.get(endpoint + '/' + method_resp, params=query_resp)
                    json = response.json()
                    if(json['ok'] == True):
                        if(kick == True):
                            reply_text = ''
                        else:
                            reply_text = spec_user + " UnBanned!"
                    else:
                        reply_text = str(json['description'])
            else:
                reply_text = 'Please reply to a message of the user you want to'
                if(kick == True):
                    reply_text += ' kick.'
                else:
                    reply_text += ' unban.'
        except:
            reply_text = "Unexpected error."
    else:
        reply_text = "Who this non-admin telling me what to do"
    return reply_text

def noOfWarns(message, path, endpoint):
    if 'reply_to_message' in message:
        admin_check = userStatus(message['reply_to_message'], endpoint)
        if(admin_check == 'administrator' or admin_check == 'creator'):
            reply_text = 'Ah! these admins are too powerful for me :('
        else:
            chat_id = message['chat']['id']
            user_id = message['reply_to_message']['from']['id']
            if 'username' in message['reply_to_message']['from']:
                spec_user = '@' + message['reply_to_message']['from']['username']
            else:
                spec_user = message['reply_to_message']['from']['first_name']
            save_name = path + "saved_files/" + str(chat_id) + '_' + str(user_id) + '_warns.txt'
            try:
                with open(save_name, 'rb') as f:
                    user = pickle.load(f)
                    reply_text = spec_user + " has " + str(user.warns) + ' warnings'
            except FileNotFoundError:
                reply_text = spec_user +' has never been warned'
    else:
        reply_text = 'Please reply to a message of the user you want to ban'

    return reply_text

def warnUser(message, endpoint, path):
    status = userStatus(message,endpoint)
    reply_text = ''
    if(status == 'administrator' or status == 'creator'):
        try:
            if 'reply_to_message' in message:
                admin_check = userStatus(message['reply_to_message'], endpoint)
                if(admin_check == 'administrator' or admin_check == 'creator'):
                    reply_text = 'Ah! these admins are too powerful for me :('
                else:
                    chat_id = message['chat']['id']
                    user_id = message['reply_to_message']['from']['id']
                    if 'username' in message['reply_to_message']['from']:
                        spec_user = '@' + message['reply_to_message']['from']['username']
                    else:
                        spec_user = message['reply_to_message']['from']['first_name']
                    
                    save_name = path + "saved_files/" + str(chat_id) + '_' + str(user_id) + '_warns.txt'
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
                        reply_text = unbanUser(message, endpoint, True)
                        os.remove(save_name)
                    else:
                        reply_text = spec_user + ' has ' + str(warns) + " warnings"
            else:
                reply_text = 'Please reply to a message of the user you want to warn.'
        except:
            reply_text = str(sys.exc_info())
    else:
        reply_text = "Who this non-admin telling me what to do"
    return reply_text

def removeWarn(message, path):
    if 'reply_to_message' in message:
        chat_id = message['chat']['id']
        user_id = message['reply_to_message']['from']['id']
        if 'username' in message['reply_to_message']['from']:
            spec_user = '@' + message['reply_to_message']['from']['username']
        else:
            spec_user = message['reply_to_message']['from']['first_name']
        save_name = path + "saved_files/" + str(chat_id) + '_' + str(user_id) + '_warns.txt'
        try:
            with open(save_name, 'rb') as f:
                user = pickle.load(f)

            if(user.warns == 0):
                reply_text = spec_user + " has no warnings."
            else:
                user.warns -= 1
                with open(save_name, 'wb') as f:
                    pickle.dump(user,f)
                reply_text = spec_user + " has " + str(user.warns) + ' warnings'

        except FileNotFoundError:
            reply_text = spec_user +' has never been warned'
    else:
        reply_text = 'Please reply to a message of the user you want to remove the warn from.'

    return reply_text

def muteUser(message,endpoint):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        if 'reply_to_message' in message:
            chat_id = message['chat']['id']
            user_id = message['reply_to_message']['from']['id']
            admin_check = userStatus(message['reply_to_message'], endpoint)
            if(admin_check == 'administrator' or admin_check == 'creator'):
                reply_text = 'Ah! these admins are too powerful for me :('
            else:
                if 'username' in message['reply_to_message']['from']:
                    spec_user = '@' + message['reply_to_message']['from']['username']
                else:
                    spec_user = message['reply_to_message']['from']['first_name']

                permissions = {
                            'can_send_messages' : False,
                            'can_send_media_messages' : False,
                            'can_send_polls' : False,
                            'can_send_other_messages' : False,
                            'can_add_web_page_previews' : False,
                            'can_change_info' : False,
                            'can_invite_users' : False,
                            'can_pin_messages' : False
                }

                perm = json.dumps(permissions)
                method_resp = 'restrictChatMember'
                query_resp = {'chat_id' : chat_id, 'user_id' : user_id, 'permissions' : perm}
                response = requests.get(endpoint + '/' + method_resp, params=query_resp)
                json_file = response.json()
                if(json_file['ok'] == True):
                    reply_text = spec_user + ' muted successfully'
                else:
                    reply_text = str(json_file)
        else:
            reply_text = 'Please reply to a message of the user you want to mute'
    else:
        reply_text = "Who this non-admin telling me what to do"
    return reply_text

def unmuteUser(message,endpoint):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        if 'reply_to_message' in message:
            chat_id = message['chat']['id']
            user_id = message['reply_to_message']['from']['id']
            admin_check = userStatus(message['reply_to_message'], endpoint)
            if(admin_check == 'administrator' or admin_check == 'creator'):
                reply_text = 'Cannot unmute the one who cannot be muted.'
            else:
                if 'username' in message['reply_to_message']['from']:
                    spec_user = '@' + message['reply_to_message']['from']['username']
                else:
                    spec_user = message['reply_to_message']['from']['first_name']

                permissions = {
                            'can_send_messages' : True,
                            'can_send_media_messages' : True,
                            'can_send_polls' : True,
                            'can_send_other_messages' : True,
                            'can_add_web_page_previews' : True,
                            'can_change_info' : True,
                            'can_invite_users' : True,
                            'can_pin_messages' : True
                }

                perm = json.dumps(permissions)
                method_resp = 'restrictChatMember'
                query_resp = {'chat_id' : chat_id, 'user_id' : user_id, 'permissions' : perm}
                response = requests.get(endpoint + '/' + method_resp, params=query_resp)
                json_file = response.json()
                if(json_file['ok'] == True):
                    reply_text = spec_user + ' unmuted successfully'
                else:
                    reply_text = str(json_file)
        else:
            reply_text = 'Please reply to a message of the user you want to mute'
    else:
        reply_text = "Who this non-admin telling me what to do"
    return reply_text