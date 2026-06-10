# Zentom AI Core

Zentom AI Core is a reusable AI orchestration layer for product workflows.

Zentom AI Core is divided into reusable core services and product-specific
intelligence layers.

SentinelFlow uses the Operations Intelligence layer for incident reasoning,
root cause analysis, runbook recommendation, and human-approved operational
actions.

TomCodeX Academy uses the Learning Intelligence layer for AI tutoring, lab
verification, interview coaching, code review, Skill Passport scoring, and POC
project guidance.

## Confidentiality

This repository may contain company-owned implementation details. Do not publish
customer data, credentials, tokens, private URLs, internal environment values,
runbook details, or proprietary operational procedures in README files.

Use local `.env` files, private deployment notes, or the company knowledge base
for sensitive setup details.

## Repository Layout

```text
src/core/                            Shared AI engine services
src/intelligence-layers/operations/ Operations intelligence layer
src/intelligence-layers/learning/    Learning intelligence layer
src/providers/                       Model provider integrations
src/knowledge/                       Product knowledge placeholders
src/utils/                           Shared utilities
examples/                            Sanitized usage examples
docs/                                High-level documentation
tests/                               Validation tests
```

## Architecture

`core/` contains common services used by every intelligence layer: routing,
provider selection, quota checks, logging, response normalization, safety
guarding, and fallback behavior.

`intelligence-layers/operations/` contains the operations-facing reasoning
surface.

`intelligence-layers/learning/` contains the learning-facing tutoring,
verification, coaching, code review, scoring, and project guidance surface.

`knowledge/` stores sanitized knowledge placeholders. Do not commit private
curriculum, customer incident data, proprietary runbooks, production policy
rules, credentials, or environment-specific configuration.

## Development

Run the local MVP:

```powershell
npm install
npm test
npm start
```

Keep public README content high-level and avoid exposing environment-specific
configuration.
