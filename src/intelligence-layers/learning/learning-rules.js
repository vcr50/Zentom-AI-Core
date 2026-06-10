export function normalizeAnswer(value) {
  return String(value || "")
    .trim()
    .toLowerCase();
}

export function percentageScore(passedCount, total) {
  if (!total) return 0;
  return Math.round((passedCount / total) * 100);
}

export function verifyTextAnswer(answer, criterion) {
  const normalized = normalizeAnswer(answer);
  const expected = criterion.expectedKeywords || criterion.expectedValues || [];
  const matches = expected.filter((keyword) => normalized.includes(normalizeAnswer(keyword)));
  const minimumMatches = criterion.minimumMatches || 1;
  const passed = matches.length >= minimumMatches;

  return {
    id: criterion.id,
    question: criterion.question,
    passed,
    score: passed ? 100 : 0,
    matched: matches,
    hint: passed ? null : criterion.hint || "Review the lab instructions and try again."
  };
}

export function verifyNumberAnswer(answer, criterion) {
  const numericAnswer = Number(answer);
  const expected = Number(criterion.expectedValue);
  const passed = Number.isFinite(numericAnswer) && numericAnswer === expected;

  return {
    id: criterion.id,
    question: criterion.question,
    passed,
    score: passed ? 100 : 0,
    matched: passed ? [expected] : [],
    hint: passed ? null : criterion.hint || "Check the number and try again."
  };
}
