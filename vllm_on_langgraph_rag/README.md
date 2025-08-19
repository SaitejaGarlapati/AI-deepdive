## vLLM Orchestration on RAG using LangGraph

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

Tried models:
```
- meta-llama/Meta-Llama-3-8B-Instruct
- mistralai/Mistral-7B-Instruct
- HuggingFaceH4/zephyr-7b-beta
- google/flan-t5-large
```

Use a state machine model:
→ user_input → retrieve_docs → generate_response → check_user_followup → (loop or exit)


Run with vLLM (default): `USE_VLLM=1 python3 main.py`

Run with local HuggingFace pipeline: `USE_VLLM=0 python3 main.py`