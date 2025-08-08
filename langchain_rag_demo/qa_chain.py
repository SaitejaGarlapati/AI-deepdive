from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

def build_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # Use local HF pipeline for stability
    hf_pipeline = pipeline(
        "text2text-generation",
        model="HuggingFaceH4/zephyr-7b-beta",
        device=0
    )

    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return chain