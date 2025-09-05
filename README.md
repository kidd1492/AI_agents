# AI_agents
## Project Overview

The goal of this project is to:
- What is an Agent
- ReAct Agent the focus is building from scratch all the way to a Prebuild.
- Learning  LangGraph and LangChain and how it builds an Agent
- Run everything locally using Ollama for privacy.
- Explore streaming responses, memory, and conditional routing


 - agent_one.py --- ReAct Agent with no Framwork.
 #### Blog
 https://humansideoftek.blogspot.com/2025/09/how-ai-agent-works-without-framework.html


### `agents/`

Contains prototypes of various agents:

| File                   | Description                                         
| `RagAgent.py`          | RAG using Chroma  
| `chatbot_1.py`         | Minimal chatbot for baseline testing                                       
| `chatbot_2.py`         | chatbot using checkpointer-memory and MessageState                            
| `conversation.py`      | using 2 bots to have a conversation for a set number of turns. 
                           The topic of the conversation is what my 9th grader is learning about at school.        
