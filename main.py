import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (MessageEvent, TextMessage, TextSendMessage, PostbackEvent, PostbackTemplateAction,
                            PostbackAction, ConfirmTemplate, TemplateSendMessage, ButtonsTemplate,MessageTemplateAction,URITemplateAction,
                            CarouselTemplate, CarouselColumn, URIAction)

import jsonFile
#import Tapo_Function
import re
from linebot.exceptions import LineBotApiError

import air_conditioner_tem
app = Flask(__name__)






#要改channel_secret和channel_access_token
channel_secret = 'b66ee3cb45b881093e1c94ee040b1a39'
channel_access_token = 'WlZ/ZsNlmmIaBZQS61pyn9RhO8Am619TI+XEOU64nafXLILC/jwcYfkn+xzLI4G1XaFgd0Q3GG1K4iYigZMwByVbUiIVMZCtpTA7nTTWttPP7zm0dC46moutA47iPlWe1UFa3sWzcrhiKP4mNeU1mAdB04t89/1O/w1cDnyilFU='
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#wireless_switch = 0  # 無限開關的初始狀態 (0:關, 1:開)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


##################### 確定這段要不要???
#open air condition or not
airConditioner_confirm = ConfirmTemplate(text="要開冷氣嗎？", actions=[
        PostbackAction(label="Yes", data="開冷氣"),
        PostbackAction(label="No", data="不開冷氣")
    ])
airConditioner_confirm_template = TemplateSendMessage(alt_text="confirm alt text", template=airConditioner_confirm)
#######################




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    mtext = event.message.text
    str_pas = re.search("^@@冷氣",mtext)
    str_pas2 = re.search("^@@照片",mtext)
    str_pas3 = re.search("^@@結束",mtext)
    if str_pas2:
        mtext_pic_temp = mtext.split("片")
        #line_bot_api.reply_message(event.reply_token, TextSendMessage("216"))
        user_id_for_pic = event.source.user_id
        store_path = mtext_pic_temp[1]+"_"+user_id_for_pic   # 測試這樣的命名能不能通過
        f_pic = open('store_path.txt', 'w+')
        f_pic.write(store_path)
        f_pic.close()
        
        try:
            os.mkdir(store_path)
        except:
            pass
    if str_pas3:
        # 傳訊號給辨識模型(再次訓練)或是call再次訓練的function
        print("待完成")
        line_bot_api.reply_message(event.reply_token, TextSendMessage("待完成"))
        
            
    if str_pas:
        user_name = mtext[4:-2]         # 用戶的名字
        user_temperature = mtext[-2:]   # 用戶希望設定的溫度
        '''
        這邊要寫進json的東西有:
        1. 用戶設定的溫度
        '''
        username_userID = user_name + "_" + event.source.user_id
        jsonFile.modify_jsonFile(username_userID, 'airConditionerTemp', user_temperature)
        line_bot_api.reply_message(event.reply_token, TextSendMessage("設定完成"))
    ################################################## 確定這段要不要???
    if mtext == "@冷氣溫度":
        line_bot_api.reply_message(event.reply_token, airConditioner_confirm_template)
    ################################################## 
    elif mtext == "@查看監視器影像":
        # https://ithelp.ithome.com.tw/articles/10198142?sc=iThelpR 作法參照這個網站
        line_bot_api.reply_message(event.reply_token, TextSendMessage("此功能暫未啟用"))
        '''
        try:  #先用測試圖片 #之後要去抓宇霈的照片網址
            message_reply_pic = {
                "type": "image",
                "originalContentUrl": "https://drive.google.com/file/d/1VNRMU0U_v8WJAwc1A4B8YXZTT8nQJ1SR/view?usp=sharing", 
                "previewImageUrl": "https://drive.google.com/file/d/1VNRMU0U_v8WJAwc1A4B8YXZTT8nQJ1SR/view?usp=sharing"
            }
            line_bot_api.reply_message(event.reply_token, message_reply_pic)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("發生錯誤"))
        '''
    elif mtext == "@查看亮度":
        try:
            f = open('light_intensity.txt', 'r')
            light_now = f.readline()
            f.close()
            light_now = str(light_now)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(light_now))
            line_bot_api.reply_message(event.reply_token, TextSendMessage("請聯絡效華 ><"))
            #jsonFile.modify_jsonFile(event.source.user_id, 'light', light_now)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("發生錯誤,請稍等5分鐘"))
    elif mtext == "@查看溫度":
        try:
            f = open('temperature.txt', 'r')
            temperature_now = f.readline()
            f.close()
            temperature_now = str(temperature_now)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(temperature_now))
            line_bot_api.reply_message(event.reply_token, TextSendMessage("請聯絡效華 ><"))
            #jsonFile.modify_jsonFile(event.source.user_id, 'tem', temperature_now)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("發生錯誤,請稍等5分鐘"))
    elif mtext == "@查看濕度":
        try:
            f = open('moisture.txt', 'r')
            moisture_now = f.readline()
            f.close()
            moisture_now = str(moisture_now)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(moisture_now))
            line_bot_api.reply_message(event.reply_token, TextSendMessage("請聯絡效華 ><"))
            #jsonFile.modify_jsonFile(event.source.user_id, 'humidity', moisture_now)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("發生錯誤,請稍等5分鐘"))
    elif mtext == "@無線開關打開":
        try:
            #8/30 測試
            #Tapo_Function.openTapo_temp()
            line_bot_api.reply_message(event.reply_token, TextSendMessage("開關 On"))
            line_bot_api.reply_message(event.reply_token, TextSendMessage("效華給我記住 ><"))
        except:
            pass
    elif mtext == "@無線開關關閉":
        try:
            #8/30 測試
            #Tapo_Function.closeTapo_temp() 
            line_bot_api.reply_message(event.reply_token, TextSendMessage("開關 Off")) 
            line_bot_api.reply_message(event.reply_token, TextSendMessage("效華效華效華效華效華效華效華效華"))
        except:
            pass
    elif mtext == "@幫助":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("您好! 歡迎使用本服務\n\
        若要設定冷氣請打 @@冷氣+用戶名稱+要設定的溫度 ex.@@冷氣Mom26\n\
        若要設定照片資料請打 @@照片+用戶名稱,接著傳送10張自己的臉部照片(各種不同角度為佳)\n\
        若照片傳送結束請打 @@結束"))
    elif mtext == "@聯絡客服":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請聯絡 效華xDDDDDDDDDDDDDDDDDDDDDDDDDD"))
      
      
    ##push message
    user_id = event.source.user_id
    print("user_id =", user_id)

#    try:
#     alt_text 因template只能夠在手機上顯示，因此在PC版會使用alt_Text替代
#      line_bot_api.push_message(user_id, TextSendMessage(text='testtttttttttttttt')) 
 #   except LineBotApiError as e:
        # error handle
 #       raise e



#################################################### 確定這段要不要           
@handler.add(PostbackEvent)
def handle_postback(event):
    #content = "{}: {}".format(event.source.user_id, event.message.text)
    #line_bot_api.reply_message(
     #   event.reply_token,
      #  TextSendMessage(text=content))

    if event.postback.data == "不開冷氣":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("不開冷氣"))
        jsonFile.modify_jsonFile(event.source.user_id, 'airConditioner', 'noAirConditioner')
    elif event.postback.data == "開冷氣":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請問你冷氣要開幾度呢?", quick_reply=air_conditioner_tem.airConditionerTem_reply))
        jsonFile.modify_jsonFile(event.source.user_id, 'airConditioner', 'yesAirConditioner')

    #設定冷氣溫度
    if event.postback.data.find("°C") >= 0:
        print(event.postback.data + "temppppp")
        line_bot_api.reply_message(event.reply_token, TextSendMessage("okokokokokokkkkk"))
        jsonFile.modify_jsonFile(event.source.user_id, 'airConditionerTemp', event.postback.data[:-2])
        #set_airConditioner_tem() #設定冷氣溫度???
##################################################################


## 處理照片
'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 這邊要測會不會成功，因為handler沒有寫type = textmessage
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    if (event.message.type == "text"):
        line_bot_api.reply_message(event.reply_token, TextSendMessage("210"))
        mtext_pic = event.message.text
        str_pas2 = re.search("^@@照片",mtext_pic)
        print(str_pas2)
        str_pas3 = re.search("^@@結束",mtext_pic)
        if str_pas2:
            mtext_pic_temp = mtext_pic.split("片")
            #line_bot_api.reply_message(event.reply_token, TextSendMessage("216"))
            user_id_for_pic = event.source.user_id
            store_path = mtext_pic_temp[1]+"_"+user_id_for_pic   # 測試這樣的命名能不能通過
            f_pic = open('store_path.txt', 'w+')
            f_pic.write(store_path)
            f_pic.close()
            
            try:
                os.mkdir(store_path)
            except:
                #pass
                print("store_path fail")
        if str_pas3:
            # 傳訊號給辨識模型(再次訓練)或是call再次訓練的function
            print("待完成")
'''
                
@handler.add(MessageEvent)
def handle_message(event):
    # 這邊要測會不會成功，因為handler沒有寫type = textmessage
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    if (event.message.type == "image"):
        SendImage = line_bot_api.get_message_content(event.message.id)
        f_pic_read = open('store_path.txt','r')
        store_path = f_pic_read.readline()
        f_pic_read.close()
        path = '/home/pig/linebot_ver2/' + store_path + "/" + event.message.id + '.png'      # 這邊要改path
        with open(path, 'wb') as fd:
            for chenk in SendImage.iter_content():
                fd.write(chenk)
    
'''
要先請用戶輸入名字 (加一串re ... 建立資料夾用的)
再上傳照片
把這些照片存在同一個資料夾
'''



###main###
if __name__ == "__main__":
    global store_path
    store_path = ""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)