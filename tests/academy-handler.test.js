import assert from "node:assert/strict";
import { createAcademyAiHandler } from "../src/index.js";
import { resetQuotaForTests } from "../src/core/quota-manager.js";
import { resetUsageLogsForTests } from "../src/core/usage-logger.js";

process.env.NODE_ENV = "test";
process.env.FREE_DAILY_AI_LIMIT = "10";

resetQuotaForTests();
resetUsageLogsForTests();

const savedUpdates = [];

const handler = createAcademyAiHandler({
  async updateSkillPassport(event) {
    savedUpdates.push(event);
  }
});

const req = {
  session: {
    user: {
      id: "academy-handler-user",
      tier: "free"
    }
  },
  body: {
    task: "verify-lab",
    moduleId: "admin-module-1",
    skillId: "admin-hands-on-basics",
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
          }
        ]
      },
      studentAnswers: {
        q1: "Sample Training Account"
      }
    }
  }
};

let responseBody;

const res = {
  json(payload) {
    responseBody = payload;
    return payload;
  }
};

await handler(req, res);

assert.equal(responseBody.ok, true);
assert.equal(responseBody.task, "verify-lab");
assert.equal(responseBody.data.score, 100);
assert.equal(responseBody.skillPassportUpdate.status, "verified");
assert.equal(savedUpdates.length, 1);
assert.equal(savedUpdates[0].userId, "academy-handler-user");
assert.equal(savedUpdates[0].update.moduleId, "admin-module-1");
assert.equal(savedUpdates[0].update.skillId, "admin-hands-on-basics");

console.log("academy handler test passed");
