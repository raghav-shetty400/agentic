from typing import TypedDict

class AgentState(TypedDict):

    question:str

    username:str

    user:dict

    device:dict

    subscription:dict

    settings:list

    events:list

    answer:str

    route:str