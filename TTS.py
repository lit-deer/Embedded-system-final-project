# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS

from gtts import gTTS
from Connect import sheet
import os
from datetime import datetime, timezone, timedelta, tzinfo

import imutils
import time
import cv2
#import TTS

#from keras.models import load_model
import tensorflow as tf
import numpy as np

#抓取吃藥提醒的時間
def TTS():
    data = sheet.get_all_records()

    #for row in data:
        #print(row['藥品'], " ", row['提醒日期'], " ", row['提醒時間'], " ", row['是否已經吃藥'], " ")

    #比對提醒日期和時間
    time_zone = timezone(timedelta(hours=+8))
    now = datetime.now(time_zone)
    print("now : ", now)
    today = str(now.year) + '年' + str(now.month) + '月' + str(now.day) +'日'
    print("today : ", today)
    time = now
    #remind_time = now + timedelta(minutes=5)
    time2 = str(time.hour) + '點' + str(time.minute) + '分'
    print("time : ", time2)

    counter = 1
    check = False
    for row in data:
        print(row['藥品'], " ", row['提醒日期'], " ", row['提醒時間'], " ", row['是否已經吃藥'], " ")
        counter = counter + 1
        if (str(row['提醒日期']) == str(today)):
            print("日期相同!")

            t = str(row['提醒時間'])
            h = int(t[:t.find('點')])
            m = int(t[t.find('點')+1:t.find('分')])

            if (time.hour>=h and time.minute>=m):
                print("時間相同!")
                if(row['是否已經吃藥'] == 0):
                    print("還沒有吃藥!")
                    if(row["提醒次數"] == 0):
                        check = True
                        print("還沒有提醒過!")
                        index = 'F' + str(counter)
                        sheet.update(index, 1)
                    
                        remind_text = '提醒您!請記得在10分鐘內，吃'+str(row['藥品'])
                        print("remind_text : ", remind_text)
                        tts = gTTS(text=remind_text, lang='zh-TW')
                        tts.save('reminder.mp3')
                        os.system('omxplayer -o local -p reminder.mp3')

                        break
                    elif(row["提醒次數"] > 0):
                        #超過時間(10min)沒吃藥
                        check = True
                        print("已經提醒過了!")
                        index = 'F' + str(counter)
                        sheet.update(index, 2)
                    
                        remind_text = '您忘記吃藥囉!請記得吃'+str(row['藥品'])
                        print("remind_text : ", remind_text)
                        tts = gTTS(text=remind_text, lang='zh-TW')
                        tts.save('reminder.mp3')
                        os.system('omxplayer -o local -p reminder.mp3')

                        break

    #print("離開TTS")
    if check == False: 
        counter = 0
    return counter

def medicine(counter):
    model = tf.keras.models.load_model('keras_model.h5', compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    #try:
        # created a *threaded *video stream, allow the camera sensor to warmup,
        # and start the FPS counter
    print("[INFO] sampling frames from PiVideoStream module...")
    vs = PiVideoStream().start()
    time.sleep(2.0)
    status = True

    # loop over some frames...this time using the threaded stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        pos = sheet.cell(counter, 5).value
        print(pos)
        if pos=='1': 
            frame1 = frame[0:, 0:46]
        elif pos=='2': 
            frame1 = frame[0:, 46:91]
        elif pos=='3': 
            frame1 = frame[0:, 91:137]
        elif pos=='4': 
            frame1 = frame[0:, 137:183]
        elif pos=='5': 
            frame1 = frame[0:, 183:228]
        elif pos=='6': 
            frame1 = frame[0:, 228:274]
        elif pos=='7': 
            frame1 = frame[0:, 274:320]       
        cv2.imshow("split", frame1)
        
        image = cv2.resize(frame1, (224, 224))
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        y,n= prediction[0]    # 印出每個項目的數值資訊
        print(y,n)
        if y>0.5:              # 判斷有藥
            print('yes')
            status = True
            sheet.update_cell(counter, 4, 0) #未吃藥
        if n>0.5:              # 判斷沒藥
            print('no')
            status = False
            sheet.update_cell(counter, 4, 1) #已吃藥
            print("已吃藥!!!")
            break
            #cv2.imshow("Webcam", image)
            '''
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"): 
                break
            '''
        #time.sleep(5.0)
            
    cv2.destroyAllWindows()
    vs.stop()
    return 0    
    '''
    except KeyboardInterrupt:
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        return 0
    '''
