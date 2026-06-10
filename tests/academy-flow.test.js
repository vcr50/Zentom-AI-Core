import assert from "node:assert/strict";
import { aiEngine, buildSkillPassportUpdate } from "../src/index.js";
import { resetQuotaForTests } from "../src/core/quota-manager.js";
import { resetUsageLogsForTests } from "../src/core/usage-logger.js";

process.env.NODE_ENV = "test";
process.env.FREE_DAILY_AI_LIMIT = "10";

resetQuotaForTests();
resetUsageLogsForTests();

const req = {
  session: {
    user: {
      id: "academy-test-user",
      tier: "free"
    }
  },
  body: {
    task: "verify-lab",
    params: {
      lab: {
        labId: "admin-module-1-lab",
        labTitle: "Admin Module 1 Hands-on Lab",
        passingScore: 80,
        criteria: [
          {
            id: "q1",
            question: "What account name did you create?",
            type: "text",
            expectedKeywords: ["Sample Training Account"]
          },
          {
            id: "q2",
            question: "How many sample records did you create?",
            type: "number",
            expectedValue: 2
          }
        ]
      },
      studentAnswers: {
        q1: "Sample Training Account",
        q2: 2
      }
    }
  }
};

const result = await aiEngine.run(req.body.task, req.body.params, {
  userId: req.session?.user?.id,
  tier: req.session?.user?.tier || "free"
});

assert.equal(result.ok, true);
assert.equal(result.task, "verify-lab");
assert.equal(result.mode, "rule-based");
assert.equal(result.data.passed, true);
assert.equal(result.data.score, 100);

const passportUpdate = buildSkillPassportUpdate({
  labResult: result.data,
  moduleId: "admin-module-1",
  skillId: "admin-hands-on-basics"
});

assert.equal(passportUpdate.moduleId, "admin-module-1");
assert.equal(passportUpdate.skillId, "admin-hands-on-basics");
assert.equal(passportUpdate.status, "verified");
assert.equal(passportUpdate.score, 100);
assert.ok(passportUpdate.feedback);
assert.ok(passportUpdate.verifiedAt);

console.log("academy flow test passed");
