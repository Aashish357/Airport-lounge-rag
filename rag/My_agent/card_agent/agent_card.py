from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.messages import HumanMessage
from card_agent import Tools
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",   
    temperature=0.3,
    timeout=2
)


tool_box=[Tools.check_loungekey_exists,Tools.validate_bin,Tools.validate_card]
prompt='''


#tools details to call

@tool name :- check_loungekey_exists - Use this tool when you want to check loungekey exists or not (lounge_number needed)
@tool name :- validate_bin - Call this tool when the agent only needs card metadatas (bin_number needed)
@tool name :- validate_card - Call this tool when the agent must confirm if a card is usable(card_number,expiry_month,expiry_year,cvv needed)

#OverView
You are a card assistant.
- Choose EXACTLY ONE tool if required
- If information is missing, ask the user politely
- NEVER invent tools
- Return ONLY JSON

#Output

We want in json format only and  if its error then show error and its reasons
And also went tool return something you need to analyze that content and give it back in json format
'''
agent=create_agent(model=llm,tools=tool_box,system_prompt=prompt)



def card_run(msg : str):
    response=agent.invoke({
        'messages':HumanMessage(content=msg)
    })
    return response['messages'][-1].content