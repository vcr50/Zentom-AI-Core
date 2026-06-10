# Zentom Admin Console

Internal admin dashboard for tenant setup, diagnostics, support operations, and enterprise controls.

## Features

- **Sidebar Navigation** — Organized sections: Overview, Tenants, Incidents, AI Engine, Policy, Diagnostics, Settings
- **Key Metrics** — Total tenants, active incidents, AI requests/day, system uptime, open approvals, avg response time
- **Tenant Management** — View all tenants with plan badges (Free/Pro/Enterprise), status indicators, and quick actions
- **Incident Monitor** — Real-time incident table with severity badges, tenant mapping, and AI confidence scores
- **AI Engine Panel** — LLM provider stats, model usage, latency metrics, and token consumption
- **Policy Engine** — Active rules, approval queue, risk engine status, compliance score
- **Diagnostics** — System health bars (API, DB, Redis, Celery, AI, Salesforce), error rate chart, recent errors log
- **Activity Feed** — Real-time audit trail of all admin actions with timestamps
- **Quick Actions** — Add tenant, run diagnostics, export data, emergency shutdown

## How to Use

Open `index.html` in your browser — no server required. All data is simulated for demo purposes.

## Source

🔗 [github.com/vcr50/salesforce-ops-monitoring-platform](https://github.com/vcr50/salesforce-ops-monitoring-platform)

