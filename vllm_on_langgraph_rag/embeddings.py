from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def prepare_retriever(texts):
    documents = [Document(page_content=t) for t in texts]

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        # This model will turn text into dense vector representations
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(split_docs, embeddings) # retriever

    return vectorstore.as_retriever()
