from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import psycopg2
import os
import re
DATABASE_URL = os.environ["postgres://nwajksqwsgrbww:0ecdacf3ab35c8b3ff3bbe0113830ed1b9078eef57dbe18dbc721dbee4047ca9@ec2-52-203-160-194.compute-1.amazonaws.com:5432/d1jihonate44gb"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor=conn.cursor()


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
    cursor=conn.cursor()
    message = TextSendMessage(text=event.message.text)

    cursor.execute("SELECT status from users where userID = %s",event.source.user_id)
    status = cursor.fetchone()

    if(status == "Addroomid"):
        if(message == "break"):
            cursor.execute("INSERT INTO users(userID,status) VALUES(%s,%s)",event.source.user_id, '')
            conn.commit()
            conn.close()
            return 0
        #檢查 roomid 存在
        if (cursor.execute("SELECT COUNT(*) from rooms where roomid = %s", message) == 0):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "addroom failed"))
            conn.commit()
            conn.close()
            return 0
        else:    
            cursor.execute("INSERT INTO admin(adminID,roomID) VALUES(%s,%s)", event.source.user_id, message)
            print('admin add success')

    if(message.find("管理者")):
        cursor.execute("INSERT INTO users(userID,status) VALUES(%s,%s)",event.source.user_id, 'Addroomid')
        conn.commit()
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

    conn.commit()
    conn.close()

@handler.add(PostbackEvent)
def handle_postback(event):
    postback = event.postback.data



if __name__ == "__main__":
  
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
    DATABASE_URL = os.environ["DATABASE_URL"]
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor=conn.cursor()


#note
#string.find()尋找關鍵字