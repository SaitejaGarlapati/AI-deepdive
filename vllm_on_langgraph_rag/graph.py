from langgraph.graph import StateGraph
from typing import TypedDict, List, Any
from nodes import retrieve_node, generate_node

# Defining what the state will look like
class RAGState(TypedDict):
    query: str
    retriever: Any
    docs: List[Any]
    answer: str

def build_graph(retriever):
    builder = StateGraph(RAGState)
    
    # Add each step (node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)

    # Connect them
    builder.set_entry_point("retrieve")
    builder.add_edge("retrieve", "generate")
    builder.set_finish_point("generate")

    graph = builder.compile()
    
    def run(query):
        result = graph.invoke({
            "query": query,
            "retriever": retriever,
        })
        return result["answer"]

    return run
