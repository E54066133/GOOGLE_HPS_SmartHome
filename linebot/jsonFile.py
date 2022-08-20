import json
import time
import math
import os
#### 彙整資料 ####


# Data to be written
def jsonFile(userID):

    #if os.path.exists('user_data.json'):
     #   print('exists')
    #with open('user_data.json', 'r', encoding='utf-8') as f:
      #  if f != '':
      #      j = json.load(f)
      #      print(j)

    user_dict = {
        userID:{
            "name": "sssith",
            "rollno": 56,
            "cgpa": 8.6,
            "phonenumber": "eeeeee500"
        },
        "aaaa":{
            "name": "sssssssssssssssssss",
            "rollno": 56,
            "cgpa": 8.6,
            "phonenumber": "eeeeee500"
        }
    }

        #j.update(user_dict)
    with open("user_data.json", "w") as f:
        json.dump(user_dict, f)



def modify_jsonFile(userID, type, text):

    record = False
    with open('user_data.json', 'r', encoding='utf-8') as f:
        j = json.load(f)
        if userID in j:
            record = True

        if not record:                  # 若為新用戶，註冊新usre_id
            user_dict = \
                {
                    userID: {
                        type: text
                    }
                }
            j.update(user_dict)
            print('notexist_userID')
            print(j)
        else:  # 更新用戶內的資料
            new_dict = \
                {
                    type: text
                }
            j[userID].update(new_dict)
            print(j)
    with open("user_data.json", "w") as f:
        json.dump(j, f)


#jsonFile('aaaaaaa')
modify_jsonFile('zzzzzzzz','tele','hihi')