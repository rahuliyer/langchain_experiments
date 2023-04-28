from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory

from langchain.llms import OpenAI

from api_key_loader import load_api_keys
from notion import NotionCreatePageTool
from notion import NotionAddTextToPageTool
from notion import NotionQueryDatabaseTool

load_api_keys()

llm = OpenAI(temperature=0)

tools = load_tools(["google-search", "wikipedia", "human"])
tools.append(NotionCreatePageTool())
tools.append(NotionAddTextToPageTool())
tools.append(NotionQueryDatabaseTool())

memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools, 
    llm, 
    AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory = memory,
    verbose=True)

while True:
    user_input = input("> ")
    if user_input == "bye":
        break

    print(agent.run(input=user_input))
