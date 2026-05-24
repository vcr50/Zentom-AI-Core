# Zentom Training Dataset

This folder stores exported Zentom memory datasets for local fine-tuning experiments.

## Files

- `zentom_alpaca_v0_1.json` - Alpaca-format JSON dataset exported from Zentom memory entries.

## Alpaca JSON Format

Each record is a JSON object with:

- `instruction` - the training instruction for Zentom AI.
- `input` - incident context, risk, policy, runbook, and source payload details.
- `output` - expected safe recommendation output as a JSON string.

Example:

```json
{
  "instruction": "You are Zentom AI...",
  "input": "Incident Type: ...",
  "output": "{\"summary\":\"...\",\"rootCause\":\"...\",\"recommendedAction\":\"...\"}"
}
```

## JSONL Format

The API can also export JSONL, where each line is one Alpaca-format record:

```text
{"instruction":"...","input":"...","output":"..."}
{"instruction":"...","input":"...","output":"..."}
```

Use:

```text
GET /api/dataset/export?format=jsonl
GET /api/dataset/export-jsonl
```

## Regenerating The JSON File

From the repository root:

```powershell
cd services/zentom-api
.\venv\Scripts\python.exe scripts\export_dataset.py
```

The export uses the configured `DATABASE_URL`. If the database is not running, start the local Zentom database first.

## Safety Rules

- This dataset is experimental and must not replace the production Zentom model.
- Only use records that passed Zentom dataset filtering rules.
- Do not include secrets, credentials, access tokens, customer personal data, or proprietary payloads.
- Keep policy, approval, risk, and runbook safety controls in every instruction.
- Treat fine-tuned outputs as recommendations only; production actions must still pass policy and approval checks.

## Current Training Guidance

The current dataset is intentionally small. Use this pipeline to prove export and training mechanics first.

- 100+ examples: basic experiment.
- 500+ examples: useful pattern learning.
- 1000+ examples: stronger result.
