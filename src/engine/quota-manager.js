const memoryUsage = new Map();

function getQuota(tier) {
  const quotas = {
    free: Number(process.env.FREE_DAILY_AI_LIMIT || 10),
    founder: Number(process.env.FOUNDER_DAILY_AI_LIMIT || 100),
    personal_key: Infinity
  };

  return quotas[tier] ?? quotas.free;
}

function getTodayKey(userId) {
  const today = new Date().toISOString().slice(0, 10);
  return `${userId}:${today}`;
}

export function checkQuota({ userId = "anonymous", tier = "free", hasPersonalKey = false } = {}) {
  if (hasPersonalKey) {
    return {
      allowed: true,
      limit: Infinity,
      used: 0,
      remaining: Infinity
    };
  }

  const limit = getQuota(tier);
  const key = getTodayKey(userId);
  const used = memoryUsage.get(key) || 0;

  return {
    allowed: used < limit,
    limit,
    used,
    remaining: Math.max(limit - used, 0)
  };
}

export function consumeQuota({ userId = "anonymous", tier = "free", hasPersonalKey = false } = {}) {
  if (hasPersonalKey) return;

  const key = getTodayKey(userId);
  const used = memoryUsage.get(key) || 0;
  memoryUsage.set(key, used + 1);
}

export function resetQuotaForTests() {
  memoryUsage.clear();
}
