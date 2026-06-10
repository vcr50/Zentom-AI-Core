/**
 * prove-admin-module-9.js
 * Proof script: Admin Module 9 — Approval Processes and Advanced Automation
 *
 * Run: node prove-admin-module-9.js
 */

import { labCriteria } from "./src/knowledge/academy/lab-criteria.js";
import { moduleProgression } from "./src/knowledge/academy/module-progression.js";

const MODULE_ID = "admin-9";
const LAB_ID = "admin-9-lab-1";

console.log("\n🔍 Admin Module 9 Proof Script — Approval Processes\n");
console.log("=".repeat(55));

// 1. Verify lab criteria exists
const lab = labCriteria.find(l => l.moduleId === MODULE_ID && l.labId === LAB_ID);
if (!lab) {
  console.error("❌ FAIL: Lab criteria for admin-9 not found.");
  process.exit(1);
}

console.log(`\n✅ Lab criteria found:`);
console.log(`   Module ID  : ${lab.moduleId}`);
console.log(`   Lab ID     : ${lab.labId}`);
console.log(`   Title      : ${lab.labTitle}`);
console.log(`   Skill ID   : ${lab.skillId}`);
console.log(`   Passing    : ${lab.passingScore}%`);
console.log(`   Questions  : ${lab.criteria.length}`);

// 2. Verify all 5 questions present
const expectedIds = ["q1", "q2", "q3", "q4", "q5"];
const foundIds = lab.criteria.map(c => c.id);
const allPresent = expectedIds.every(id => foundIds.includes(id));
if (!allPresent) {
  console.error(`❌ FAIL: Missing questions. Found: ${foundIds.join(", ")}`);
  process.exit(1);
}
console.log("\n✅ All 5 lab questions verified:");
lab.criteria.forEach(c => console.log(`   [${c.id}] ${c.question}`));

// 3. Verify module progression
const mod9 = moduleProgression.find(m => m.moduleId === MODULE_ID);
if (!mod9) {
  console.error("❌ FAIL: Module progression entry for admin-9 not found.");
  process.exit(1);
}
console.log(`\n✅ Module progression found:`);
console.log(`   Module ID     : ${mod9.moduleId}`);
console.log(`   Name          : ${mod9.moduleName}`);
console.log(`   Required Tier : ${mod9.requiredTier}`);
console.log(`   Next Module   : ${mod9.nextModuleId}`);
console.log(`   Prerequisites : ${mod9.prerequisites.length > 0 ? mod9.prerequisites.map(p => p.labId).join(", ") : "None (stub)"}`);

// 4. Simulate lab scoring
console.log("\n" + "=".repeat(55));
console.log("📋 Simulated Lab Scoring:");

const simulatedAnswers = {
  q1: "Student_Graduation_Approval",
  q2: "Student__c",
  q3: "Status__c equals Pending Graduation",
  q4: "Field Update Status__c to Graduated",
  q5: "Approval Process requires a human to approve or reject, while a Record-Triggered Flow runs automatically."
};

let totalScore = 0;
lab.criteria.forEach(criterion => {
  const answer = simulatedAnswers[criterion.id] || "";
  const keywords = criterion.expectedKeywords || [];
  const minMatches = criterion.minimumMatches || keywords.length;
  const matches = keywords.filter(kw => answer.toLowerCase().includes(kw.toLowerCase())).length;
  const passed = matches >= minMatches;
  const points = passed ? 20 : 0;
  totalScore += points;
  console.log(`   [${criterion.id}] ${passed ? "✅" : "❌"} "${answer.slice(0, 45)}..." → ${points}/20`);
});

console.log(`\n   Total Score: ${totalScore}/100`);
console.log(`   Status: ${totalScore >= lab.passingScore ? "✅ PASSED" : "❌ NEEDS IMPROVEMENT"}`);

console.log("\n" + "=".repeat(55));
console.log("🎉 Admin Module 9 proof complete.\n");
