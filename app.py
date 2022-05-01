from flask import Flask, request, abort  # building a website or a server

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('D2XPmvG53D0kT5SkHSOB1gPt3YnwfkOpPmQ89FjPKVfTMs2e492gltQwYDZ2qpk1kp69DI8pEE5Xcg4gcKew8/Q58C7wADemQHK0/EJTwGJjUDhcYlK1FCjqagV4uH85hIpeZ7lr8AGwN7JxzKJqHAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9a49e02d06091be47fd7f63c59f50071')

# If someone goes to address:www.line-bot/callback, this function will run.
# It does not work if the address is like www.line-bot/callback222.


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


# This command is to require command to active this code after importing this code,
# the code will automatically run right after importing this code without this commnad.
if __name__ == "__main__":
    app.run()
