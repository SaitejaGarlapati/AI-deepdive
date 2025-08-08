from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

def build_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # Use local HF pipeline for stability
    hf_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-base", # LLM Model
        # device=0 # local inferencing
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever, # here retriever is FAISS
        return_source_documents=True
    )
    return chain