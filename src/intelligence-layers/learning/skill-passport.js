export function buildSkillPassportUpdate({ labResult, moduleId, skillId }) {
  if (!labResult?.labId) {
    throw new Error("Lab result is required for Skill Passport update.");
  }

  return {
    moduleId,
    skillId,
    labId: labResult.labId,
    status: labResult.passed ? "verified" : "needs_review",
    score: labResult.score,
    feedback: labResult.feedback,
    verifiedAt: labResult.passed ? new Date().toISOString() : null
  };
}
