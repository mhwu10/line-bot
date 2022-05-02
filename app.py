from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'D2XPmvG53D0kT5SkHSOB1gPt3YnwfkOpPmQ89FjPKVfTMs2e492gltQwYDZ2qpk1kp69DI8pEE5Xcg4gcKew8/Q58C7wADemQHK0/EJTwGJjUDhcYlK1FCjqagV4uH85hIpeZ7lr8AGwN7JxzKJqHAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9a49e02d06091be47fd7f63c59f50071')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = "I don't understand"

    if "give me stickers" in msg:
        sticker_message = StickerSendMessage(
            package_id='11538',
            sticker_id='51626501'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ["hi", "Hi"]:
        r = "hi"
    elif msg == "Have you had meal?":
        r = "Not yet"
    elif msg == "Who are you?":
        r = "I am a robot"
    elif "book" in msg:
        r = "Do you want to book?"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
