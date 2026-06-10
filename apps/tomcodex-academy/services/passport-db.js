const passports = new Map();

export function getSkillPassport(userId) {
  if (!passports.has(userId)) {
    passports.set(userId, {
      userId,
      completedLabs: [],
      attempts: [],
      skills: {},
      bestScores: {},
      verifiedAt: {},
      failedAttemptsCount: {},
      lastUpdatedAt: null
    });
  }

  return passports.get(userId);
}

export function updateSkillPassport({ userId, skillPassportUpdate, result }) {
  const passport = getSkillPassport(userId);

  const labId = skillPassportUpdate?.labId || result?.data?.labId;
  const score = skillPassportUpdate?.score || result?.data?.score || 0;
  const passed = skillPassportUpdate?.passed || result?.data?.passed || false;

  // Track all attempts
  if (!passport.attempts) {
    passport.attempts = [];
  }
  passport.attempts.push({
    labId,
    score,
    passed,
    completedAt: new Date().toISOString()
  });

  if (passed) {
    // Preserve completed lab
    const alreadyCompleted = passport.completedLabs.some(l => l.labId === labId);
    if (!alreadyCompleted) {
      passport.completedLabs.push({
        labId,
        score,
        passed,
        completedAt: new Date().toISOString()
      });
    }

    // Track verifiedAt (only set once on first verification)
    if (!passport.verifiedAt) {
      passport.verifiedAt = {};
    }
    if (!passport.verifiedAt[labId]) {
      passport.verifiedAt[labId] = new Date().toISOString();
    }
  } else {
    // Track failed attempts
    if (!passport.failedAttemptsCount) {
      passport.failedAttemptsCount = {};
    }
    passport.failedAttemptsCount[labId] = (passport.failedAttemptsCount[labId] || 0) + 1;
  }

  // Preserve best score
  passport.bestScores[labId] = Math.max(passport.bestScores[labId] || 0, score);

  // Update skills map
  passport.skills["Salesforce Platform Foundations"] = {
    status: passport.bestScores[labId] >= 80 ? "Verified" : "Needs Improvement",
    score: passport.bestScores[labId],
    source: "Zentom AI Learning Intelligence"
  };

  passport.lastUpdatedAt = new Date().toISOString();

  return passport;
}

export function getUnlockDecision({ userId, moduleId, nextModuleId, tier, labId, passingScore }) {
  const passport = getSkillPassport(userId);
  const bestScore = passport.bestScores[labId] || 0;
  const passed = bestScore >= passingScore;

  if (tier === "free") {
    return {
      moduleId,
      nextModuleId,
      eligibleToUnlock: false,
      reason: `${nextModuleId === "admin-2" ? "Module 2" : nextModuleId} requires Founder Access.`
    };
  }

  if (passed) {
    return {
      moduleId,
      nextModuleId,
      eligibleToUnlock: true,
      reason: `Lab score is ${bestScore} and passing score is ${passingScore}.`
    };
  }

  return {
    moduleId,
    nextModuleId,
    eligibleToUnlock: false,
    reason: `Lab score of ${bestScore} is below the passing score of ${passingScore}.`
  };
}
