from dotenv import load_dotenv
from pydantic import BaseModel
import os
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent,AgentExecutor

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str] 
    

load_dotenv()
import requests


# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="api", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)        
# # parse the output by the llm and then make it in an object which we can use in our code
# parser = PydanticOutputParser(pydantic_object = ResearchResponse)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ('system','''you are a research assistent which will help generate a research paper
#          answer the user query and use neccessary tools
#          Wrap the output in this format and provide no other text \n{format_instruction}'''),
#          ('placeholder','{chat_history}'),
#          ("human","{query}"),
#          ("placeholder",'{agent_scratchpad}')
#     ]

# ).partial(format_instruction = parser.get_format_instructions())

# agent = create_tool_calling_agent(
#     llm = llm,
#     prompt=prompt,
#     tools = []
# )

# agent_executor = AgentExecutor(agent=agent, tools= [],verbose=True)
# raw_response = agent_executor.invoke({'query':'what is the capital of france'})
# print(raw_response)