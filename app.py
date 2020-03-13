from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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
    line_bot_api.reply_message(event.reply_token, message)
    message2 = TextSendMessage(text='No')
    line_bot_api.push_message(event.push_token, message2)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


#note
#string.find()尋找關鍵字