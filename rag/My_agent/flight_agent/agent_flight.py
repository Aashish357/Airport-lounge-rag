from dotenv import load_dotenv
from langchain_groq import ChatGroq
from flight_agent import Tools
from langchain.agents import create_agent
from langchain.messages import HumanMessage
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",   
    temperature=0.3,
    timeout=2
)

tool_box=[Tools.get_flight,Tools.validate_flight,Tools.flight_depart]
prompt='''
#Overview
You are an flight assistant.
You need solve the user query based on their requirements

#tools details to call

@tool name :- get_flight - Use this tool to get the flight details  (flight_number needed)
@tool name :- validate_flight - Use this tool to get the flight details are vaild or not (flight_number needed)
@tool name :- flight_depart - Use this tool to get the flight depart time delay (flight_number needed)


#Rules

- Dont call more than one tool
- Analyze the user requirement and then answer them accordingly 
- Dont add anything to that just return as it answer from tool

#Output

We want in json format only and  if its error then show error and its reasons
And also went tool return something you need to analyze that content and give it back in json format
'''
agent=create_agent(model=llm,tools=tool_box,system_prompt=prompt)


val=agent.invoke({'messages':[HumanMessage(content='is my flight delay AI171')]})

def flight_run(msg : str):
    response=agent.invoke({
        'messages':HumanMessage(content=msg)
    })
    return response['messages'][-1].content