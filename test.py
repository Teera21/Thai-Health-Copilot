import os
from langchain_core.messages import AIMessage, HumanMessage
from tool.function_tools import Core_momory
from decision.semantic_routing import Semantic_Route
import sys
from flow_bot.function_flow import function_bot
sys.path.append(f'{os.getcwd()}')
from config import config as cfg
import time
import sys
sys.path.append(f'{os.getcwd()}')
from tool.function_tools import Core_momory

from googletrans import Translator
translator = Translator()

bot = function_bot()
bot.check_data(unique_id="6210f167-467e-411c-83aa-ca5d951bde32")
chat_history = []
data_history = {}
# def str_range_to_thai(text):
#         count = len(text) // 1300
#         trans = ''
#         for i in range(count+1):
#             trans += translator.translate(text[i*1300:(i+1)*1300], src='en', dest='th').text
#         return trans
unique_id = "6210f167-467e-411c-83aa-ca5d951bde32"
while True:
    user_input = input("User : ")
    start = time.time()
    route = Semantic_Route()
    track_information = route.decision_to_extract_data(user_input)
    if str(track_information) == "YES" or str(track_information) =="yes":
        main_core = Core_momory(user_input=user_input,cfg=cfg,unique_id="6210f167-467e-411c-83aa-ca5d951bde32")
        main_core.retreiver_memory()
        main_core.core_memory_append()

    if unique_id in data_history:
        data_history[unique_id].extend([HumanMessage(content=user_input), ai_msg])
        ai_msg =  bot.rag_chain(user_input=user_input,chat_history=data_history[unique_id])
    else:
        ai_msg =  bot.rag_chain(user_input=user_input,chat_history=chat_history)
        data_history[unique_id] = [HumanMessage(content=user_input), ai_msg]
    if len(data_history[unique_id]) > 4:
        data_history[unique_id] = data_history[unique_id][2:]

    print(ai_msg.content)
    print(data_history)
    
    end = time.time()
    print("The time of execution of above program is :",
        (end-start) ,"s")


