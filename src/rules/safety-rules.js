export function requiresHumanReview(action = {}) {
  return Boolean(action.requiresApproval || action.risk === "high");
}
