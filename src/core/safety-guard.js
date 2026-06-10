const blockedTaskNames = new Set(["execute-production-action"]);

export function applySafetyGuard({ task } = {}) {
  if (blockedTaskNames.has(task)) {
    return {
      allowed: false,
      reason: "This task requires an explicit human approval workflow."
    };
  }

  return {
    allowed: true,
    reason: null
  };
}
