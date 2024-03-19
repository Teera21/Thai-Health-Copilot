import os
import sys
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from googletrans import Translator

# Custom imports
from langchain_core.messages import AIMessage, HumanMessage
from tool.function_tools import Core_momory
from decision.semantic_routing import Semantic_Route
from flow_bot.function_flow import function_bot
from config import config as cfg

# Initialize Flask application and LINE Messaging API
app = Flask(__name__)
line_bot_api = LineBotApi(cfg.LINEBOT_API)
handler = WebhookHandler(cfg.WEBHOOK)

# Create instances of necessary classes
bot = function_bot()
chat_history = []
data_history = {}
ai_msg = []
translator = Translator()

# Define route for webhook
@app.route("/callback", methods=['POST'])
def callback():
    # Extract request information
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name
    
    # Process user input
    user_input = text
    route = Semantic_Route()
    track_information = route.decision_to_extract_data(user_input)
    unique_id = id
    bot.check_data(unique_id)

    # Core memory and history management
    if str(track_information) == "YES" or str(track_information) == "yes":
        main_core = Core_momory(user_input=user_input, cfg=cfg, unique_id=unique_id)
        main_core.retreiver_memory()
        main_core.core_memory_append()
    try:
        if len(data_history[unique_id]) > 4:
            data_history[unique_id] = data_history[unique_id][2:]
    except KeyError:
        chat_history = []

    # Generate response and update chat history
    if unique_id in data_history:
        ai_msg = bot.rag_chain(user_input=user_input, chat_history=data_history[unique_id])
        data_history[unique_id].extend([HumanMessage(content=user_input), ai_msg])
    else:
        ai_msg = bot.rag_chain(user_input=user_input, chat_history=chat_history)
        data_history[unique_id] = [HumanMessage(content=user_input), ai_msg]

    # Send reply to user
    reply(ai_msg.content, reply_token)
    return 'OK'

# Function to send reply message
def reply(text, reply_token):
    text_message = TextSendMessage(text=text)
    line_bot_api.reply_message(reply_token, text_message)

# Main function to run the Flask app
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)