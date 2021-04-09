import requests

def get(message, endpoint, spl, token):
    chat_id = message['chat']['id']    
    chk=0
    try:
        f = open('saved_files/' + str(chat_id) + '_' + 'notes.txt')
        lines = f.readlines()
        for line in lines:
            if(spl[1]+'\n' == line):
                chk=1
        if(chk==1):
            path = "saved_files/" + str(chat_id) + "_" + spl[1] + ".txt"
            f = open(path, 'r')
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
    finally:
        return reply_text