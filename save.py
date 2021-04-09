import requests
def save(message,endpoint,spl,token):
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
        save_name = "saved_files/" + str(chat_id) + "_" + note_name + '.txt'
        open(save_name, 'w').write(doc_type + '_' + file_id) #create a new file with file_id
        open('saved_files/' + str(chat_id) + "_notes.txt", 'a').write(note_name + '\n') #update the notes file
        reply_text = 'Save Name : ' + save_name
    return reply_text