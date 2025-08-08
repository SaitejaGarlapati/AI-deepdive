from dotenv import load_dotenv
load_dotenv()

from loader import load_docs_from_urls
from embeddings import build_vectorstore
from qa_chain import build_qa_chain

# Load env vars (especially the Hugging Face token)
load_dotenv()

def main():
    urls = [
    # "https://raw.githubusercontent.com/huggingface/transformers/main/README.md",
    "https://raw.githubusercontent.com/langchain-ai/langchain/master/README.md",
]

    texts = load_docs_from_urls(urls)
    vectorstore = build_vectorstore(texts)
    qa_chain = build_qa_chain(vectorstore)

    while True:
        query = input("\nAsk a question (or 'exit'): ")
        if query.lower() == "exit":
            break
        print("Calling LLM...")
        result = qa_chain.invoke(query)
        print("Received response ✅")
        print("\n🧠 Answer:")
        print(result["result"])

if __name__ == "__main__":
    main()
