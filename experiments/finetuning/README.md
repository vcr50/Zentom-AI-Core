# Zentom Fine-tuning Experiments

This workspace is for local/free LoRA or QLoRA experiments only.

## Status

- Milestone 15C: Dataset quality checker is available.
- Milestone 15D: Fine-tuning experiment workspace is scaffolded.
- No production Zentom model is replaced by anything in this folder.

## Dataset

Default dataset path:

```text
datasets/zentom/zentom_alpaca_v0_1.json
```

Expected Alpaca record shape:

```json
{
  "instruction": "You are Zentom AI...",
  "input": "Incident Type: ...",
  "output": "{\"summary\":\"...\",\"rootCause\":\"...\",\"recommendedAction\":\"...\",\"confidenceScore\":85,\"runbookKey\":\"...\"}"
}
```

## Quality Gate

Run:

```powershell
python experiments\finetuning\dataset_quality_check.py --json
```

The checker validates:

- dataset count
- missing `instruction`, `input`, or `output`
- invalid JSON in `output`
- duplicate examples
- too-short examples
- safety instruction coverage
- `runbookKey` in output
- `confidenceScore` in output

## Dataset Size Guidance

- `100+` examples: basic experiment.
- `500+` examples: useful pattern learning.
- `1000+` examples: stronger result.

The current exported artifact may be smaller than this. Treat low-count runs as pipeline validation only.

## Dry-run Experiment

Run:

```powershell
python experiments\finetuning\train_lora_experiment.py --dry-run
```

The script checks dataset readiness and prints the planned training configuration. It does not train by default.

## Future Training Path

Future implementation can use:

- Unsloth for free/local QLoRA notebooks.
- Hugging Face `transformers`, `datasets`, `peft`, and `trl`.
- A small instruct model suitable for local experimentation.

## Safety Rules

- Do not fine-tune or replace the production Zentom model from this workspace.
- Do not train on secrets, credentials, access tokens, personal data, or proprietary customer payloads.
- Keep policy, risk, approval, and runbook safety controls in every training instruction.
- Treat fine-tuned output as recommendation text only. Production execution remains controlled by policy and approval systems.
