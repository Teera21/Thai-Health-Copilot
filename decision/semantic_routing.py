from langchain_openai import ChatOpenAI
import openai
import os 
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage

class Semantic_Route:
    def __init__(self)-> None:
        os.environ["OPENAI_API_KEY"] = "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"
        api_key = os.environ['OPENAI_API_KEY']
        self.llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview",api_key=api_key)

    def decision_to_extract_data(self,user_input:str)->str:
        
        prompt = f"""
        Analyze the following MESSAGE and determine if it contains any information about the following topics: name, weight, height, events that happened, likes, personality traits, birthday, illness, symptoms, or health information.
        Respond with "YES" if any of these details are present, 
        and "NO" otherwise.
        MESSAGE:{user_input}
        RESPONSD: 
        """
        messages = [
        HumanMessage(
            content=prompt
        ),
        ]
        result = self.llm(messages)

        return str(result.content)