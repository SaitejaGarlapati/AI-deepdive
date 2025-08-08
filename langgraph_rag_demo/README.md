





langgraph_rag_demo/
├── main.py               # Entry: starts the graph-based agent
├── nodes.py              # Each node (function) in the graph
├── graph.py              # LangGraph DAG definition and construction
├── loader.py             # (reuse from langchain folder) Fetch docs from the web
├── embeddings.py         # (reuse from langchain folder) Embed and store chunks in FAISS
├── prompt_template.txt   # custom prompt
├── requirements.txt



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