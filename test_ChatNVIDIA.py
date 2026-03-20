# ===============
# 20260304
# Li Ling Chang
# using ChatNVIDIA package
# ===============

# packages
import os
import requests
from getpass import getpass
from dotenv import load_dotenv

from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.runnables.passthrough import RunnableAssign
from langchain_core.prompts import ChatPromptTemplate # for prompt
from langchain_core.output_parsers import StrOutputParser # str -> json -> content
from langchain_core.output_parsers import PydanticOutputParser
from functools import partial
from pydantic import BaseModel, Field
from typing import Any, Dict, Union, Optional


# import gradio as gr

# my packages
from model_util import RPrint

load_dotenv()

chat_key = os.getenv("NVIDIA_CHAT_API_KEY")
embed_key = os.getenv("NVIDIA_EMBED_API_KEY")

# ======model checking======
    
# print(ChatNVIDIA.get_available_models())

# ======api test: nvidia service -- ChatNvidia======

# llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", base_url="https://integrate.api.nvidia.com/v1", api_key=os.getenv('NVIDIA_CHAT_API_KEY'), mode='open')
llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", api_key=os.getenv('NVIDIA_CHAT_API_KEY'))

""" # 20260304--simple question without chain
message = "hello llm model what your name?"
response = llm.invoke(message).model_dump_json()
print(response)
"""

""" # 20260305--simple cat llm
cat_prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a cat and i am your servant"),
    ("user", "{input}")
])

cat_chain = cat_prompt | llm | StrOutputParser()

print(cat_chain.invoke({"input":"What do you wanna have for lunch?"}))

def cat_chat_stream(message, history):
    buffer = ""
    for token in cat_chain.stream({"input":message}):
        buffer = buffer + token
        yield buffer

demo = gr.ChatInterface(cat_chat_stream)#.queue() # why queue?
window_kwargs = {}
demo.launch(share=True, debug=True, **window_kwargs)"""

# ======knowledge base======
class KnowledgeBase(BaseModel):
    ## Fields of the BaseModel, which will be validated/assigned when the knowledge base is constructed
    conversation_summary: str = Field('unknown', description="Record things about the conversation between llm and user")
    response: str = Field('unknown', description="you are a cat and here is your response")


cat_base_prompt = ChatPromptTemplate.from_template(
    " You are a cat who is having a conversation with user"
    " You just say ('output') and the user responded ('input'). Please update the knowledge base."
    " Record your response in the 'response' tag to continue the conversation."
    " Do not hallucinate any details, and make sure the knowledge base is not redundant."
    " Update the entries frequently to adapt to the conversation flow."
    "\n{format_instructions}"
    "\n\nOLD KNOWLEDGE BASE: {know_base}"
    "\n\nNEW MESSSAGE: {input}"
    "\n\nNEW KNOWLEDGE BASE:"
)

## Definition of RExtract
def RExtract(pydantic_class, llm, prompt):
    '''
    Runnable Extraction module
    Returns a knowledge dictionary populated by slot-filling extraction
    '''
    parser = PydanticOutputParser(pydantic_object=pydantic_class)
    instruct_merge = RunnableAssign({'format_instructions' : lambda x: parser.get_format_instructions()})
    def preparse(string):
        if '{' not in string: string = '{' + string
        if '}' not in string: string = string + '}'
        string = (string
            .replace("\\_", "_")
            .replace("\n", " ")
            .replace(r"\]", "]")
            .replace(r"\[", "[")
        )
        # print(string)  ## Good for diagnostics
        return string
    return instruct_merge | prompt | llm | parser # | StrOutputParser() | preparse | parser | RPrint

base_update =  RunnableAssign({'know_base' : RExtract(KnowledgeBase, llm, cat_base_prompt)})

state = {'know_base' : KnowledgeBase()}
history = []

while True:
    message_new = input("Say something to your kitten: ")
    state['input'] = message_new
    state['output'] = "" if history == [] else history[-1].get('output') 
    state = base_update.invoke(state)
    # print(state)
    message_out = state.get('know_base').response
    print('cat: ', message_out)
    history.append({'input':message_new, 'output': message_out})
