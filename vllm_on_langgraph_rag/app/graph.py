from langgraph.graph import StateGraph, START, END
from .state import GraphState
from .nodes import retrieve_node, generate_node

def build_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()
