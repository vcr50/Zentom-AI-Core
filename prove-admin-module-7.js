import assert from "node:assert/strict";
import { aiEngine, buildSkillPassportUpdate, moduleProgression } from "./src/index.js";

// Helper to evaluate unlock decisions based on attempt history and tier
function getUnlockDecision({ studentAttempts, moduleId, tier }) {
  const currentConfig = moduleProgression.find(m => m.moduleId === moduleId);
  if (!currentConfig) {
    throw new Error(`Module configuration not found for ${moduleId}`);
  }

  const nextModuleId = currentConfig.nextModuleId;
  if (!nextModuleId) {
    return {
      eligibleToUnlock: false,
      reason: `No subsequent module after ${moduleId}.`
    };
  }

  const nextConfig = moduleProgression.find(m => m.moduleId === nextModuleId);
  if (!nextConfig) {
    throw new Error(`Configuration not found for next module ${nextModuleId}`);
  }

  const prerequisites = currentConfig.prerequisites || [];
  const summaryKey = `${moduleId}:summary`;
  const bestScore = studentAttempts[summaryKey]?.bestScore || 0;

  for (const prereq of prerequisites) {
    if (bestScore < prereq.minPassingScore) {
      return {
        eligibleToUnlock: false,
        reason: `Lab score of ${bestScore}% is below the passing score of ${prereq.minPassingScore}%.`
      };
    }
  }

  if (nextConfig.requiredTier === "founder" && tier !== "founder") {
    return {
      eligibleToUnlock: false,
      reason: `${nextConfig.moduleName} requires Founder Access.`
    };
  }

  return {
    eligibleToUnlock: true,
    reason: `Prerequisites met and tier authorized.`
  };
}

console.log("Starting Admin Module 7 progression proof...");

const studentAttempts = {};
const tier = "founder";

// 1. Simulate passing Admin Module 1
console.log("Simulating Admin Module 1 lab completion...");
const res1 = await aiEngine.run("verify-lab", {
  moduleId: "admin-1",
  labId: "admin-1-lab-1",
  studentAnswers: {
    q1: "TomCodeX Training Institute",
    q2: "Demo Student",
    q3: "TomCodeX Training Institute",
    q4: "My Active Accounts",
    q5: "Account Name, Phone"
  }
}, { userId: "founder-student-001", tier });

assert.equal(res1.ok, true);
assert.equal(res1.data.passed, true);
studentAttempts["admin-1:summary"] = { bestScore: res1.data.score };

// Check that Admin Module 2 unlocks
const unlock2 = getUnlockDecision({ studentAttempts, moduleId: "admin-1", tier });
assert.equal(unlock2.eligibleToUnlock, true);
console.log("✓ Admin Module 2 unlocked");

// 2. Simulate passing Admin Module 2
console.log("Simulating Admin Module 2 lab completion...");
const res2 = await aiEngine.run("verify-lab", {
  moduleId: "admin-2",
  labId: "admin-2-lab-1",
  studentAnswers: {
    q1: "Student__c",
    q2: "Course__c",
    q3: "Enrollment__c",
    q4: "Enrollment__c",
    q5: "Email, Phone"
  }
}, { userId: "founder-student-001", tier });

assert.equal(res2.ok, true);
assert.equal(res2.data.passed, true);
studentAttempts["admin-2:summary"] = { bestScore: res2.data.score };

// Check that Admin Module 3 unlocks
const unlock3 = getUnlockDecision({ studentAttempts, moduleId: "admin-2", tier });
assert.equal(unlock3.eligibleToUnlock, true);
console.log("✓ Admin Module 3 unlocked");

// 3. Simulate passing Admin Module 3
console.log("Simulating Admin Module 3 lab completion...");
const res3 = await aiEngine.run("verify-lab", {
  moduleId: "admin-3",
  labId: "admin-3-lab-1",
  studentAnswers: {
    q1: "Student Success User",
    q2: "Student__c",
    q3: "Create",
    q4: "flexible and user specific without changing profile",
    q5: "Read, Create"
  }
}, { userId: "founder-student-001", tier });

assert.equal(res3.ok, true);
assert.equal(res3.data.passed, true);
studentAttempts["admin-3:summary"] = { bestScore: res3.data.score };

// Check that Admin Module 4 unlocks
const unlock4 = getUnlockDecision({ studentAttempts, moduleId: "admin-3", tier });
assert.equal(unlock4.eligibleToUnlock, true);
console.log("✓ Admin Module 4 unlocked");

// 4. Simulate passing Admin Module 4
console.log("Simulating Admin Module 4 lab completion...");
const res4 = await aiEngine.run("verify-lab", {
  moduleId: "admin-4",
  labId: "admin-4-lab-1",
  studentAnswers: {
    q1: "Student Success CRM",
    q2: "Student__c",
    q3: "Course__c",
    q4: "Enrollment__c",
    q5: "Student Page Layout",
    q6: "Active Students"
  }
}, { userId: "founder-student-001", tier });

assert.equal(res4.ok, true);
assert.equal(res4.data.passed, true);
studentAttempts["admin-4:summary"] = { bestScore: res4.data.score };

// Check that Admin Module 5 unlocks
const unlock5 = getUnlockDecision({ studentAttempts, moduleId: "admin-4", tier });
assert.equal(unlock5.eligibleToUnlock, true);
console.log("✓ Admin Module 5 unlocked!");

// 5. Simulate passing Admin Module 5
console.log("Simulating Admin Module 5 lab completion...");
const res5 = await aiEngine.run("verify-lab", {
  moduleId: "admin-5",
  labId: "admin-5-lab-1",
  studentAnswers: {
    q1: "Student_Email_Required",
    q2: "Student__c",
    q3: "Enrollment_Status_Required",
    q4: "ensures data quality and prevents incorrect data based on business rules",
    q5: "Email, Status"
  }
}, { userId: "founder-student-001", tier });

assert.equal(res5.ok, true);
assert.equal(res5.data.passed, true);
studentAttempts["admin-5:summary"] = { bestScore: res5.data.score };

// Check that Admin Module 6 unlocks
const unlock6 = getUnlockDecision({ studentAttempts, moduleId: "admin-5", tier });
assert.equal(unlock6.eligibleToUnlock, true);
console.log("✓ Admin Module 6 unlocked!");

// 6. Simulate passing Admin Module 6
console.log("Simulating Admin Module 6 lab completion...");
const res6 = await aiEngine.run("verify-lab", {
  moduleId: "admin-6",
  labId: "admin-6-lab-1",
  studentAnswers: {
    q1: "Students by Status",
    q2: "Enrollments by Course",
    q3: "Pending Fee Payments",
    q4: "Student Success CRM Dashboard",
    q5: "bar chart, pie chart, metric"
  }
}, { userId: "founder-student-001", tier });

assert.equal(res6.ok, true);
assert.equal(res6.data.passed, true);
studentAttempts["admin-6:summary"] = { bestScore: res6.data.score };

// Check that Admin Module 7 unlocks
const unlock7 = getUnlockDecision({ studentAttempts, moduleId: "admin-6", tier });
assert.equal(unlock7.eligibleToUnlock, true);
console.log("✓ Admin Module 7 unlocked!");

// 7. Simulate passing Admin Module 7
console.log("Simulating Admin Module 7 lab completion...");
const res7 = await aiEngine.run("verify-lab", {
  moduleId: "admin-7",
  labId: "admin-7-lab-1",
  studentAnswers: {
    q1: "Record-Triggered Flow",
    q2: "Student__c",
    q3: "Student_Registration_Automation",
    q4: "Decision",
    q5: "$Record"
  }
}, { userId: "founder-student-001", tier });

assert.equal(res7.ok, true);
assert.equal(res7.data.passed, true);
assert.equal(res7.data.score, 100);

const passportUpdate = buildSkillPassportUpdate({
  labResult: res7.data,
  moduleId: "admin-7",
  skillId: "salesforce-flow-automation"
});

assert.equal(passportUpdate.moduleId, "admin-7");
assert.equal(passportUpdate.skillId, "salesforce-flow-automation");
assert.equal(passportUpdate.status, "verified");
assert.equal(passportUpdate.score, 100);
console.log("✓ Salesforce Flow Automation skill verified!");

// 8. Verify that Admin Module 8 becomes the next unlock candidate
studentAttempts["admin-7:summary"] = { bestScore: res7.data.score };
const unlock8 = getUnlockDecision({ studentAttempts, moduleId: "admin-7", tier });
assert.equal(unlock8.eligibleToUnlock, true);
console.log("✓ Admin Module 8 is now eligible to unlock (Unlock Candidate)!");

console.log("\nAll Admin Module 7 progression proof assertions PASSED successfully!");
