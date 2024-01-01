import requests
import sys
import psycopg2
from userStatus import userStatus
import json as js
from decouple import config

dbname = config('database')
user = config('user')
host = config('host')
password = config('password')
port = config('port')


def notes(chat_id,endpoint):
    try:
        reply_text = ''
        conn = psycopg2.connect(
            database = dbname, 
            user = user, 
            host= host,
            password = password,
            port = port
        )      
        cursor = conn.cursor()
        cursor.execute("select notename from savednotes where chat_id = %s" , (str(chat_id),))
        rowcount = cursor.rowcount
        if rowcount == 0:
            reply_text = '/save was never used in this chat.'
        else:
            lines = cursor.fetchall()
            rows = []
            keyboard= []
            i = 1
            for line in lines:
                button = {'text' : str(line[0]), 'callback_data' : str(line[0])}
                rows.append(button)
                if (i%3 == 0 and i != 1):
                    keyboard.append(rows)
                    rows = []
                i = i+1
            keyboard.append(rows)
            inlineKeyboardMarkup = {'inline_keyboard' : keyboard}
            text = 'Notes in this chat :'
            method_resp = 'sendMessage'
            query_resp = {'chat_id' : chat_id, 'text' : text, 'reply_markup' : js.dumps(inlineKeyboardMarkup)}
            requests.get(endpoint + '/' + method_resp, params=query_resp)
        cursor.close()
        conn.close()
        return reply_text
    except :
        reply_text = "Unexpected error" + str(sys.exc_info())

def save(message,endpoint,spl):
    try:
        reply_text = ''
        status = userStatus(message,endpoint)
        if(status == 'administrator' or status == 'creator' or message['chat']['type'] == 'private'):
            if(len(spl) == 1):
                reply_text = "Please Specify the Note Name."
            else:
                note_name = spl[1] #The name of the note.
                print(message)
                if('reply_to_message' in message):
                    reply_to_message = message['reply_to_message']
                    if 'document' in reply_to_message:
                        file_id = reply_to_message['document']['file_id']
                        doc_type = 'doc'
                    elif 'photo' in reply_to_message:
                        photo = reply_to_message['photo'][0]
                        file_id = photo['file_id']
                        doc_type = 'img'
                    elif 'audio' in reply_to_message:
                        file_id = reply_to_message['audio']['file_id']
                        doc_type = 'aud'
                    elif 'video' in reply_to_message:
                        file_id = reply_to_message['video']['file_id']
                        doc_type = 'vid'
                    else:
                        file_id = reply_to_message['text']
                        doc_type = 'txt'

                    chat_id = message['chat']['id']

                    conn = psycopg2.connect(
                        database = dbname, 
                        user = user, 
                        host= host,
                        password = password,
                        port = port
                    )
                    
                    cursor = conn.cursor()
                    try:
                        cursor.execute( 'insert into savednotes values(%s,%s,%s,%s)' , (str(chat_id), note_name, str(file_id), doc_type))
                    except psycopg2.errors.UniqueViolation:
                        print("Note already exists") 
                        conn.rollback()
                        cursor.execute("update savednotes set data = %s, type = %s where chat_id = %s and notename = %s" , (str(file_id), doc_type, str(chat_id), note_name))
                    except:
                        reply_text = "Unexpected error" + str(sys.exc_info())
                    finally:
                        cursor.close()
                        conn.commit()
                        reply_text = 'Note saved successfully!'
                    conn.close()
                else:
                    reply_text = 'Please reply to the message/file you want to save while using this command'
                
        else:
            reply_text = "Sorry, non-admins cannot use this command"
        return reply_text
    except:
        return "Unexpected error" + str(sys.exc_info()[0])

def del_note(spl,message,endpoint):
    chat_id = message['chat']['id']
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator' or message['chat']['type'] == 'private'):
        if(len(spl) == 1):
            reply_text = "Please specify the note name first."
        else:
            try:
                note_name = spl[1]
                conn = psycopg2.connect(
                    database = dbname, 
                    user = user, 
                    host= host,
                    password = password,
                    port = port
                )
                cursor = conn.cursor()
                cursor.execute("delete from savednotes where chat_id = %s and notename = %s", (str(chat_id),note_name))
                rowcount = cursor.rowcount
                cursor.close()
                if rowcount == 0:
                    reply_text = 'Note doesnot exist. Please check the notename'
                else:
                    conn.commit()
                    reply_text = 'Note deleted successfully!!'
                conn.close()
            except:
                reply_text = "Unexpected error" + str(sys.exc_info())
            # finally:
            #     conn.close()
    else:
        reply_text = "Sorry, non-admins cannot use this command"
    return reply_text

def get(chat_id, endpoint, notename):
    reply_text = ''
    try:
        conn = psycopg2.connect(
            database = dbname, 
            user = user, 
            host= host,
            password = password,
            port = port
        )
                
        cursor = conn.cursor()
        cursor.execute("select data, type from savednotes where chat_id = %s and notename = %s" , (str(chat_id),notename))
        rows = cursor.fetchall()
        if( rows ):
            doc_type = rows[0][1]
            file_id = rows[0][0]
            reply_text = "Here is your saved text :\n\n" + file_id #used for the case when the note is a saved text.
            if(doc_type == 'img'):
                method_resp = 'sendPhoto'
                query_resp = {'chat_id' : chat_id, 'photo' : file_id, 'caption' : "Here is your note"}
            elif(doc_type == 'doc'):
                method_resp = 'sendDocument'
                query_resp = {'chat_id' : chat_id, 'document' : file_id, 'caption' : "Here is your note"}
            elif(doc_type == 'aud'):
                method_resp = 'sendAudio'
                query_resp = {'chat_id' : chat_id, 'audio' : file_id, 'caption' : "Here is your note"}
            elif(doc_type == 'vid'):
                method_resp = 'sendVideo'
                query_resp = {'chat_id' : chat_id, 'video' : file_id, 'caption' : "Here is your note"}
            else:
                return reply_text
            requests.get(endpoint + '/' + method_resp, params=query_resp)
            reply_text = ''
        else:
            print("Note doesnpt exist")
        cursor.close()
        conn.close()
    except:
        reply_text = "Unexpected error" + str(sys.exc_info())
    finally:
        
        return reply_text
