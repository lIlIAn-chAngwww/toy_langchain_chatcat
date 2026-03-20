# ===============
# 20260302 
# Li Ling Chang
# using manual python requests
# ===============

import os
import requests
from dotenv import load_dotenv

from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from functools import partial

load_dotenv()

# ======for fast print======

def print_and_return(x, preface=""):
    print(f"{preface}{x}")
    return x

def RPrint(preface=""):
    return RunnableLambda(partial(print_and_return, preface=preface))

# ======model checking======

def printAvailableModelList():
    invoke_url = os.getenv("MODEL_LIST_INVOKE_URL")
    headers = {"Authorization": invoke_url}
    response = requests.get(invoke_url, headers=headers, stream=False).json()
    print(response)
    for info in response["data"]:
        print(info["id"])
    
if __name__ == "__main__":
    printAvailableModelList()