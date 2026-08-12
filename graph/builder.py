from langgraph.graph import StateGraph, START, END

from graph.state import AgentState
from graph.router import router
from graph.conditional_edges import route_question

from nodes.ask_username import ask_username
from nodes.support_agent import support_agent
from nodes.response import response
from nodes.log_node import log_node      # <-- NEW
from nodes.llm_agent import llm_agent

# Create graph
workflow = StateGraph(AgentState)

# ---------------- Nodes ----------------

workflow.add_node("router", router)
workflow.add_node("ask_username", ask_username)
workflow.add_node("support_agent", support_agent)
workflow.add_node("log_node", log_node)   # <-- NEW
workflow.add_node("llm_agent", llm_agent)
workflow.add_node("response", response)

# ---------------- Start ----------------

workflow.add_edge(START, "router")

# ---------------- Conditional Edge ----------------

workflow.add_conditional_edges(
    "router",
    route_question,
    {
        "support": "ask_username",
        "rag": "response"
    }
)

# ---------------- Normal Edges ----------------

workflow.add_edge("ask_username", "support_agent")
workflow.add_edge("support_agent", "log_node")
workflow.add_edge("log_node", "response")     
workflow.add_edge("response", END)

# ---------------- Compile ----------------

graph = workflow.compile()