import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
import openai

client = openai.OpenAI()

file = client.files.create(
    file=open("2021_population.csv", "rb"),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
    name="Python Developer",
    instructions="You are a python developer",
    model="gpt-4-1106-preview",
    tools = [ { "type": "code_interpreter" } ],
    file_ids=[file.id]
)

llm_config = { 
    "assistant_id": assistant.id,
    # "tools": [ { "type": "code_interpreter" } ],
    # "file_ids": [file.id]
}

gpt_assistant = GPTAssistantAgent(
    name="Coder Assistant",
    instructions="""
    You are an expert at writing python code to solve problems. 
    Reply TERMINATE when the task is solved and there is no problem
    """,
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="MervinPraison",
    code_execution_config={
        "work_dir" : "coding",
    }
)

user_proxy.initiate_chat(
    gpt_assistant,
    message="""
    What is the population trend.
    Give me an overview of the data. 
    Show how you solved it with code.
    """
)
