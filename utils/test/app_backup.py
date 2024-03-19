from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import SystemMessage
from tool.custom_tools import Save_Information_Tool
from tool.function_tools import retreiver_memory,core_memory_append
from prompt.read_prompt import Prompt_Text
from googletrans import Translator
from decision.semantic_routing import Semantic_Route
import os 

os.environ["OPENAI_API_KEY"] = "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"
api_key = os.environ['OPENAI_API_KEY']

translator = Translator()

llm = ChatOpenAI(temperature=0.7, model="gpt-4-1106-preview",api_key=api_key)

system_prompt = Prompt_Text()
system_message = SystemMessage(
    content=f"""
    {system_prompt}
    """
)

# tools = [
#     Save_Informatirenn_Tool()
# ]

# agent_kwargs = {
#     "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
#     "system_message": system_message,
# }

memory = ConversationSummaryBufferMemory(
    llm=llm)

while True:
    # agent = initialize_agent(
    #     tools,
    #     llm,
    #     agent=AgentType.OPENAI_FUNCTIONS,
    #     verbose=True,
    #     agent_kwargs=agent_kwargs,
    #     memory=memory,
    # )

    user_input = input('user_input: ')
    if user_input == "Q":
        break
    route = Semantic_Route()
    if route.decision_to_extract_data(user_input) == "YES" or "yes":
        retreiver_memory(user_input)
        core_memory_append(user_input)

    user_input = translator.translate(user_input, to_lang='en',dest='en').text
    conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=memory
                )
    print(conversation.predict(input=user_input))
    
    # with get_openai_callback() as cb:
    #     result = agent.invoke({"input": user_input})
    #     result = translator.translate(result['output'], to_lang='th',dest='th').text
    #     print(result)
        # print(cb)
