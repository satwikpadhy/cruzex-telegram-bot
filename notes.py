def notes(chat_id):
    try:
        f = open('saved_files/' + str(chat_id) + '_' + 'notes.txt')
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