const logs = [];

export function logUsage(event) {
  const record = {
    ...event,
    timestamp: new Date().toISOString()
  };

  logs.push(record);

  if (process.env.NODE_ENV !== "test") {
    console.log("[AI Usage]", record);
  }

  return record;
}

export function getUsageLogs() {
  return [...logs];
}

export function resetUsageLogsForTests() {
  logs.length = 0;
}
