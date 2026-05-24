# SentinelFlow Migration Map

`SentinelFlow` is the existing SentinelFlow app source.

This monorepo keeps the original app separated by responsibility instead of copying the entire old root into one mixed folder.

## Source Mapping

| SentinelFlow source | Zentom Suite destination | Purpose |
| --- | --- | --- |
| `SentinelFlow/website/` | `apps/sentinelflow-web/` | SentinelFlow static product website |
| `SentinelFlow/force-app/` | `apps/sentinelflow-salesforce/force-app/` | Salesforce package metadata |
| `SentinelFlow/manifest/` | `apps/sentinelflow-salesforce/manifest/` | Salesforce deployment manifests |
| `SentinelFlow/.forceignore` | `apps/sentinelflow-salesforce/.forceignore` | Salesforce deploy ignore rules |
| `SentinelFlow/src/` | `services/zentom-api/legacy-sentinelflow-node/src/` | Existing Node API and dashboard service |
| `SentinelFlow/package.json` | `services/zentom-api/legacy-sentinelflow-node/package.json` | Existing Node service scripts and dependencies |
| `SentinelFlow/server.js` | `services/zentom-api/legacy-sentinelflow-node/server.js` | Existing Node server entry |
| `SentinelFlow/zentom-ai/` | `services/zentom-ai-engine/legacy-zentom-ai/` | Existing Python Zentom AI service |

## Excluded During Migration

- `SentinelFlow/.git/`
- `SentinelFlow/.sf/`
- `SentinelFlow/.sfdx/`
- `SentinelFlow/node_modules/`
- `SentinelFlow/coverage/`
- `SentinelFlow/tmp/`
- `SentinelFlow/temp_deploy/`
- `SentinelFlow/zentom-ai/venv/`
- `SentinelFlow/zentom-ai/.env`
- `SentinelFlow/zentom-ai/zentom.db`
- generated `__pycache__/` directories

## Forward Direction

The clean target architecture remains:

- `services/zentom-api/`: FastAPI backend API
- `services/zentom-ai-engine/`: AI model routing and recommendations
- `services/zentom-policy-engine/`: risk, approval, and action rules
- `services/zentom-memory-engine/`: replay, incident memory, and vector search
- `services/zentom-integration-engine/`: Salesforce, Agentforce, and webhook clients

The migrated legacy folders are preserved so existing behavior is not lost while the code is gradually refactored into the clean module boundaries.
