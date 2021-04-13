def convert(time_value):
    time = time_value
    hh = time[:2]
    mm = time[2] + time[3]
    hh_int = int(hh)
    mm_int = int(mm)
    if(hh_int >= 24 or mm_int >= 60):
        reply_text = "Time format is wrong"
        return reply_text
    elif(hh_int > 12):
        hh_int = hh_int-12
        tt = 'pm'
    elif(hh_int == 0):
        hh_int = 12
        tt = 'am'
    else:
        tt = 'am'
    hh = str(hh_int)
    return hh + ":" + mm + tt

def time_convert(message,spl):
    reply_text = ''
    if(len(spl) == 1):
        if 'reply_to_message' in message:
            try:
                reply_split = message['reply_to_message']['text'].split(" ")
                for word in reply_split:
                    if(word[1].isdigit()):
                        reply_text += word + ' = ' + convert(word) + '\n'
            except IndexError:
                reply_text = "Please enter the time properly"
    else:
        if(len(spl) == 1):
                reply_text = "Please give some input"
        else:
            try:
                reply_text = convert(spl[1])
            except ValueError:
                reply_text = "Time is format wrong.Try giving time in correct format. e.g 1500"

    return reply_text