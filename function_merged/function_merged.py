import json
import time
#import Tapo_Function


tapo_off = True   # False 表示電器是開的，True 表示電器是關的
list_person = []


while True:
    try:
        f2 = open('temperature.txt','r')         # 拿sensor測到的溫度
        temprature_now = f2.readline()
        f2.close()

        f3 = open("person_detected.txt",'r')     # 拿辨識模型辨識到的用戶名稱
        person_detected = f3.readline()
        f3.close()

        f = open('user_data.json','r')           # 拿user_data.json 面的設定檔
        f1 = json.load(f)
        f.close()

        for key in f1.keys():                    # 檢查用戶有無更新 user_data.json
                if format(key) in list_person:
                    pass
                else:
                    list_person.append(format(key))

        if person_detected in list_person:                                       # 邏輯判斷是否開啟tapo開關
            temprature_set = int(f1[person_detected]["airConditionerTemp"])
            temprature_now = int(temprature_now)
            if temprature_now >= temprature_set :
                if tapo_off :
                    #Tapo_Function.openTapo_temp()
                    print("開啟開關")
                    tapo_off = False
            else:
                tapo_off = True
        
        time.sleep(1)
    except:
        time.sleep(302)
