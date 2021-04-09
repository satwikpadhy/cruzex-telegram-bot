import requests
def save(message,endpoint,spl,token):
    if(len(spl) == 1):
        reply_text = "Please Specify the Note Name."
    else:
        note_name = spl[1] #The name of the note.
        reply_to_message = message['reply_to_message']
        '''
        method_resp = 'getFile'
        reply_to_message = message['reply_to_message']
        if 'document' in reply_to_message:
            file_id = reply_to_message['document']['file_id']
            file_name = reply_to_message['document']['file_name']
        elif 'photo' in reply_to_message:
            photo = reply_to_message['photo'][0]
            file_id = photo['file_id']
            print(file_id)
            file_name = "photo.jpg"
        elif 'audio' in reply_to_message:
            file_id = reply_to_message['audio']['file_id']
            file_name = reply_to_message['audio']['file_name']
        elif 'video' in reply_to_message:
            file_id = reply_to_message['video'][0]['file_id']
            file_name = "video.mp4"
        
        temp = file_name.split('.')
        file_name = temp[1]
        query_resp = {'file_id' : file_id}
        response = requests.get(endpoint + '/' + method_resp, params=query_resp)
        json = response.json()
        url = 'https://api.telegram.org/file/bot' + token + '/' + json['result']['file_path']
        r=requests.get(url, allow_redirects=True)
        chat_id = message['chat']['id']
        save_name = "saved_files/" + str(chat_id) + "_" + note_name + "." + file_name
        open(save_name, 'wb').write(r.content)
        reply_text = 'Save Name : ' + save_name
        '''

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
            file_id = reply_to_message['video'][0]['file_id']
            doc_type = 'vid'
        else:
            return "emror sar"

        chat_id = message['chat']['id']
        save_name = "saved_files/" + str(chat_id) + "_" + note_name + '.txt'
        open(save_name, 'w').write(doc_type + '_' + file_id)
        open('saved_files/' + str(chat_id) + "_notes.txt", 'a').write('\n' + note_name)
        reply_text = 'Save Name : ' + save_name
    return reply_text