const API_BASE = "http://localhost:3001";

const userId = "student-journey-module2";

const admin1Payload = {
  task: "verify-lab",
  userId,
  tier: "founder",
  params: {
    moduleId: "admin-1",
    labId: "admin-1-lab-1",
    studentAnswers: {
      q1: "TomCodeX Training Institute",
      q2: "Demo Student",
      q3: "TomCodeX Training Institute",
      q4: "My Active Accounts",
      q5: "Account Name, Phone"
    }
  }
};

const admin2Payload = {
  task: "verify-lab",
  userId,
  tier: "founder",
  params: {
    moduleId: "admin-2",
    labId: "admin-2-lab-1",
    studentAnswers: {
      q1: "Student__c",
      q2: "Course__c",
      q3: "Enrollment__c",
      q4: "Enrollment__c",
      q5: "Email, Phone"
    }
  }
};

async function sendRequest(payload) {
  const response = await fetch(`${API_BASE}/api/academy/verify-lab`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return response.json();
}

async function getPassport(userId) {
  const response = await fetch(`${API_BASE}/api/academy/passport/${userId}`);
  return response.json();
}

async function proveModule2Journey() {
  console.log("Starting TomCodeX Academy Admin Module 2 progression proof...");

  // ==========================================
  // STEP 1: Founder user passes Admin Module 1
  // ==========================================
  console.log("\n--- Step 1: Submitting Admin Module 1 Lab ---");
  const res1 = await sendRequest(admin1Payload);
  console.log(`Module 1 passed: ${res1.data.passed} | Score: ${res1.data.score}%`);
  console.log("Unlock Decision:", JSON.stringify(res1.unlockDecision, null, 2));

  if (res1.data.passed !== true || res1.unlockDecision.eligibleToUnlock !== true || res1.unlockDecision.nextModuleId !== "admin-2") {
    throw new Error("Step 1 failed: Expected Admin Module 1 to pass and unlock Admin Module 2.");
  }

  // ==========================================
  // STEP 2: Founder user submits Admin Module 2 Lab
  // ==========================================
  console.log("\n--- Step 2: Submitting Admin Module 2 Lab ---");
  const res2 = await sendRequest(admin2Payload);
  console.log(`Module 2 passed: ${res2.data.passed} | Score: ${res2.data.score}%`);
  console.log("Unlock Decision:", JSON.stringify(res2.unlockDecision, null, 2));
  console.log("Passport Summary:", JSON.stringify(res2.passportSummary, null, 2));

  if (res2.data.passed !== true || res2.unlockDecision.eligibleToUnlock !== true || res2.unlockDecision.nextModuleId !== "admin-3") {
    throw new Error("Step 2 failed: Expected Admin Module 2 to pass and unlock Admin Module 3.");
  }

  // ==========================================
  // STEP 3: Verify Skill Passport updates
  // ==========================================
  console.log("\n--- Step 3: Fetching Final Skill Passport State ---");
  const finalPassportRes = await getPassport(userId);
  console.log("Final Passport State from DB:");
  console.log(JSON.stringify(finalPassportRes.passport, null, 2));

  const passport = finalPassportRes.passport;
  if (!passport.skills["Salesforce Platform Foundations"] || passport.skills["Salesforce Platform Foundations"].status !== "Verified") {
    throw new Error("Step 3 failed: Salesforce Platform Foundations skill was not verified.");
  }
  if (!passport.skills["Salesforce Object Modeling"] || passport.skills["Salesforce Object Modeling"].status !== "Verified") {
    throw new Error("Step 3 failed: Salesforce Object Modeling skill was not verified.");
  }
  if (passport.completedLabs.length !== 2) {
    throw new Error("Step 3 failed: Completed labs count should be exactly 2.");
  }

  console.log("\nAdmin Module 2 and Multi-Module progression proved successfully!");
}

proveModule2Journey().catch((error) => {
  console.error("Progression proof failed:", error);
  process.exit(1);
});
