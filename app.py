from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

user_id = {}

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('D4jP2o+UJxNhEPro+12EqFl7HUa8iHyfabFIxtTXjYx/tLm2QAEDJqY2f6KmrqfDepOhTigfWzCJS2ttTjQXSNcA0RHsLqS+6d2W3/LSzWxYbRaAyIhrsnRxxRNuAxXaUiOg6rkqUpwSCEmtqFL6+QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('91d2018622705a3117d64eb67044f573')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    if(message == "我要成為管理者"):
        roomIdRequest = TextSendMessage(text = "請輸入roomid")
        line_bot_api.reply_message(event.reply_token, roomIdRequest)

    if(event.source.user_id == 'Uc38ec3a6672b3b5033dddc4851ad4893'): 
        if(message == 'login'):
            #login
            login = TextSendMessage(text="login success")
            line_bot_api.reply_message(event.reply_token, login)
            f_userid = open('user_id.txt', 'r')
            for userid in f_userid.readlines():
                line_bot_api.push_message(userid, message)
                user = TextSendMessage(text = userid)
                line_bot_api.reply_message(event.source.user_id, user)
            f_userid.close()
    else:
        line_bot_api.reply_message(event.reply_token, message)
        fo = open('user_id.txt', 'r')
        if event.source.user_id not in fo.read():
            f = open('user_id.txt', 'w+')
            f.write(event.source.user_id + '\n')
        f.close()
        fo.close()
'''
#admin
app2 = Flask(__name__)
# Channel Access Token
line_bot_api2 = LineBotApi('ZS0OVcr4EZb+XWe0ot/Etpb3hufOWtLONcE8I4TNmjjU0t83+1GAYOldPEbwgf2IBUOZLte/5qUJFQJ/nSnnKB/6RlfWYUSWHZxCkGXkteyqKc9F+UzyimnCZUviB24ZhT+7vSNnTJP6xuA/+IgniwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler2 = WebhookHandler('3261bde6e8fdf4087dc2d2da1e68886d')
# 監聽所有來自 /callback 的 Post Request
@app2.route("/admin", methods=['POST'])
def admin():
    # get X-Line-Signature header value
    signature2 = request.headers['X-Line-Signature']
    # get request body as text
    body2 = request.get_data(as_text=True)
    app2.logger.info("Request body: " + body2)
    # handle webhook body
    try:
        handler2.handle(body2, signature2)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
@handler2.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if(event.user_id == 'Uc38ec3a6672b3b5033dddc4851ad4893'): 

    message = TextSendMessage(text= event.message.text)
    line_bot_api2.reply_message(event.reply_token, message)
    for userid in user_id:
        line_bot_api.push_message(user_id, message)
'''
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


#note
#string.find()尋找關鍵字