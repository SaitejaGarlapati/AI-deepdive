import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

def build_llm():
    # vLLM OpenAI-compatible server you launched on Gaudi
    return ChatOpenAI(
        base_url="http://localhost:8000/v1",
        api_key="EMPTY",
        model="meta-llama/Meta-Llama-3-8B-Instruct",  # or the HF ID you served via vLLM
        extra_body={"max_tokens": 512, "temperature": 0.3}
    )

def retrieve_node(state):
    retriever = state["retriever"]
    query = state["query"]
    docs = retriever.get_relevant_documents(query)
    return {**state, "docs": docs}

def generate_node(state):
    llm = build_llm()
    prompt = PromptTemplate.from_template(
        "Use the following context to answer the question. "
        "If you don't know, say you don't know.\n\n"
        "Context:\n{context}\n\nQuestion:\n{query}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    context = "\n\n".join(d.page_content for d in state["docs"])
    answer = chain.run({"context": context, "query": state["query"]})
    return {**state, "answer": answer}
