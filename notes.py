import os
import requests
import sys
from userStatus import userStatus

def notes(chat_id,path):
    try:
        f = open(path + 'saved_files/' + str(chat_id) + '_' + 'notes.txt')
        lines = f.readlines()
        reply_text = 'Notes in this chat :\n'
        for line in lines:
            reply_text += '#'
            reply_text += line
        reply_text += '\nAccess them using /get notename'
    except FileNotFoundError:
        reply_text = "/save was never used in this chat. Use /help to get help with commands."
    finally:
        return reply_text
    
def save(message,endpoint,spl,token,path):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        if(len(spl) == 1):
            reply_text = "Please Specify the Note Name."
        else:
            note_name = spl[1] #The name of the note.
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
            save_name = path + "saved_files/" + str(chat_id) + "_" + note_name + '.txt'
            open(save_name, 'w').write(doc_type + '_' + file_id) #create a new file with file_id

            try:
                f = open(path + 'saved_files/' + str(chat_id) + "_notes.txt")
                lines = f.readlines()
                chk=0
                for line in lines:
                    if spl[1] + '\n' == line:
                        chk = 1
            except:
                chk = 0

            if chk==0:
                open(path + 'saved_files/' + str(chat_id) + "_notes.txt", 'a').write(note_name + '\n') #update the notes file
                reply_text = 'Note added Successfully,\n\nSave Name : ' + save_name
            else:
                reply_text = 'Note updated successfully, \n\nSave Name : ' + save_name
    else:
        reply_text = "Sorry, non-admins cannot use this command"  
    return reply_text

def del_note(spl,chat_id,message,endpoint,path):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator'):
        if(len(spl) == 1):
            reply_text = "Please specify the note name first."
        else:
            note_name = spl[1]
            chk=0
            try:
                f = open(path + 'saved_files/' + str(chat_id) + '_' + 'notes.txt')
                lines = f.readlines()
                t = open(path + 'saved_files/temp','w')

                for line in lines:
                    if(note_name+'\n' != line):
                        t.writelines(line)
                    else:
                        chk=1
                f.close()
                t.close()
                os.remove(path + 'saved_files/' + str(chat_id) + '_' + 'notes.txt')
                os.rename(path + 'saved_files/temp' , path + 'saved_files/' + str(chat_id) + '_' + 'notes.txt')
                if(chk==1):
                    os.remove(path + 'saved_files/' + str(chat_id) + '_' + note_name + '.txt')
                    reply_text = "Successfully Deleted."
                else:
                    reply_text = "This not doesnot exist."
            except FileNotFoundError:
                reply_text = "/save was never used in this chat. Use /help to get help with commands."
    else:
        reply_text = "Sorry, non-admins cannot use this command"
    return reply_text

def get(message, endpoint, spl, token, path):
    chat_id = message['chat']['id']    
    chk=0
    try:
        f = open(path + 'saved_files/' + str(chat_id) + '_' + 'notes.txt')
        lines = f.readlines()
        for line in lines:
            if(spl[1]+'\n' == line):
                chk=1
        if(chk==1):
            file_path = path + "saved_files/" + str(chat_id) + "_" + spl[1] + ".txt"
            f = open(file_path, 'r')
            contents = f.read()
            type = contents.split("_",1)
            file_id = type[1]
            reply_text = file_id
            doc_type = type[0]
            if(doc_type[:3] == 'img'):
                method_resp = 'sendPhoto'
                query_resp = {'chat_id' : chat_id, 'photo' : file_id, 'caption' : "Here is your note"}
            elif(doc_type[:3] == 'doc'):
                method_resp = 'sendDocument'
                query_resp = {'chat_id' : chat_id, 'document' : file_id}
            elif(doc_type[:3] == 'aud'):
                method_resp = 'sendAudio'
                query_resp = {'chat_id' : chat_id, 'audio' : file_id}
            elif(doc_type[:3] == 'vid'):
                method_resp = 'sendVideo'
                query_resp = {'chat_id' : chat_id, 'video' : file_id}
            else:
                return reply_text
            requests.get(endpoint + '/' + method_resp, params=query_resp)
            reply_text = ""
        else:
            reply_text = "This note doesnot exist."
    except FileNotFoundError:
        reply_text = "/save was never used in this chat. Use /help to get help with commands."
    except:
        reply_text = 'Unexpected error'
    finally:
        return reply_text