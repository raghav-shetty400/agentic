from langgraph.graph import StateGraph, START, END

from graph.state import AgentState
from graph.router import router
from graph.conditional_edges import route_question

from nodes.ask_username import ask_username
from nodes.find_user import find_user
from nodes.support_agent import support_agent
from nodes.log_node import log_node
from nodes.llm_agent import llm_agent
from nodes.response import response


# =====================================================
# CREATE GRAPH
# =====================================================

workflow = StateGraph(AgentState)


# =====================================================
# NODES
# =====================================================

workflow.add_node(
    "router",
    router
)

workflow.add_node(
    "ask_username",
    ask_username
)

workflow.add_node(
    "find_user",
    find_user
)

workflow.add_node(
    "support_agent",
    support_agent
)

workflow.add_node(
    "log_node",
    log_node
)

workflow.add_node(
    "llm_agent",
    llm_agent
)

workflow.add_node(
    "response",
    response
)


# =====================================================
# START
# =====================================================

workflow.add_edge(
    START,
    "router"
)


# =====================================================
# ROUTING
# =====================================================

workflow.add_conditional_edges(
    "router",
    route_question,
    {
        # Device/account issue
        "support": "ask_username",

        # Normal/general question
        "rag": "llm_agent"
    }
)


# =====================================================
# SUPPORT FLOW
# =====================================================

workflow.add_edge(
    "ask_username",
    "find_user"
)

workflow.add_edge(
    "find_user",
    "support_agent"
)

workflow.add_edge(
    "support_agent",
    "log_node"
)

workflow.add_edge(
    "log_node",
    "llm_agent"
)


# =====================================================
# LLM → RESPONSE
# =====================================================

workflow.add_edge(
    "llm_agent",
    "response"
)


# =====================================================
# END
# =====================================================

workflow.add_edge(
    "response",
    END
)


# =====================================================
# COMPILE
# =====================================================

graph = workflow.compile()