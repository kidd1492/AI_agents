from typing import TypedDict, Union
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

class AgentState(TypedDict):
    messages: list[Union[HumanMessage, AIMessage, ToolMessage]]

@tool
def add(a: int, b: int) -> int:
    '''This function adds two numbers'''
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    '''This function multiplies two numbers'''
    return a * b

tools = [add, multiply]
model = ChatOllama(model="qwen2.5:3b").bind_tools(tools=tools)
tool_lookup = {tool.name: tool for tool in tools}


def chat_node(state: AgentState) -> AgentState:
    result = model.invoke(state["messages"])
    print(result.content)
    state["messages"].append(result)

    # Check for tool calls
    if result.tool_calls:
        state = tool_node(state, result)
    return state


def tool_node(state: AgentState, result: AIMessage) -> AgentState:
    tool_messages = []

    for tool_call in result.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        print(f"Tool_call: {tool_name} with args {tool_args}")

        tool_fn = tool_lookup.get(tool_name)
        if tool_fn:
            tool_result = tool_fn.invoke(tool_args)
        else:
            tool_result = f"Tool '{tool_name}' not found."

        tool_msg = ToolMessage(name=tool_name, content=str(tool_result), tool_call_id=tool_id)
        state["messages"].append(tool_msg)
        tool_messages.append(tool_msg)

    followup = model.invoke(state["messages"])
    print(followup.content)
    state["messages"].append(followup)

    return state


conversation_history = []

while True:
    user_input = input("Enter: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    conversation_history.append(HumanMessage(content=user_input))
    state = AgentState(messages=conversation_history.copy())
    state = chat_node(state)

    new_messages = state["messages"][len(conversation_history):]
    conversation_history.extend(new_messages)

    # Optional: pretty print all messages
    for msg in new_messages:
        msg.pretty_print()

