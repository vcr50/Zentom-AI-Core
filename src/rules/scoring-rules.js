export function percentageScore(passedCount, total) {
  if (!total) return 0;
  return Math.round((passedCount / total) * 100);
}
