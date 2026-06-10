/**
 * prove-admin-module-10.js
 * Proof script: Admin Module 10 — Data Management and Import Tools
 *
 * Run: node prove-admin-module-10.js
 */

import { labCriteria } from "./src/knowledge/academy/lab-criteria.js";
import { moduleProgression } from "./src/knowledge/academy/module-progression.js";

const MODULE_ID = "admin-10";
const LAB_ID = "admin-10-lab-1";

console.log("\n🔍 Admin Module 10 Proof Script — Data Management & Import Tools\n");
console.log("=".repeat(60));

// 1. Verify lab criteria
const lab = labCriteria.find(l => l.moduleId === MODULE_ID && l.labId === LAB_ID);
if (!lab) {
  console.error("❌ FAIL: Lab criteria for admin-10 not found.");
  process.exit(1);
}
console.log(`\n✅ Lab criteria found:`);
console.log(`   Module ID  : ${lab.moduleId}`);
console.log(`   Lab ID     : ${lab.labId}`);
console.log(`   Title      : ${lab.labTitle}`);
console.log(`   Skill ID   : ${lab.skillId}`);
console.log(`   Passing    : ${lab.passingScore}%`);
console.log(`   Questions  : ${lab.criteria.length}`);

// 2. Verify all 5 questions
const expectedIds = ["q1", "q2", "q3", "q4", "q5"];
const foundIds = lab.criteria.map(c => c.id);
if (!expectedIds.every(id => foundIds.includes(id))) {
  console.error(`❌ FAIL: Missing questions. Found: ${foundIds.join(", ")}`);
  process.exit(1);
}
console.log("\n✅ All 5 lab questions verified:");
lab.criteria.forEach(c => console.log(`   [${c.id}] ${c.question}`));

// 3. Verify module progression
const mod = moduleProgression.find(m => m.moduleId === MODULE_ID);
if (!mod) {
  console.error("❌ FAIL: Module progression entry for admin-10 not found.");
  process.exit(1);
}
console.log(`\n✅ Module progression found:`);
console.log(`   Module ID     : ${mod.moduleId}`);
console.log(`   Name          : ${mod.moduleName}`);
console.log(`   Required Tier : ${mod.requiredTier}`);
console.log(`   Next Module   : ${mod.nextModuleId || "null (final module)"}`);
console.log(`   Prerequisites : ${mod.prerequisites.length > 0 ? mod.prerequisites.map(p => p.labId).join(", ") : "None"}`);

// 4. Verify full chain admin-1 → admin-10
console.log(`\n✅ Full Admin Path Chain:`);
const chain = [];
let current = moduleProgression.find(m => m.moduleId === "admin-1");
while (current) {
  chain.push(current.moduleId);
  current = current.nextModuleId ? moduleProgression.find(m => m.moduleId === current.nextModuleId) : null;
}
chain.forEach((id, i) => console.log(`   ${i + 1}. ${id} → ${moduleProgression.find(m => m.moduleId === id).moduleName}`));
if (chain.length < 10) {
  console.error(`❌ FAIL: Chain is only ${chain.length} modules (expected 10+)`);
  process.exit(1);
}
console.log(`\n   Total modules in chain: ${chain.length} ✅`);

// 5. Simulate lab scoring
console.log("\n" + "=".repeat(60));
console.log("📋 Simulated Lab Scoring:");

const simulatedAnswers = {
  q1: "10",
  q2: "Data Import Wizard",
  q3: "Email__c",
  q4: "Block",
  q5: "Data Import Wizard is browser-based and supports up to 50,000 records. Data Loader is a desktop application that can handle millions of records."
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
  console.log(`   [${criterion.id}] ${passed ? "✅" : "❌"} "${answer.slice(0, 50)}..." → ${points}/20`);
});

console.log(`\n   Total Score: ${totalScore}/100`);
console.log(`   Status: ${totalScore >= lab.passingScore ? "✅ PASSED" : "❌ NEEDS IMPROVEMENT"}`);

console.log("\n" + "=".repeat(60));
console.log("🎉 Admin Module 10 proof complete — Full 10-module Admin Foundation verified!\n");
