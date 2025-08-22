import os
from .graph import build_graph

def main():
    question = os.environ.get("QUESTION", "Explain what this pipeline is doing, briefly.")
    graph = build_graph()
    result = graph.invoke({"question": question})
    print("\n=== ANSWER ===")
    print(result.get("answer", ""))
    print("\n=== TRACES ===")
    for t in result.get("traces", []):
        print("-", t)

if __name__ == "__main__":
    main()
