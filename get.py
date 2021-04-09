import requests

def get(message, endpoint, spl, token):
    chat_id = message['chat']['id']
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
    else:
        reply_text = "Doc type not supported yet"
        return reply_text
    response = requests.get(endpoint + '/' + method_resp, params=query_resp)
    json = response.json()
    return str(json)
    #return reply_text