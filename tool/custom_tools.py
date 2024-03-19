import os
from dotenv import load_dotenv, find_dotenv
import openai
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from tool.function_tools import core_memory_append
import os 


os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.environ.get('OPENAI_API_KEY')
 
class Save_Information(BaseModel):
    lates_reply:str = Field(description='This is output from conversation.')

class Save_Information_Tool(BaseTool):
    name = 'core_memory_append'
    description = 'use this to save information from Properies.'
    args_schema: Type[BaseModel] = Save_Information

 
    def _run(self,lates_reply:str):
        return core_memory_append(user_input=lates_reply)
    
    def _arun(self, url:str):
        raise NotImplementedError('does not support async')