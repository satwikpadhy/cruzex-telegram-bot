import os
import requests
import sys
from userStatus import userStatus
import json as js

def notes(chat_id,path,endpoint):
    try:
        f = open(path + '/saved_files/' + str(chat_id) + '_' + 'notes.txt')
        lines = f.readlines()
        rows = []
        keyboard= []
        i = 1
        for line in lines:
            button = {'text' : line, 'callback_data' : line}
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
        response = requests.get(endpoint + '/' + method_resp, params=query_resp)
        json = response.json()
        reply_text = str(json)
        reply_text = ''
    except FileNotFoundError:
        reply_text = "/save was never used in this chat. Use /help to get help with commands."
    finally:
        return reply_text

def save(message,endpoint,spl,token,path):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator' or message['chat']['type'] == 'private'):
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
            save_name = path + "/saved_files/" + str(chat_id) + "_" + note_name + '.txt'
            open(save_name, 'w').write(doc_type + '_' + file_id) #create a new file with file_id

            try:
                f = open(path + '/saved_files/' + str(chat_id) + "_notes.txt") #checking if the notename already existed
                lines = f.readlines()
                chk=0
                for line in lines:
                    if spl[1] + '\n' == line:
                        chk = 1 #If note exits set chk to 1 so that a new entry with the same name is not added
                f.close()
            except:
                chk = 0

            if chk==0: #This portion is executed ONLY if the note doesnt exist already
                try:
                    f = open(path + '/saved_files/' + str(chat_id) + "_notes.txt")
                    lines = f.readlines()

                    if note_name.lower() < lines[0].lower():
                        #If notename lower than first element of notes file, add at the beginning of the file
                        f2 = open(path + '/saved_files/' + str(chat_id) + '_temp.txt', 'w')
                        f2.write(note_name + '\n')
                        for line in lines:
                            f2.write(line)
                        f.close()
                        f2.close()
                        os.remove(path + '/saved_files/' + str(chat_id) + "_notes.txt")
                        os.rename(path + '/saved_files/' + str(chat_id) + '_temp.txt', path + '/saved_files/' + str(chat_id) + "_notes.txt")
                        
                    elif note_name.lower() > lines[len(lines) - 1].lower():
                        #If notename higher than last element of notes file, add at the end of the file
                        open(path + '/saved_files/' + str(chat_id) + "_notes.txt", 'a').write(note_name + '\n')
                    else:
                        f2 = open(path + '/saved_files/' + str(chat_id) + '_temp.txt', 'w')
                        for i in range(0, len(lines)):
                            f2.write(lines[i])
                            if(note_name.lower() > lines[i].lower() and note_name.lower() < lines[i+1].lower()):
                                f2.write(note_name + '\n')
                        f.close()
                        f2.close()
                        os.remove(path + '/saved_files/' + str(chat_id) + "_notes.txt")
                        os.rename(path + '/saved_files/' + str(chat_id) + '_temp.txt', path + '/saved_files/' + str(chat_id) + "_notes.txt")
                        
                    reply_text = 'Note added Successfully!'
                except FileNotFoundError:
                    f = open(path + '/saved_files/' + str(chat_id) + "_notes.txt", 'w') #If save was never used in the chat :
                    f.write(note_name + '\n')
                    f.close()
                    reply_text = 'Note added Successfully!. Use /notes to access your notes'
            else:
                reply_text = 'Note updated successfully!'
    else:
        reply_text = "Sorry, non-admins cannot use this command"
    return reply_text

def del_note(spl,chat_id,message,endpoint,path):
    status = userStatus(message,endpoint)
    if(status == 'administrator' or status == 'creator' or message['chat']['type'] == 'private'):
        if(len(spl) == 1):
            reply_text = "Please specify the note name first."
        else:
            note_name = spl[1]
            chk=0
            try:
                f = open(path + '/saved_files/' + str(chat_id) + '_' + 'notes.txt')
                lines = f.readlines()
                t = open(path + '/saved_files/temp','w')

                for line in lines:
                    if(note_name+'\n' != line):
                        t.writelines(line)
                    else:
                        chk=1
                f.close()
                t.close()
                os.remove(path + '/saved_files/' + str(chat_id) + '_' + 'notes.txt')
                os.rename(path + '/saved_files/temp' , path + '/saved_files/' + str(chat_id) + '_' + 'notes.txt')
                if(chk==1):
                    os.remove(path + '/saved_files/' + str(chat_id) + '_' + note_name + '.txt')
                    reply_text = "Note is successfully deleted."
                else:
                    reply_text = "This note doesnot exist."
            except FileNotFoundError:
                reply_text = "/save was never used in this chat. Use /help to get help with commands."
    else:
        reply_text = "Sorry, non-admins cannot use this command"
    return reply_text

def get(chat_id, endpoint, spl, token, path):
    #chat_id = message['chat']['id']
    chk=0
    try:
        f = open(path + '/saved_files/' + str(chat_id) + '_' + 'notes.txt')
        lines = f.readlines()
        for line in lines:
            if(spl[1]+'\n' == line):
                chk=1
        if(chk==1):
            file_path = path + "/saved_files/" + str(chat_id) + "_" + spl[1] + ".txt"
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
            reply_text = ''
        else:
            reply_text = "This note doesnot exist."
    except FileNotFoundError:
        reply_text = "/save was never used in this chat. Use /help to get help with commands."
    except:
        reply_text = 'Unexpected error'
    finally:
        return reply_text
