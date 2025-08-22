import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LLMConfig:
    provider: str = os.getenv("LLM_PROVIDER", "vllm").lower()
    # vLLM (OpenAI-compatible server)
    vllm_api_base: str = os.getenv("VLLM_API_BASE", "http://localhost:8000/v1")
    vllm_api_key: str = os.getenv("VLLM_API_KEY", "dummy")
    vllm_model: str = os.getenv("VLLM_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
    # OpenAI (optional fallback)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

cfg = LLMConfig()
