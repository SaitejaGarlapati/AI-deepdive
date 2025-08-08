from dotenv import load_dotenv
from loader import load_docs_from_urls
from embeddings import prepare_retriever
from graph import build_graph
import os

load_dotenv()
print("Token loaded:", os.getenv("HUGGINGFACEHUB_API_TOKEN"))

def main():

    urls = [
        "https://docs.langchain.com/docs/expression_language",
        "https://docs.langchain.com/docs/integrations/document_loaders/",
        "https://huggingface.co/docs/transformers/index"
    ]

    print("Fetching docs...")
    docs = load_docs_from_urls(urls)

    print("Embedding and indexing...")
    retriever = prepare_retriever(docs)

    print("Building graph...")
    run_graph = build_graph(retriever)

    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() == "exit":
            break
        print("Calling LLM...")
        answer = run_graph.invoke(q)
        print("Received response ✅")
        print("\n🧠 Answer:\n", answer)

if __name__ == "__main__":
    main()
