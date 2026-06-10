import assert from "node:assert/strict";
import { evaluateCertificateEligibility } from "./src/index.js";

console.log("Starting Certificate Eligibility Engine proof...");

// Scenario 1: Free tier student with all 8 labs passed
console.log("Scenario 1: Free tier student with all 8 labs passed at 100%...");
const studentAttempts1 = {};
const skillPassport1 = {};
for (let i = 1; i <= 8; i++) {
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
  "salesforce-flow-automation-intermediate"
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
assert.equal(res1.verifiedModules, 8);
assert.equal(res1.missingRequirements.length, 1);
assert.ok(res1.missingRequirements[0].includes("Upgrade to founder tier required"));
console.log("✓ Correctly blocked Free tier student (requires Founder tier)");

// Scenario 2: Founder student with only 7 labs completed
console.log("Scenario 2: Founder student with 7 out of 8 labs completed...");
const studentAttempts2 = { ...studentAttempts1 };
const skillPassport2 = { ...skillPassport1 };
delete studentAttempts2["admin-8:summary"];
delete skillPassport2["salesforce-flow-automation-intermediate"];

const res2 = evaluateCertificateEligibility({
  studentAttempts: studentAttempts2,
  skillPassport: skillPassport2,
  tier: "founder"
});

assert.equal(res2.eligible, false);
assert.equal(res2.verifiedModules, 7);
assert.ok(res2.missingRequirements.some(req => req.includes("Module 8") && req.includes("Salesforce Flow Automation Intermediate")));
console.log("✓ Correctly blocked student with incomplete labs");

// Scenario 3: Founder student with all 8 labs completed
console.log("Scenario 3: Founder student with all 8 labs completed at 100%...");
const res3 = evaluateCertificateEligibility({
  studentAttempts: studentAttempts1,
  skillPassport: skillPassport1,
  tier: "founder"
});

assert.equal(res3.eligible, true);
assert.equal(res3.verifiedModules, 8);
assert.equal(res3.missingRequirements.length, 0);
assert.equal(res3.verifiedSkills.length, 8);
assert.equal(res3.verifiedSkills[7], "Salesforce Flow Automation Intermediate");
console.log("✓ Correctly authorized Founder student with all 8 completed labs");

console.log("\nAll Certificate Eligibility Engine proof assertions PASSED successfully!");
