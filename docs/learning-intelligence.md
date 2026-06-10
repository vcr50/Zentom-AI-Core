# Learning Intelligence

The learning intelligence layer contains education-facing AI workflows such as
tutoring, lab verification, mastery evaluation, interview coaching, code review,
skill analysis, and project audit support.

## First End-to-End Flow

The first flow to prove is rule-based only:

```text
Admin Module 1
Hands-on Lab
Check My Work
Zentom AI Learning Intelligence
Score + feedback
Skill Passport update
```

The Academy backend should call `aiEngine.run("verify-lab", ...)` through its
`/api/ai/run` endpoint. Model providers are intentionally not required for this
flow.

For an Express backend, use `createAcademyAiHandler` and provide the Academy
Skill Passport persistence function:

```js
import { createAcademyAiHandler } from "zentom-ai-core";

app.post("/api/ai/run", createAcademyAiHandler({
  async updateSkillPassport({ userId, update }) {
    await skillPassportService.updateLabProgress(userId, update);
  }
}));
```

Keep private curriculum, learner data, assessment answers, scoring rubrics, and
customer-specific examples out of this document.
