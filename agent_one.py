from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

@tool
def add(a: int, b: int) -> int:
    '''this function adds two numbers'''
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    '''this function multiplies two numbers'''
    return a * b


tools = [add, multiply]
model = ChatOllama(model="qwen2.5:3b").bind_tools(tools=tools)
#Create a lookup dictionary from tool name to function
tool_lookup = {tool.name: tool for tool in tools}

while True:
    user_input = input("Enter: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    # Step 1: Send user input to model
    result = model.invoke([HumanMessage(content=user_input)])
    print(result.content)
    # Step 2: Check for tool calls
    if result.tool_calls:
        tool_messages = []
        for tool_call in result.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            print(f"Tool_call: {tool_name}")

            # Get the actual tool function
            tool_fn = tool_lookup.get(tool_name)

            # Safely invoke the tool if found
            if tool_fn:
                tool_result = tool_fn.invoke(tool_args)
            else:
                tool_result = f"Tool '{tool_name}' not found."

            # Create ToolMessage to send back to model
            tool_messages.append(
                ToolMessage(name=tool_name, content=str(tool_result), tool_call_id=tool_id)
            )

        # Step 5: Send original user input + all tool results back to model
        followup = model.invoke([
            HumanMessage(content=user_input),
            *tool_messages
        ])
        print(followup.content)

