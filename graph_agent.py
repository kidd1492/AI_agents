from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import MessagesState, START, StateGraph

class AgentState(MessagesState):
    pass

@tool
def add(a: int, b: int) -> int:
    '''this function adds two numbers'''
    return a + b

@tool
def multipy(a: int, b: int) -> int:
    '''this function multipies two numbers'''
    return a + b


tools = [add, multipy]
model = ChatOllama(model="qwen2.5:3b").bind_tools(tools=tools)


def chat_node(state:AgentState) -> AgentState:
    result = model.invoke(state["messages"])
    print(result.content)
    return {'messages': [result]}

graph = StateGraph(AgentState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", ToolNode(tools=tools))

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

app = graph.compile()

with open("agent.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

while True:
    user_input = input("Enter: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break
    results = app.invoke({"messages": [HumanMessage(content=user_input)]})
