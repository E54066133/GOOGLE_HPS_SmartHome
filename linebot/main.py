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



#open air condition or not
airConditioner_confirm = ConfirmTemplate(text="要開冷氣嗎？", actions=[
        PostbackAction(label="Yes", data="開冷氣"),
        PostbackAction(label="No", data="不開冷氣")
    ])
airConditioner_confirm_template = TemplateSendMessage(alt_text="confirm alt text", template=airConditioner_confirm)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    mtext = event.message.text
    if mtext == "@冷氣溫度":
        line_bot_api.reply_message(event.reply_token, airConditioner_confirm_template)
    elif mtext == "@查看監視器影像":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("此功能暫未啟用"))
    elif mtext == "@查看亮度":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("此功能暫未啟用"))
        jsonFile.modify_jsonFile(event.source.user_id, 'light', 'light:500000000')
    elif mtext == "@查看溫度":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("此功能暫未啟用"))
        jsonFile.modify_jsonFile(event.source.user_id, 'tem', 'temp:44444444444')
    elif mtext == "@查看濕度":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("此功能暫未啟用"))
        jsonFile.modify_jsonFile(event.source.user_id, 'humidity', 'humidity:heeeeeeeeeeee')
    elif mtext == "@聯絡客服":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("此功能暫未啟用"))
        
      
      
    ##push message
    user_id = event.source.user_id
    print("user_id =", user_id)

#    try:
#     alt_text 因template只能夠在手機上顯示，因此在PC版會使用alt_Text替代
#      line_bot_api.push_message(user_id, TextSendMessage(text='testtttttttttttttt')) 
 #   except LineBotApiError as e:
        # error handle
 #       raise e
            
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

###main###
if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(debug=True)