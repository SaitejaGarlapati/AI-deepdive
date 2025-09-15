# TensorZero + vLLM (Gaudi) Local Setup

This folder shows how to integrate vLLM with TensorZero for routing, metrics, and observability.

## Overview
- vLLM: Inference server (serving Meta-Llama-3-8B-Instruct on Gaudi).
- TensorZero Gateway: Sits in front of vLLM to route requests, capture metrics, and expose a UI.
- ClickHouse: Stores inference logs.
- TensorZero UI: Web UI to explore metrics, traces, and feedback.

## Prerequisites
- Ensure vLLM is running. Follow `vllm-setup-demo/README.md` to setup vLLM.

## Configure TensorZero
```
tensorZero/
├── .env
├── config/
│   └── tensorzero.toml
└── docker-compose.yml
```

### Start everything
Path: tensorZero/
```
docker compose up -d
```

## Usage

### Call through TensorZero /inference API
```
curl -X POST http://localhost:3000/inference \
  -H "Content-Type: application/json" \
  -d '{
    "function_name": "chat_basic",
    "input": {
      "messages": [{"role":"user","content":"Tell me about Gaudi HPUs"}]
    }
  }'
```

### Explore the UI
Gateway: `http://localhost:3000`
UI Dashboard: `http://localhost:4000`