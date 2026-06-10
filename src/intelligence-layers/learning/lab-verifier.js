import { percentageScore, verifyNumberAnswer, verifyTextAnswer } from "./learning-rules.js";
import { labCriteria } from "../../knowledge/academy/lab-criteria.js";

function findLabCriteria({ moduleId, labId }) {
  if (!labId) return null;
  return labCriteria.find(
    (item) =>
      item.labId === labId &&
      (!moduleId || item.moduleId === moduleId)
  );
}

export function verifyAcademyLab({ lab, studentAnswers, moduleId, labId }) {
  const officialLab =
    findLabCriteria({ moduleId, labId }) ||
    findLabCriteria({ labId: lab?.labId }) ||
    lab;

  if (!officialLab?.criteria?.length) {
    throw new Error(`Lab criteria not found for labId: ${labId || lab?.labId}`);
  }

  const results = officialLab.criteria.map((criterion) => {
    const answer = studentAnswers?.[criterion.id];

    if (criterion.type === "number") {
      return verifyNumberAnswer(answer, criterion);
    }

    return verifyTextAnswer(answer, criterion);
  });

  const passedCount = results.filter((item) => item.passed).length;
  const total = results.length;
  const score = percentageScore(passedCount, total);
  const passed = score >= (officialLab.passingScore || 80);

  return {
    labId: officialLab.labId,
    labTitle: officialLab.labTitle,
    moduleId: officialLab.moduleId,
    skillId: officialLab.skillId,
    passingScore: officialLab.passingScore || 80,
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
