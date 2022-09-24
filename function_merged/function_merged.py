import json
import time
import Tapo_Function
import my_test_client

tapo_off = True   # False 表示電器是開的，True 表示電器是關的
list_person = []
num = 0


from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError

CHANNEL_ACCESS_TOKEN = "iOjpAvuH3tsABVdaxxtGRh8zFPQ//RmiK1LDZzZX4KmM7QnlR2+N4tGDJZqPlGJv3EIBkZNZgrYTNkNr+wPGgXGusVgR7bWcTHuFF07bMGl5pI2BRU7b9CUu5U7jbefcAV+bw8dNEFOoEQJMqKXZpAdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

while True:
    try:
        num = num+1
        f2 = open('temperature.txt','r')         # 拿sensor測到的溫度
        temprature_now = f2.readline()
        f2.close()
        print("temperature.txt OK",num)

        f3 = open("person_detected.txt",'r')     # 拿辨識模型辨識到的用戶名稱
        person_detected = f3.readline()
        
        if person_detected == "unknown":
            c = c+1
            try:
                if c % 5 == 0:
                    f = open('userid_launch.txt')
                    l = f.readlines()
                    print(l)
                    for id in l:
                        line_bot_api.push_message(id, TextSendMessage(text='已偵測到陌生人'))
                        
                        pic_http,pic_http_small = my_test_client.capture()
                        image_message = ImageSendMessage(
                            original_content_url = pic_http,
                            preview_image_url = pic_http_small
                            )
                        line_bot_api.push_message(id, image_message)
                        time.sleep(1)
            except:
                print("error")
                
        f3.close()
        print("person_detected OK",num)
        print(person_detected)

        f = open('user_data.json','r')           # 拿user_data.json 面的設定檔
        f1 = json.load(f)
        f.close()
        print("ser_data.json OK",num)
        print(f1)

        for key in f1.keys():                    # 檢查用戶有無更新 user_data.json
                if format(key) in list_person:
                    pass
                else:
                    list_person.append(format(key))

        if person_detected in list_person:                                       # 邏輯判斷是否開啟tapo開關
            temprature_set = int(f1[person_detected]["airConditionerTemp"])
            print("temprature_set = ",temprature_set)
            print(type(temprature_set))
            temprature_now = int(temprature_now)
            print("temprature_now = ",temprature_now)
            print(type(temprature_now))
            if temprature_now >= temprature_set :
                #if tapo_off :
                Tapo_Function.openTapo_temp()
                print("開啟開關")
                tapo_off = False
            else:
                tapo_off = True
        
    except:
        print(tapo_off)
        print("into exception")
        time.sleep(1)