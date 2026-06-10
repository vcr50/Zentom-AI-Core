import { moduleProgression } from "zentom-ai-core";

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

  // Update skills map dynamically
  const skillId = skillPassportUpdate?.skillId || result?.data?.skillId || "salesforce-platform-foundations";
  const skillName = skillId
    .split("-")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");

  passport.skills[skillName] = {
    status: passport.bestScores[labId] >= 80 ? "Verified" : "Needs Improvement",
    score: passport.bestScores[labId],
    source: "Zentom AI Learning Intelligence"
  };

  passport.lastUpdatedAt = new Date().toISOString();

  return passport;
}

export function getUnlockDecision({ userId, moduleId, tier }) {
  const passport = getSkillPassport(userId);

  // Find current module configuration
  const currentConfig = moduleProgression.find(m => m.moduleId === moduleId);
  if (!currentConfig) {
    return {
      moduleId,
      nextModuleId: "unknown",
      eligibleToUnlock: false,
      reason: `Module configuration not found for ${moduleId}.`
    };
  }

  const nextModuleId = currentConfig.nextModuleId;
  if (!nextModuleId) {
    return {
      moduleId,
      nextModuleId: null,
      eligibleToUnlock: false,
      reason: `No subsequent module after ${moduleId}.`
    };
  }

  // Find next module configuration to see its entry requirements
  const nextConfig = moduleProgression.find(m => m.moduleId === nextModuleId);
  if (!nextConfig) {
    return {
      moduleId,
      nextModuleId,
      eligibleToUnlock: false,
      reason: `Configuration not found for next module ${nextModuleId}.`
    };
  }

  // 1. Check prerequisites: user must pass all required labs of the current module
  const prerequisites = currentConfig.prerequisites || [];
  
  for (const prereq of prerequisites) {
    const bestScore = passport.bestScores[prereq.labId] || 0;
    if (bestScore < prereq.minPassingScore) {
      return {
        moduleId,
        nextModuleId,
        eligibleToUnlock: false,
        reason: `Lab score of ${bestScore} is below the passing score of ${prereq.minPassingScore}.`
      };
    }
  }

  // 2. Check next module entry tier eligibility
  if (nextConfig.requiredTier === "founder" && tier !== "founder") {
    // If the next module requires Founder Access and user doesn't have it
    return {
      moduleId,
      nextModuleId,
      eligibleToUnlock: false,
      reason: `Module 2 requires Founder Access.`
    };
  }

  // All prerequisites passed, and tier criteria satisfies!
  const mainPrereq = prerequisites[0] || {};
  const mainLabScore = passport.bestScores[mainPrereq.labId] || 0;

  return {
    moduleId,
    nextModuleId,
    eligibleToUnlock: true,
    reason: `Lab score is ${mainLabScore} and passing score is ${mainPrereq.minPassingScore || 80}.`
  };
}
