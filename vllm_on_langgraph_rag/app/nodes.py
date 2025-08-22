from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .config import cfg

def get_llm() -> ChatOpenAI:
    """
    Returns a LangChain ChatOpenAI LLM configured either for local vLLM (OpenAI-compatible)
    or real OpenAI, depending on env.
    """
    if cfg.provider == "vllm":
        # Point ChatOpenAI at your local vLLM server
        return ChatOpenAI(
            api_key=cfg.vllm_api_key,
            base_url=cfg.vllm_api_base,
            model=cfg.vllm_model,
            # you can set timeouts, max_tokens, temperature here, or per-call
        )
    else:
        # Real OpenAI fallback
        return ChatOpenAI(
            api_key=cfg.openai_api_key,
            model=cfg.openai_model,
        )

def retrieve_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Stub retriever: in real life, plug your RAG here (Elastic, PGVector, Weaviate, etc.).
    For now, we just echo a tiny context so the flow is complete.
    """
    q = state["question"]
    context = f"(stub) No external retrieval yet. Question was: {q}"
    traces = state.get("traces", [])
    traces.append("retrieve_node: provided stub context")
    return {**state, "context": context, "traces": traces}

def generate_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calls the LLM through LangChain, which routes to your vLLM OpenAI server (or OpenAI).
    """
    llm = get_llm()
    sys_prompt = (
        "You are a concise, helpful assistant. "
        "Use the provided context when relevant. If context is not useful, continue anyway."
    )
    messages = [
        SystemMessage(content=sys_prompt),
        HumanMessage(content=f"Context:\n{state.get('context','(none)')}\n\nQuestion:\n{state['question']}"),
    ]
    resp = llm.invoke(messages)
    answer = resp.content if hasattr(resp, "content") else str(resp)
    traces = state.get("traces", [])
    traces.append("generate_node: got answer from LLM")
    return {**state, "answer": answer, "traces": traces}
