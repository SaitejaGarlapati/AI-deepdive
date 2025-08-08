from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from transformers import pipeline

llm_pipeline = pipeline(
    task="text2text-generation",  # For Zephyr, Flan, T5
    # model="google/flan-t5-large",  # or mistralai/Mistral-7B-Instruct, etc.
    model="HuggingFaceH4/zephyr-7b-beta",
    device=0  # Or -1 for CPU
)
    
# Node: Retrieve top-k relevant docs
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
    Use the following context to answer the question.
    If unsure, say you don’t know.

    Context:
    {context}

    Question:
    {query}
    """
    
    output = llm_pipeline(prompt, max_new_tokens=512, temperature=0.3)
    answer = output[0]["generated_text"].strip()

    return {**state, "answer": answer}
