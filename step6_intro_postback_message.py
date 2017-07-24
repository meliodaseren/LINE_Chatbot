# coding: utf-8

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,PostbackEvent 
)

from linebot.models.template import (
    ButtonsTemplate,PostbackTemplateAction,MessageTemplateAction,URITemplateAction
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
    
buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://54788c11.ap.ngrok.io/images/eddie.jpg',
        title='Menu',
        text='Please select',
        actions=[
            PostbackTemplateAction(
                label='postback',
                text='同時也可以讓用戶發送文字訊息',
                data='action=buy&itemid=1'
            ),
            MessageTemplateAction(
                label='message',
                text='資策會聊天機器人'
            ),
            URITemplateAction(
                label='uri',
                uri='https://www.youtube.com/watch?v=uauzw00I0wY'
            )
        ]
    )
)
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        buttons_template_message)
        
@handler.add(PostbackEvent)
def handle_postback_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.postback.data))        
        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
