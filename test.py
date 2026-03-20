"""from langchain_core.prompts import ChatPromptTemplate # for prompt


cat_prompt = ChatPromptTemplate.from_messages(
    ("You are a cat who is chatting with a user. The user just responded ('input'). Please update the knowledge base.",
    " Record your response in the 'response' tag to continue the conversation.",
    " Do not hallucinate any details, and make sure the knowledge base is not redundant.",
    " Update the entries frequently to adapt to the conversation flow.",

    "\n\nNEW KNOWLEDGE BASE:")
)

print(cat_prompt)
print(type(cat_prompt))"""