# Customer Questions & Objection Log — Milestone 35D

## 1. Purpose
To systematically capture, track, and address customer questions and objections raised during Beta 2 demo sessions. This ensures we follow up correctly and refine our product messaging, feature set, and sales strategy.

## 2. Demo/Customer Context
- **Date:** [YYYY-MM-DD]
- **Customer / Organization:** [Company Name]
- **Audience:** [Target Audience/Roles]
- **Presenter:** [Name]

---

## 3. Customer Questions & Objections Log

| ID | Concern Category | Question / Objection | Response Given (During Demo) | Follow-up Needed? | Severity / Impact | Owner | Status |
|---|---|---|---|---|---|---|---|
| Q01 | Competition | We already use Salesforce. Why do we need this? | SentinelFlow acts as the operational governance layer *on top* of Salesforce. It catches the silent failures (flows, integrations) that Salesforce itself doesn't alert you about proactively. | [Yes/No] | High | [Name] | Open |
| Q02 | Product Scope | Does this replace Salesforce Case management? | No. It *integrates* with it. SentinelFlow detects the issue and automatically creates a pre-populated Case for your existing support team to work on. | [Yes/No] | Medium | [Name] | Open |
| Q03 | Governance | Can AI execute actions automatically? | Not in Beta. We enforce a "human-in-the-loop" model. The AI recommends an action based on policy, but a human must click 'Approve'. Full auto-heal is a future, opt-in feature. | [Yes/No] | High | [Name] | Open |
| Q04 | Security | Is customer data sent outside Salesforce? | We only send operational metadata (error codes, flow names, user IDs) to the Zentom API for risk scoring. We do *not* send PII or actual record data (like Account names or emails). | [Yes/No] | Critical | [Name] | Open |
| Q05 | Security | How secure is the hosted API? | The Zentom API runs on a secure, isolated infrastructure using HTTPS and token-based authentication. (Provide architecture diagram in follow-up). | [Yes/No] | Critical | [Name] | Open |
| Q06 | Product Scope | Can we use this without Slack/Agentforce? | Yes. SentinelFlow is fully functional within the Salesforce UI as a Command Center. Slack/Agentforce integrations are planned future extensions. | [Yes/No] | Low | [Name] | Open |
| Q07 | Integration | Can this work with our existing flows? | Yes. SentinelFlow monitors standard Salesforce platform events and apex exceptions, which apply to your existing flows automatically. | [Yes/No] | Medium | [Name] | Open |
| Q08 | Reliability | What happens if Zentom API is down? | SentinelFlow falls back to a local rules-based engine within Salesforce. The UI continues to work, and incidents are still logged, just without the neural risk score until the API recovers. | [Yes/No] | High | [Name] | Open |
| Q09 | Go-to-Market | Is this AppExchange/security-review ready? | We are currently in Beta 2. The package will undergo Salesforce AppExchange security review before general availability. | [Yes/No] | High | [Name] | Open |
| Q10 | Competition | How is this different from Datadog/ServiceNow? | Datadog monitors infrastructure. ServiceNow manages IT tickets. SentinelFlow specifically governs *Salesforce* operational incidents with native context (flows, apex, users). | [Yes/No] | Medium | [Name] | Open |

---

## 4. Response Principles
When addressing questions or objections during the demo, adhere to these principles:
- **Be honest.** If the feature doesn't exist, say so.
- **Do not oversell.** Don't promise capabilities that aren't on the immediate roadmap.
- **Explain current beta capability vs future roadmap.** Differentiate clearly between what is live today in Beta 2 and what is planned for the future.

## 5. Final Objection Summary
*(Brief summary of the most common or difficult objections raised during this session and how they were handled.)*
- [Summary text]
