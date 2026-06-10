import assert from "node:assert/strict";
import { evaluateCertificateEligibility } from "./src/index.js";

console.log("Starting Certificate Eligibility Engine proof...");

// Scenario 1: Free tier student with all 10 labs passed
console.log("Scenario 1: Free tier student with all 10 labs passed at 100%...");
const studentAttempts1 = {};
const skillPassport1 = {};
for (let i = 1; i <= 10; i++) {
  studentAttempts1[`admin-${i}:summary`] = { bestScore: 100 };
}
const skillsList = [
  "salesforce-platform-foundations",
  "salesforce-object-modeling",
  "salesforce-security-foundations",
  "salesforce-app-user-experience",
  "salesforce-data-quality-rules",
  "salesforce-reporting-dashboards",
  "salesforce-flow-automation",
  "salesforce-flow-automation-intermediate",
  "salesforce-approval-processes",
  "salesforce-data-management"
];
skillsList.forEach(id => {
  skillPassport1[id] = { status: "Verified", score: 100 };
});

const res1 = evaluateCertificateEligibility({
  studentAttempts: studentAttempts1,
  skillPassport: skillPassport1,
  tier: "free"
});

assert.equal(res1.eligible, false);
assert.equal(res1.verifiedModules, 10);
assert.equal(res1.missingRequirements.length, 1);
assert.ok(res1.missingRequirements[0].includes("Upgrade to founder tier required"));
console.log("✓ Correctly blocked Free tier student (requires Founder tier)");

// Scenario 2: Founder student with only 9 labs completed
console.log("Scenario 2: Founder student with 9 out of 10 labs completed...");
const studentAttempts2 = { ...studentAttempts1 };
const skillPassport2 = { ...skillPassport1 };
delete studentAttempts2["admin-10:summary"];
delete skillPassport2["salesforce-data-management"];

const res2 = evaluateCertificateEligibility({
  studentAttempts: studentAttempts2,
  skillPassport: skillPassport2,
  tier: "founder"
});

assert.equal(res2.eligible, false);
assert.equal(res2.verifiedModules, 9);
assert.ok(res2.missingRequirements.some(req => req.includes("Module 10") && req.includes("Salesforce Data Management")));
console.log("✓ Correctly blocked student with incomplete labs");

// Scenario 3: Founder student with all 10 labs completed
console.log("Scenario 3: Founder student with all 10 labs completed at 100%...");
const res3 = evaluateCertificateEligibility({
  studentAttempts: studentAttempts1,
  skillPassport: skillPassport1,
  tier: "founder"
});

assert.equal(res3.eligible, true);
assert.equal(res3.verifiedModules, 10);
assert.equal(res3.missingRequirements.length, 0);
assert.equal(res3.verifiedSkills.length, 10);
assert.equal(res3.verifiedSkills[9], "Salesforce Data Management");
console.log("✓ Correctly authorized Founder student with all 10 completed labs");

console.log("\nAll Certificate Eligibility Engine proof assertions PASSED successfully!");
