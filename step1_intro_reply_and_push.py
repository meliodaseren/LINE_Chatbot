# coding: utf-8
# pip install flask; pip install line-bot-sdk

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/" )

# create a instance for line
# line_bot_api 用來處理消息 <Channel Access Token>
line_bot_api = LineBotApi('<channel access token>')

# 用來接收外部消息 <channel secret>
handler = WebhookHandler('<channel secret>')

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body 驗證封包是否來自Line
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    line_bot_api.push_message(
        # <userId>
        '<user Id>',
        TextSendMessage(text="歡迎參加 LINE 聊天機器人測試")
    )      
        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
