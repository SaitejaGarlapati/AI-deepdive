## Retrieval-Augmented Generation (RAG) pipeline using LangGraph

LangGraph gives you full control over the workflow as a dataflow graph, which makes it ideal for:
- Multi-step decision agents
- Retry flows
- Conditional logic
- Dynamic tool selection

```
langgraph_rag_demo/
├── main.py               # Entry: starts the graph-based agent
├── nodes.py              # Each node (function) in the graph
├── graph.py              # LangGraph DAG definition and construction
├── loader.py             # (reuse from langchain folder) Fetch docs from the web
├── embeddings.py         # (reuse from langchain folder) Embed and store chunks in FAISS
├── prompt_template.txt   # custom prompt
├── requirements.txt
```


Use a state machine model:
→ user_input → retrieve_docs → generate_response → check_user_followup → (loop or exit)

difference

```
Feature	               LangChain	                         LangGraph
Flow	           Query → Retrieve → Answer	Dynamic: Ask → Retrieve → Respond → Branch
Context Reuse	   Not persistent	            Fully stateful
Multiple Rounds	   Manual loop	                Natural
Decisions	       Hardcoded logic	            Conditional node edges
Debuggability	   Harder to trace	            You can visualize the graph! (graph.get_graph().draw_ascii())
```

Differences:
- LangChain and LangGraph are frameworks to build LLM apps
- LangChain is the main LLM orchestration framework: it gives you tools, wrappers, memory, 
   agents, chains, RAGs, tools, etc.
- LangGraph is an extension of LangChain, built specifically to model stateful, graph-based
   LLM workflows.
- LangGraph is a power mode inside LangChain. (not a replacement), but a move advanced layer
