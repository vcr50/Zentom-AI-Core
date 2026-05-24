# Hosted AI Strategy

## 1. Current Hosted Mode: RULE

The hosted Zentom API on Render remains in `AI_MODE=RULE` for beta.

Hosted beta environment:

```env
AI_MODE=RULE
AI_PROVIDER=LOCAL
AI_MODEL=zentom-rule-v1
LOCAL_LLM_URL=
LOCAL_LLM_MODEL=
```

This mode keeps the Salesforce integration stable:

```text
Salesforce -> Render Zentom API -> Hosted PostgreSQL -> Salesforce write-back
```

Hosted RULE mode already verifies risk scoring, policy decisions, runbook selection, incident persistence, and Salesforce write-back without depending on a hosted LLM.

## 2. Local AI Mode: Ollama HYBRID

Local development and advanced demos can continue using:

```env
AI_MODE=HYBRID
AI_PROVIDER=LOCAL
LOCAL_LLM_MODEL=phi3:mini
EMBEDDING_MODEL=all-minilm
```

Local AI stack:

```text
Zentom API
-> Ollama phi3:mini
-> all-minilm embeddings
-> PostgreSQL + pgvector
-> Memory/RAG context
```

This mode proves the higher-value AI path while keeping model serving on the developer machine.

## 3. Why Ollama Is Not Hosted Yet

Do not host Ollama on Render free tier for beta.

Reasons:

- Ollama models need more memory, storage, and CPU than a free web service is designed to provide.
- Model startup and cold-start behavior can slow or break incident workflows.
- Hosted model serving adds infrastructure cost before customer value is validated.
- Salesforce integration already works reliably in RULE mode.
- Online beta should prove the product workflow before adding hosted AI complexity.

## 4. Future Hosted AI Options

Option A: Keep RULE mode for beta.

Best for first private beta because it is stable, cheap, and easy to support.

Option B: Use a paid or low-cost model API later.

This can add hosted natural-language reasoning without operating model infrastructure.

Option C: Host Ollama on a VPS or GPU server later.

This preserves local-model control but requires server sizing, monitoring, storage, upgrades, and security hardening.

Option D: Hybrid customer-side local model gateway.

Enterprise customers can run their own local model gateway while Zentom Cloud stays lightweight and policy-controlled.

## 5. Security Rule: Never Expose Ollama Directly

Ollama must never be exposed directly to the public internet.

If hosted/local model access is needed later:

- Put it behind the Zentom API.
- Require authentication and network restrictions.
- Apply request validation and rate limits.
- Keep policy and safety checks in the API layer.
- Do not publish raw Ollama ports or unauthenticated model endpoints.

## 6. Decision: Hosted API Remains RULE Mode For Beta

Decision:

```text
Beta online mode = RULE
Advanced local demo mode = HYBRID Ollama
Production hosted AI provider = decide after beta validation
```

This keeps the hosted product reliable while preserving a clear path to richer AI once users validate the workflow.
