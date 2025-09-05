from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

def add(a:int, b:int) -> int:
    '''this function will add two numbers'''
    return a + b 

model = ChatOllama(model="qwen2.5:3b")
agent = create_react_agent(model=model,tools=[add],prompt="You are a helpful assistant.")

result = agent.invoke({"messages": [HumanMessage(content="What is 7 plus 6")] })
for m in result['messages']:
    m.pretty_print()