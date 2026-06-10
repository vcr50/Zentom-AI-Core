import { verifyAcademyLab } from "../intelligence-layers/learning/lab-verifier.js";

export async function routeTask(task, params) {
  switch (task) {
    case "verify-lab":
      return {
        mode: "rule-based",
        model: "zentom-rules-v1",
        data: verifyAcademyLab(params)
      };

    case "train":
      return {
        mode: "mock",
        model: "zentom-mock-v1",
        data: {
          message: "Training assistance mode is ready. Provider integration can be added next."
        }
      };

    case "chat":
      return {
        mode: "mock",
        model: "zentom-mock-v1",
        data: {
          message: "Chat mode is ready. Provider integration can be added next."
        }
      };

    default:
      throw new Error(`Unsupported AI task: ${task}`);
  }
}
