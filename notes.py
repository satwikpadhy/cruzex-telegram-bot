def notes(chat_id):
    f = open('saved_files/' + str(chat_id) + '_' + 'notes.txt')
    lines = f.readlines()
    reply_text = 'Notes in this chat :\n'
    for line in lines:
        reply_text += '#'
        reply_text += line
    reply_text += '\nAccess them using /get notename'
    return reply_text