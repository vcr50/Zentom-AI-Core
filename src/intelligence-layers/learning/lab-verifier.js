import { percentageScore, verifyNumberAnswer, verifyTextAnswer } from "./learning-rules.js";

export function verifyAcademyLab({ lab, studentAnswers }) {
  if (!lab?.criteria?.length) {
    throw new Error("Lab criteria are required.");
  }

  const results = lab.criteria.map((criterion) => {
    const answer = studentAnswers?.[criterion.id];

    if (criterion.type === "number") {
      return verifyNumberAnswer(answer, criterion);
    }

    return verifyTextAnswer(answer, criterion);
  });

  const passedCount = results.filter((item) => item.passed).length;
  const total = results.length;
  const score = percentageScore(passedCount, total);
  const passed = score >= (lab.passingScore || 80);

  return {
    labId: lab.labId,
    labTitle: lab.labTitle,
    passed,
    score,
    passedCount,
    total,
    criteriaResults: results,
    feedback: passed
      ? "Lab verified. Progress can be updated."
      : "Lab not fully verified. Review the hints and try again."
  };
}
