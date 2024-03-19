import openai
import json
import os 
from openai import OpenAI
import sys 

sys.path.append(f'{os.getcwd()}')
from config import config as cfg

api_key = cfg.OPENAI_API_KEY
client = OpenAI(api_key=api_key)

current_path = os.getcwd()

class Core_momory:

    def __init__(self,user_input:str,cfg,unique_id)->None:
        super().__init__()
        self.user_input = user_input
        self.cfg = cfg
        self.unique_id = unique_id

        self.folder_name = current_path + cfg.DATA_USER + "/" + str(unique_id)
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)  
            

    def retreiver_memory(self):
        function_descriptions = [
        {
            "name": "extract_info_from_sentence",
            "description": "categorise & extract key info from in sentence",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "names of people found in sentences"
                    },                                        
                    "weight": {
                        "type": "string",
                        "description": "weight of people found in sentences"
                    },
                    "height":{
                        "type": "string",
                        "description": "height of people found in sentences"
                    },
                    "happened": {
                        "type": "string",
                        "description": "what happend of people found in sentneces"
                    },
                    "ikes":{
                        "type": "string",
                        "description": "Things you like to eat found in sentences"
                    },
                    "birthday": {
                        "type": "string",
                        "description": "Date of birth found in sentences"
                    },
                    "health": {
                        "type": "string",
                        "description": "health information found in sentences"
                    },
                },
            }
        }
        ]

        prompt = f"Please extract key information from this information: {self.user_input} "
        message = [{"role": "user", "content": prompt}]
        openai.api_key = self.cfg.OPENAI_API_KEY
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=message,
            functions = function_descriptions,
            function_call="auto",
            
        )
        result = vars(response.choices[0].message) 
        if 'function_call' in result:
            arguments = vars(result['function_call'])['arguments']
            name = eval(arguments).get("name")
            weight = eval(arguments).get("weight")
            height = eval(arguments).get("height")
            happended = eval(arguments).get("happended")
            likes = eval(arguments).get("likes")
            birthday = eval(arguments).get("birthday")
            health = eval(arguments).get("health")

            result =  {
                "name": name,
                "weight":weight,
                "height":height,
                "happended":happended,
                "likes":likes,
                "birthday":birthday,
                "health":health
            }

            with open(self.folder_name +"/information.json", "w") as outfile: 
                json.dump(result, outfile)

    def core_memory_append( self):
        file_name = self.folder_name + "/Information.txt"
        with open(file_name, "a") as file:
            # Write text to the file
            file.write(f"{self.user_input}")




    
