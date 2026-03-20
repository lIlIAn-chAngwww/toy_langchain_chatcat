# ===============
# 20260302 
# Li Ling Chang
# using manual python requests
# ===============

# packages
import os
import requests
from getpass import getpass
from dotenv import load_dotenv

# my packages
import model_util

load_dotenv()

chat_key = os.getenv("NVIDIA_CHAT_API_KEY")
embed_key = os.getenv("NVIDIA_EMBED_API_KEY")

# ======model checking======
    
model_util.printAvailableModelList()

# ======api test: nvidia service -- manual python request======

def ModelSim(message_content):
    invoke_url = os.getenv("MODEL_INVOKE_URL")
    # headers = {"accept": "text/event-stream",
    #            "content-type": "application/json"}
    headers = {"accept": "application/json",
            "content_type": "application/json",
            "Authorization": f"Bearer {os.getenv('NVIDIA_CHAT_API_KEY')}"}

    payload = {
            "model": "meta/llama-3.1-70b-instruct",
            "messages": [
            {
            "content":message_content,
            "role": "user"
            }],
            "top_p": 1,
            "n": 1,
            "max_tokens": 1024,
            "stream": False,
            "frequency_penalty": 0.0,
            "stop": ["STOP"]
    }
    return requests.post(invoke_url, headers=headers, json=payload, stream=True)

message = "hello llm model what your name?"
response = ModelSim(message).json()
print(response['choices'][0]['message']['content'])


