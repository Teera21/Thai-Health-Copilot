import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from typing import List, Tuple

import sys
sys.path.append(f'{os.getcwd()}')
from config import config as cfg
from prompt.check_dir import is_name_in_folder
from flow_bot.manage_user_data import get_format_docs
from prompt.prompt_template import contextualize_q_system_prompt_source, qa_system_prompt_source

class function_bot():

    def __init__(self)->None:
        self.contextualize_q_system_prompt = contextualize_q_system_prompt_source
        self.qa_system_prompt = qa_system_prompt_source
        api_key = cfg.OPENAI_API_KEY
        self.embedding_hf = HuggingFaceEmbeddings(model_name=cfg.EMBEDDING_MODEL)

        self.llm = ChatOpenAI(temperature=0.7, model="gpt-4-1106-preview",api_key=api_key)
        self.retriever = Chroma(persist_directory= os.getcwd() + cfg.CHROMA_PATH, embedding_function=self.embedding_hf).as_retriever(k=3) 
    
    def check_data(self, unique_id):
        check_user_data, user_data = is_name_in_folder(name=unique_id,path='./data/data_user')
        if  check_user_data:
            data = "This is User data : " +  user_data
            self.qa_system_prompt += data
        else :
            self.qa_system_prompt = self.qa_system_prompt.split('This is User data :')[0]

    def generate_prompt(self):
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        self.contextualize_q_chain = contextualize_q_prompt | self.llm | StrOutputParser()

        qa_system_prompt = self.qa_system_prompt
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        return qa_prompt

    def contextualized_question(self,input: dict):
        if input.get("chat_history"):
            return self.contextualize_q_chain
        else:
            return input["question"]
        
    def rag_chain(self,user_input:str,chat_history:List)->str:  
        
        
        rag_chain = (
        RunnablePassthrough.assign(
            context= self.contextualized_question
        )
        | self.generate_prompt()
        | self.llm
        )

        ai_msg = rag_chain.invoke({"question": user_input, "chat_history": chat_history})
        return ai_msg