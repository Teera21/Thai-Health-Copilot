from flask import Flask, request
from linebot import *
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('O0Ie/6BsEvQJVPw+9EAoKEd18WMbimSFHPPU0q9eVvCW10YIpQQvx031Ece+ujlrfT7DmmszKN8sk2lvT4lLH/P8DwwH1E5jdYNvoTlRKhDkGEzpA3cHOcA3c6RlMriYWaIYpxeYZAR/VZKHgvV45gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a1f9c035e4cfc2c1a7fe9e80ec9f2251')

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    # print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name

    # print('id = ' + id)
    # print('name = ' + disname)
    # print('text = ' + text)
    # print('intent = ' + intent)
    # print('reply_token = ' + reply_token)
    for i in range(10000):
        print(i)
    reply(intent,text,reply_token,id,disname)

    return 'OK'


def reply(intent,text,reply_token,id,disname):
    text_message = TextSendMessage(text=text+' ไรวะ')
    line_bot_api.reply_message(reply_token,text_message)

if __name__ == "__main__":
    app.run()