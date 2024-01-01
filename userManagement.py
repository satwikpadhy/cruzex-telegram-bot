import sys
import requests
from userStatus import userStatus
import json
from datetime import datetime, timedelta
import psycopg2
from decouple import config

dbname = config('database')
user = config('user')
host = config('host')
password = config('password')
port = config('port')

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

def unbanUser(message,endpoint,kick = False): #if kick is true then the user is kicked
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

def noOfWarns(message, endpoint):
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
            
            conn = psycopg2.connect(
            database = dbname, 
            user = user, 
            host= host,
            password = password,
            port = port
            )      
            cursor = conn.cursor()

            cursor.execute('select no_warns from warns where chat_id = %s and user_id = %s', (str(chat_id),str(user_id)))
            lines = cursor.fetchall()
            reply_text = spec_user + ' has ' + str(lines[0][0]) + ' warnings.'
    else:
        reply_text = 'Please reply to a message of the user you want to ban'

    return reply_text

def warnUser(message, endpoint):
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

                    conn = psycopg2.connect(
                    database = dbname, 
                    user = user, 
                    host= host,
                    password = password,
                    port = port
                    )      
                    cursor = conn.cursor()
                    cursor.execute('select no_warns from warns where chat_id = %s and user_id = %s', (str(chat_id),str(user_id)))
                    rowcount = cursor.rowcount
                    
                    if rowcount == 0: #Warn was never used for this user in this chat.
                        cursor.execute('insert into warns values (%s,%s,1)' , (str(chat_id),str(user_id)))
                        cursor.close()
                        conn.commit()
                        reply_text = 'Warn was never used before. Adding one warn'
                    else:
                        cursor.execute('select no_warns from warns where chat_id = %s and user_id = %s', (str(chat_id),str(user_id)))
                        lines = cursor.fetchall()
                        warns = lines[0][0] + 1
                        if(warns >= 3):
                            reply_text = unbanUser(message, endpoint, True)
                            cursor.execute('delete from warns where chat_id = %s and user_id = %s', (str(chat_id),str(user_id)))
                            cursor.close()
                            conn.commit()
                        else:
                            cursor.execute('update warns set no_warns = %s where chat_id = %s and user_id = %s', (warns,str(chat_id),str(user_id)))
                            cursor.close()
                            conn.commit()
                            reply_text = 'adding one warn'
                    conn.close()
            else:
                reply_text = 'Please reply to a message of the user you want to warn.'
        except:
            reply_text = str(sys.exc_info())
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
        # save_name = path + "/saved_files/" + str(chat_id) + '_' + str(user_id) + '_warns.txt'
        try:
            conn = psycopg2.connect(
                    database = dbname, 
                    user = user, 
                    host= host,
                    password = password,
                    port = port
            )      
            cursor = conn.cursor()
            cursor.execute('select no_warns from warns where chat_id = %s and user_id = %s', (str(chat_id),str(user_id)))
            warns = cursor.fetchall()[0][0]
            if(warns == 0):
                reply_text = spec_user + " has no warnings."
            else:
                warns -= 1
                cursor.execute('update warns set no_warns = %s where chat_id = %s and user_id = %s', (warns,str(chat_id),str(user_id)))
                cursor.close()
                conn.commit()
                reply_text = spec_user + " has " + str(warns) + ' warnings'

        except :
            reply_text = str(sys.exc_info())
    else:
        reply_text = 'Please reply to a message of the user you want to remove the warn from.'

    return reply_text

def muteUser(message,endpoint,spl):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        if 'reply_to_message' in message:
            if len(spl) == 1:
                duration = 'None'
            else:
                duration = spl[1]
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

                now = datetime.now()
                offset = 0
                unit = 'N'
                for ch in duration:
                    if ch.isdigit():
                        temp = ch
                        offset = offset * 10
                        offset = offset + int(temp)
                    elif ch.isalpha():
                        unit = ch
                        break
                        
                #unit accepts m, h, d
                if unit == 'm':
                    now = now + timedelta(minutes = offset)
                    unit = 'minutes'
                elif unit == 'h':
                    now = now + timedelta(hours = offset)
                    unit = 'hours'
                elif unit == 'd':
                    now = now + timedelta(days = offset)
                    unit = 'days'                   
                
                unix_time = datetime.timestamp(now)
                
                perm = json.dumps(permissions)
                method_resp = 'restrictChatMember'
                query_resp = {'chat_id' : chat_id, 'user_id' : user_id, 'permissions' : perm, 'until_date' : unix_time}
                response = requests.get(endpoint + '/' + method_resp, params=query_resp)
                json_file = response.json()
                if(json_file['ok'] == True):
                    if offset == 0:
                        reply_text = spec_user + ' indefinitely muted'
                    else:
                        reply_text = spec_user + ' muted for ' + str(offset) + ' ' + unit
                else:
                    reply_text = str(json_file)
        else:
            reply_text = 'Please reply to a message of the user you want to mute '
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