Usage:
- LangChain
- FAISS (as the vector store)
- HuggingFace LLM
- Python

langchain_rag_demo/
├── main.py               # Entrypoint: sets up the chain and runs the query
├── loader.py             # Loads public documents (markdown or HTML)
├── embeddings.py         # Sets up embeddings and vector store (FAISS)
├── qa_chain.py           # Builds the RAG pipeline using LangChain
├── docs/                 # Stores downloaded documents
└── requirements.txt      # Dependencies