from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from lounge_management_agent import Tools
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",   
    temperature=0.3,
    timeout=2
)

tool_box=[Tools.get_lounge_details,Tools.get_sessions,Tools.lounge_checkin,Tools.lounge_checkout,Tools.lounge_waitlist,Tools.promote_waitlisted_user]
prompt='''
#Overview
You are an airport lounge assistant.
You need solve the user query based on their requirements

#tools details to call

@tool 1 - get_lounge_details - Use this tool when you want the lounge_details (lounge_id needed)
@tool 2 - get_sessions - Use this tool when you want sessions related details (lounge_id needed)
@tool 3 - lounge_checkin - Use this tool when you want the lounge_checkin details (lounge_id and user_id needed) 
@tool 4 - lounge_checkout - Use this tool when you want the lounge_checkout details (session_id needed)
@tool 5 - lounge_waitlist - Use this tool when you want the lounge waitlist details (lounge_id and user_id needed)
@tool 6 - promote_waitlisted_user - Use this tool when you want to promote user in the waitlisted (lounge_id is needed)

#Rules

- Dont call more than one tool
- Analyze the user requirement and then answer them accordingly 
- Dont add anything to that just return as it answer from tool

#Output

We want in json format only and  if its error then show error and its reasons
And also went tool return something you need to analyze that content and give it back in json format
'''
agent=create_agent(model=llm,tools=tool_box,system_prompt=prompt)

def lounge_man_run(msg : str):
    response=agent.invoke({
        'messages':HumanMessage(content=msg)
    })
    return response['messages'][-1].content