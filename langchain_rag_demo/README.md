## Retrieval-Augmented Generation (RAG) pipeline using LangChain

Usage:
- LangChain
- FAISS (as the vector store)
- HuggingFace LLMs (ex: Zephyr, Mistral or Flan for faster model)
- Python
- Hugging Face Embeddings (MiniLM)
- Live internet documents (scraped from LangChain docs)

```
langchain_rag_demo/
├── main.py               # Entrypoint: sets up the chain and runs the query
├── loader.py             # Loads public documents (markdown or HTML)
├── embeddings.py         # Sets up embeddings and vector store (FAISS)
├── qa_chain.py           # Builds the RAG pipeline using LangChain
├── docs/                 # Stores downloaded documents
└── requirements.txt      # Dependencies
```

This pipeline:
- Fetches public docs
- Splits and embeds them
- Stores them in a searchable vector database
- Accepts a user query
- Finds the most relevant chunks
- Feeds them (with the query) to a Hugging Face LLM
- Generates an answer

--- 
RetrievalQA = Retrieval Question Answering
- LangChain's RetrievalQA:
    - Accepts a user query
    - Uses the retriever (FAISS) to get top-k chunks
    - Stuffs those chunks into a prompt with the query
    - Feeds it to the LLM
    - Returns the answer


```
                         ┌────────────┐
                         │ User Query │
                         └─────┬──────┘
                               │
                      ┌────────▼────────┐
                      │ Vector Retriever│ <--- Embedding Model
                      └────────┬────────┘
                               │
                ┌──────────────▼─────────────┐
                │ Prompt Template + LLM Call │
                └──────────────┬─────────────┘
                               │
                         ┌─────▼──────┐
                         │   Answer   │
                         └────────────┘
```