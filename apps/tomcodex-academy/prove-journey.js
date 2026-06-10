const API_BASE = "http://localhost:3001";

const basePayload = {
  task: "verify-lab",
  userId: "student-journey-002",
  tier: "free",
  params: {
    moduleId: "admin-1",
    labId: "admin-1-lab-1"
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

async function proveJourney() {
  console.log("Starting TomCodeX Academy student journey proof (Criteria from Knowledge Layer)...");

  // ==========================================
  // SCENARIO 1: Failed Attempt
  // ==========================================
  console.log("\n--- Scenario 1: Failed Attempt (Incorrect answers) ---");
  const failedPayload = {
    ...basePayload,
    tier: "founder",
    params: {
      ...basePayload.params,
      studentAnswers: {
        q1: "Wrong Account Name",
        q2: "Wrong Student",
        q3: "Wrong Account Name",
        q4: "Wrong Account Name",
        q5: "Wrong Account Name"
      }
    }
  };

  const res1 = await sendRequest(failedPayload);
  console.log(`Passed: ${res1.data.passed} | Score: ${res1.data.score}%`);
  console.log("Unlock Decision:", JSON.stringify(res1.unlockDecision, null, 2));
  console.log("Passport Summary:", JSON.stringify(res1.passportSummary, null, 2));

  if (res1.data.passed !== false || res1.unlockDecision.eligibleToUnlock !== false) {
    throw new Error("Scenario 1 failed: Expected lab to fail and unlock to be denied.");
  }
  if (res1.passportSummary.failedAttemptsCount !== 1 || res1.passportSummary.attemptsCount !== 1) {
    throw new Error("Scenario 1 failed: Incorrect attempt counters.");
  }

  // ==========================================
  // SCENARIO 2: Passing Attempt (Free Tier)
  // ==========================================
  console.log("\n--- Scenario 2: Passing Attempt (Free Tier) ---");
  const freePassingPayload = {
    ...basePayload,
    tier: "free",
    params: {
      ...basePayload.params,
      studentAnswers: {
        q1: "TomCodeX Training Institute",
        q2: "Demo Student",
        q3: "TomCodeX Training Institute",
        q4: "My Active Accounts",
        q5: "Account Name, Phone"
      }
    }
  };

  const res2 = await sendRequest(freePassingPayload);
  console.log(`Passed: ${res2.data.passed} | Score: ${res2.data.score}%`);
  console.log("Unlock Decision:", JSON.stringify(res2.unlockDecision, null, 2));
  console.log("Passport Summary:", JSON.stringify(res2.passportSummary, null, 2));

  if (res2.data.passed !== true || res2.unlockDecision.eligibleToUnlock !== false) {
    throw new Error("Scenario 2 failed: Expected lab to pass but unlock to be denied for Free tier.");
  }
  if (res2.unlockDecision.reason !== "Module 2 requires Founder Access.") {
    throw new Error("Scenario 2 failed: Expected Free tier lockout reason.");
  }
  if (res2.passportSummary.attemptsCount !== 2 || res2.passportSummary.failedAttemptsCount !== 1) {
    throw new Error("Scenario 2 failed: Incorrect attempt counters.");
  }
  if (!res2.passportSummary.verifiedAt) {
    throw new Error("Scenario 2 failed: verifiedAt should be set since the lab passed.");
  }

  // ==========================================
  // SCENARIO 3: Passing Attempt (Founder Tier)
  // ==========================================
  console.log("\n--- Scenario 3: Passing Attempt (Founder Tier) ---");
  const founderPassingPayload = {
    ...basePayload,
    tier: "founder",
    params: {
      ...basePayload.params,
      studentAnswers: {
        q1: "TomCodeX Training Institute",
        q2: "Demo Student",
        q3: "TomCodeX Training Institute",
        q4: "My Active Accounts",
        q5: "Account Name, Phone"
      }
    }
  };

  const res3 = await sendRequest(founderPassingPayload);
  console.log(`Passed: ${res3.data.passed} | Score: ${res3.data.score}%`);
  console.log("Unlock Decision:", JSON.stringify(res3.unlockDecision, null, 2));
  console.log("Passport Summary:", JSON.stringify(res3.passportSummary, null, 2));

  if (res3.data.passed !== true || res3.unlockDecision.eligibleToUnlock !== true) {
    throw new Error("Scenario 3 failed: Expected lab to pass and unlock to be granted for Founder tier.");
  }
  if (res3.passportSummary.attemptsCount !== 3) {
    throw new Error("Scenario 3 failed: Incorrect attempts count.");
  }

  // Double check the persistent passport state
  const finalPassportRes = await getPassport(basePayload.userId);
  console.log("\nFinal Passport State from DB:");
  console.log(JSON.stringify(finalPassportRes.passport, null, 2));

  console.log("\nJourney proved successfully with criteria from knowledge layer!");
}

proveJourney().catch((error) => {
  console.error("Journey proof failed:", error);
  process.exit(1);
});
