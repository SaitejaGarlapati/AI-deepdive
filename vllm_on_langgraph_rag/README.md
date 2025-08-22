# LangGraph + vLLM (Gaudi) Starter

This is a minimal LangGraph workflow that calls a local **vLLM (Habana fork)**
server via the **OpenAI-compatible API**. Flip an env var to use real OpenAI.

## 1) Install deps
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## 2) Start the vLLM Server

```bash
mkdir -p volumes/hf_cache volumes/hpu_recipe_cache volumes/models
export HF_TOKEN=<place your HF token>

# Start vllm in the foreground so you can see logs
docker compose up vllm
# Wait until you see "Application startup complete." and healthcheck passing,
# then Ctrl+C and detach it:
docker compose up -d vllm

# Build and run app
docker compose build app
docker compose up --no-deps app
```

#### Check:
```
docker compose ps
docker logs -f gaudi-vllm
docker logs -f langgraph-app
curl http://127.0.0.1:8000/v1/models
```

(OR) 
start the server using manual steps
Steps from here: Running vLLM on Intel® Gaudi (HPU) with Docker


## 3) Run

```bash
QUESTION="Summarize LangGraph in 2 sentences." python3 -m app.run
```








# Manual setup for vLLM Server (Optional) -> already taken care in docker-compose

## Running vLLM on Intel® Gaudi (HPU) with Docker
This guide documents the full setup we used to run vLLM (Habana fork) on Gaudi HPUs using the official Habana PyTorch container.

### Steps

#### 1. Verify Gaudi drivers
`hl-smi`

#### 2. Pull Habana PyTorch Docker image
`docker pull vault.habana.ai/gaudi-docker/1.21.0/ubuntu22.04/habanalabs/pytorch-installer-2.6.0:latest`

#### 3. Run the container

Mount Hugging Face and HPU cache dirs so downloads/compilation persist:
```
mkdir -p ~/hf_cache ~/hpu_recipe_cache

docker run -it --runtime=habana \
  --cap-add=sys_nice --net=host --ipc=host \
  -e HABANA_VISIBLE_DEVICES=all \
  -e HF_TOKEN="$HF_TOKEN" \
  -e PT_HPU_RECIPE_CACHE_CONFIG='{"path":"/root/hpu_recipe_cache"}' \
  -v "${HF_HOME:-$HOME/hf_cache}:/root/.cache/huggingface" \
  -v "${HPU_RECIPE_CACHE:-$HOME/hpu_recipe_cache}:/root/hpu_recipe_cache" \
  --name gaudi-vllm \
  vault.habana.ai/gaudi-docker/1.21.0/ubuntu22.04/habanalabs/pytorch-installer-2.6.0:latest
```

#### 4. Verify PyTorch detects HPU

Inside the container:
```
python - <<'PY'
import torch
print("torch:", torch.__version__, "has_hpu:", hasattr(torch, "hpu"))
import habana_frameworks.torch as ht
print("habana_frameworks OK")
PY
```

You should see:
```
torch: <some-version> has_hpu: True
habana_frameworks OK
```

#### 5. Clone and install vLLM Habana fork
```
apt-get update && apt-get install -y git
git clone https://github.com/HabanaAI/vllm-fork.git
cd vllm-fork
pip install -r requirements/requirements-hpu.txt
python setup.py develop
```

#### 6. Launch the vLLM API server
```
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3-8B-Instruct \
  --device hpu \
  --dtype bfloat16 \
  --host 0.0.0.0 --port 8000 \
  --max-model-len 1024 \
  --max-num-seqs 4
```
You’ll see logs ending with:
`Application startup complete`
This means the server is live.

#### 7. Test the server (from host or another container shell)

List the models
`curl http://localhost:8000/v1/models`
Ensure the port is accessible

Send a chat request
```
curl http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer dummy" -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
    "messages": [{"role":"user","content":"Hello from Gaudi!"}]
  }'
```

References:
- https://github.com/HabanaAI/vllm-fork
- https://docs.habana.ai/en/latest/
- https://docs.habana.ai/en/latest/PyTorch/PyTorch_Overview.html
- https://vault.habana.ai/ui/native/gaudi-docker/
- https://docs.vllm.ai/en/latest/




Tried models:
```
- meta-llama/Meta-Llama-3-8B-Instruct
- mistralai/Mistral-7B-Instruct
- HuggingFaceH4/zephyr-7b-beta
- google/flan-t5-large
```


Run with vLLM (default): `USE_VLLM=1 python3 main.py`

Run with local HuggingFace pipeline: `USE_VLLM=0 python3 main.py`