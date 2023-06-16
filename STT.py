import speech_recognition as sr
from gtts import gTTS
from Connect import sheet
import os
import datetime

def STT(r_num):

    # Create an audio recogniaer
    r = sr.Recognizer()

    #obtain audio from the microphone    
    counter = 0
    while(counter < 3):

        if (counter == 0):
            cmd = '請說想要提醒的藥品名稱 (ex:)感冒藥'
            tts = gTTS(text=cmd, lang='zh-TW')
            tts.save('ask1.mp3')
            ask_mp3 = 'ask1.mp3'
            c_num = 'A'
        elif (counter == 1):
            cmd = '請說想要提醒的日期 (ex:)2023年01月01日'
            tts = gTTS(text=cmd, lang='zh-TW')
            tts.save('ask2.mp3')
            ask_mp3 = 'ask2.mp3'
            c_num = 'B'
        elif (counter == 2):
            cmd = '請說想要提醒的時間 (ex:)13點30分'
            tts = gTTS(text=cmd, lang='zh-TW')
            tts.save('ask3.mp3') 
            ask_mp3 = 'ask3.mp3'
            c_num = 'C'     

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1) 
            os.system('omxplayer -o local -p ' + ask_mp3)
            print(cmd)
            audio=r.listen(source, timeout = 5)

        # recognize speech using Google Speech Recognition 
        text = r.recognize_google(audio, language='zh-TW')
        print(text)

        counter = counter + 1

        # Write data in Google sheet
        #cell = sheet.cell(row=r_num, column=c_num)
        index = c_num + str(r_num)
        print("index:", index)
        sheet.update(index, text)

    # update GetMidincine value = 0
    GetMidincine = 'D'+str(r_num) 
    sheet.update(GetMidincine, 0)
    # update Remind_times = 0
    Remind_times = 'F'+ str(r_num)
    sheet.update(Remind_times, 0)
    # update location
    print("請將藥品放入第"+str(r_num-1)+"格")
    location = 'E'+ str(r_num)
    sheet.update(location, r_num-1)
    print("已經記錄完成!٩(ˊᗜˋ )و")
    return 0