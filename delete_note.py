import os
def del_note(spl,chat_id):
    if(len(spl) == 1):
        reply_text = "Please specify the note name first."
    else:
        note_name = spl[1]
        chk=0
        try:
            f = open('saved_files/' + str(chat_id) + '_' + 'notes.txt')
            lines = f.readlines()
            t = open('saved_files/temp','w')

            for line in lines:
                if(note_name+'\n' != line):
                    t.writelines(line)
                else:
                    chk=1
            f.close()
            t.close()
            os.remove('saved_files/' + str(chat_id) + '_' + 'notes.txt')
            os.rename('saved_files/temp' , 'saved_files/' + str(chat_id) + '_' + 'notes.txt')
            if(chk==1):
                os.remove('saved_files/' + str(chat_id) + '_' + note_name + '.txt')
                reply_text = "Successfully Deleted."
            else:
                reply_text = "This not doesnot exist."
        except FileNotFoundError:
            reply_text = "/save was never used in this chat. Use /help to get help with commands."
    return reply_text