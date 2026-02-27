from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from payment_gateway_agent import Tools
from langchain.messages import HumanMessage
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",   
    temperature=0.3,
    timeout=2
)


tool_box=[Tools.api_create_order,Tools.api_get_order,Tools.checkout]
prompt='''
#Overview
You are an payment_gateway assistant for lounge booking.
You need solve the user query based on their requirements

#tools details to call

@tool name :- api_create_order - Use this tool when User wants to start a payment  (user_id,token_fee and lounge_fee needed)
@tool name :- api_get_order - Use this tool when User is asking about an existing order (order_id needed)
@tool name :- flight_depart - Use this tool whenUser wants to see payment details before paying (order_id needed)


#Rules

- Dont call more than one tool
- Analyze the user requirement and then answer them accordingly 
- Dont add anything to that just return as it answer from tool

#Output

We want in json format only and  if its error then show error and its reasons
And also went tool return something you need to analyze that content and give it back in json format
'''
agent=create_agent(model=llm,tools=tool_box,system_prompt=prompt)

def payment_run(msg : str):
    response=agent.invoke({
        'messages':HumanMessage(content=msg)
    })
    return response['messages'][-1].content