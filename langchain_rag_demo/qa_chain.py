from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA

def build_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta", 
        model_kwargs={"temperature": 0.5, "max_length": 1024}
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return chain