import assert from "node:assert/strict";
import { aiEngine } from "../src/index.js";
import { resetQuotaForTests } from "../src/engine/quota-manager.js";
import { resetUsageLogsForTests } from "../src/engine/usage-logger.js";

process.env.NODE_ENV = "test";
process.env.FREE_DAILY_AI_LIMIT = "1";

resetQuotaForTests();
resetUsageLogsForTests();

const lab = {
  labId: "sample-lab-1",
  labTitle: "Create and Review Sample Records",
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
      question: "How many records did you create?",
      type: "number",
      expectedValue: 2
    }
  ]
};

const success = await aiEngine.run(
  "verify-lab",
  {
    lab,
    studentAnswers: {
      q1: "Sample Training Account",
      q2: 2
    }
  },
  {
    userId: "test-user",
    tier: "free"
  }
);

assert.equal(success.ok, true);
assert.equal(success.data.passed, true);
assert.equal(success.data.score, 100);
assert.equal(success.usage.remainingToday, 0);

const quotaExceeded = await aiEngine.run(
  "verify-lab",
  {
    lab,
    studentAnswers: {
      q1: "Sample Training Account",
      q2: 2
    }
  },
  {
    userId: "test-user",
    tier: "free"
  }
);

assert.equal(quotaExceeded.ok, false);
assert.equal(quotaExceeded.error.code, "AI_QUOTA_EXCEEDED");

const unsupported = await aiEngine.run("unknown-task");

assert.equal(unsupported.ok, false);
assert.equal(unsupported.error.code, "AI_ENGINE_ERROR");

console.log("ai-engine tests passed");
