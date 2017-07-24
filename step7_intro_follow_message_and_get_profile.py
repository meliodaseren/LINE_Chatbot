# coding: utf-8

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,FollowEvent 
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
    
        
@handler.add(FollowEvent)
def handle_follow_event(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    profileContent = profile.display_name + '\n' + profile.user_id + '\n' + profile.status_message
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=profileContent))        
        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
