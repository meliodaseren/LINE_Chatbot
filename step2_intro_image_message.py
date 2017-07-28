# coding: utf-8

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,ImageSendMessage
)

app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/" )

# create a instance for line
# line_bot_api 用來處理消息
line_bot_api = LineBotApi('<channel access token>')

# 用來接收外部消息
handler = WebhookHandler('<channel secret>')

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body 驗證封包是否來自 Line
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
        '<userId>',
        TextSendMessage(text="這是推送消息")
    )

# 圖片連結必須為 https
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url='<image url>',
            preview_image_url='<image url>')
    )
    line_bot_api.push_message(
        '<userId>',
        ImageSendMessage(
            original_content_url='<image url>',
            preview_image_url='<image url>')
    )
 
if __name__ == "__main__":
    app.run(host='0.0.0.0')
