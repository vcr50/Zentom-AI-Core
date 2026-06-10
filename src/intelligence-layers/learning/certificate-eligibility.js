import { certificateRules } from "../../knowledge/academy/certificate-rules.js";

export function evaluateCertificateEligibility({ studentAttempts = {}, skillPassport = {}, tier = "free" }) {
  const missingRequirements = [];
  const verifiedSkills = [];

  // 1. Check Founder Tier
  if (tier !== certificateRules.requiredTier) {
    missingRequirements.push(`Upgrade to ${certificateRules.requiredTier} tier required.`);
  }

  // 2. Check each required skill / module
  let verifiedModules = 0;
  for (let i = 1; i <= certificateRules.requiredModulesCount; i++) {
    const moduleId = `admin-${i}`;
    const summaryKey = `${moduleId}:summary`;
    const legacySummaryKey = `admin-module-${i}:summary`;
    const bestScore = studentAttempts[summaryKey]?.bestScore || studentAttempts[legacySummaryKey]?.bestScore || 0;

    const skillConfig = certificateRules.requiredSkills[i - 1];
    const passportSkill = skillPassport[skillConfig.id];
    const isSkillVerified = passportSkill?.status === "Verified" || passportSkill?.status === "verified";
    const finalScore = passportSkill?.score || bestScore || 0;

    if (finalScore >= certificateRules.minimumScore && isSkillVerified) {
      verifiedModules++;
      verifiedSkills.push(skillConfig.name);
    } else {
      missingRequirements.push(`Complete Module ${i} (${skillConfig.name}) lab with a score of at least ${certificateRules.minimumScore}%.`);
    }
  }

  const eligible = missingRequirements.length === 0;

  return {
    eligible,
    courseId: certificateRules.courseId,
    certificateName: certificateRules.certificateName,
    verifiedModules,
    requiredModules: certificateRules.requiredModulesCount,
    minimumScore: certificateRules.minimumScore,
    missingRequirements,
    verifiedSkills
  };
}
