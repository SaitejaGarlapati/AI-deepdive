# from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from transformers import pipeline

llm_pipeline = pipeline(
    task="text-generation",  # 'test-generation' for llama and 'text2text-generation' for other small models
    # model="google/flan-t5-large",  # or mistralai/Mistral-7B-Instruct, etc.
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    # device=0  # Or -1 for CPU
)
    
# Node: Retrieve top-k relevant docs
# Can add branching: e.g., "generate" → "summarize" if answer is too long
def retrieve_node(state):
    retriever = state["retriever"]
    query = state["query"]
    docs = retriever.get_relevant_documents(query)
    return {**state, "docs": docs}

# Node: Generate answer using context
def generate_node(state):
    query = state["query"]
    context = "\n\n".join([doc.page_content for doc in state["docs"]])

    prompt = f"""
    You are an expert AI assistant. 
    Use the following context to answer the user's question as clearly and concisely as possible. 
    If the answer isn't in the context, say you don't know.

    Context:
    {context}

    Question:
    {query}
    """
    
    output = llm_pipeline(prompt, max_new_tokens=512, temperature=0.3)
    answer = output[0]["generated_text"].strip()

    return {**state, "answer": answer}
