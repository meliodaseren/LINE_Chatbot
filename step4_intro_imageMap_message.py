# coding: utf-8

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,ImagemapSendMessage
)

from linebot.models import (
    ImagemapArea, BaseSize, URIImagemapAction, MessageImagemapAction
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

    # handle webhook body 驗證封包是否來自Line
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    
imagemap_message = ImagemapSendMessage(
    base_url='https://54788c11.ap.ngrok.io/images/s1',
    alt_text='This is an imagemap',
    base_size=BaseSize(height=700, width=700),
    actions=[
        URIImagemapAction(
            link_uri='https://www.youtube.com/watch?v=uauzw00I0wY',
            area=ImagemapArea(
                x=0, y=0, width=520, height=1040
            )
        ),
        MessageImagemapAction(
            text='hello',
            area=ImagemapArea(
                x=520, y=0, width=520, height=1040
            )
        )
    ]
)    
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        imagemap_message)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
