from Connect import *
import speech_recognition as sr
from gtts import gTTS
from STT import STT
from TTS import TTS, medicine
import os
import time

counter = 0
mode = 27

def ChangeMode():

    print("請選擇想要的模式:")
    print("輸入1為編輯模式，輸入2為提醒模式，輸入3可切換模式")
    input_value = input()

    if(input_value == '1'):
        mode = 1
        print("進入編輯模式!")
    elif (input_value == '2'):
        mode = 2
        print("進入提醒模式!")
    elif (input_value == '3'):
        mode = 3
        print("結束程式!")

    return mode


if __name__ == '__main__':

    r_num = 2
    
    while(True):    

        mode = ChangeMode()
        print("mode : ", mode)

        while(True):

            #print("mode : ", mode)
            #print("main_counter:", counter)
            counter = counter + 1

            try:
                if(mode == 1):
                    STT(r_num)
                    r_num = r_num + 1
                    print("r_num:", r_num)
                    
                    print("請問是否還要繼續編輯模式?[Y/N]")
                    change_mode = input()
                    if(change_mode == 'Y'):
                        mode = 1
                    else:
                        mode = 2
                        print("進入提醒模式!")
                elif (mode == 2):
                    #print("2")
                    count = TTS()
                    if count > 0:
                        medicine(count)
                    time.sleep(5)
            except KeyboardInterrupt: 
                break
