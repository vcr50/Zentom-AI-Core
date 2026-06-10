import { createAcademyAiHandler } from "zentom-ai-core";

export function registerAcademyAiRoute(app, { skillPassportService }) {
  app.post("/api/ai/run", createAcademyAiHandler({
    async updateSkillPassport({ userId, update }) {
      await skillPassportService.updateLabProgress(userId, update);
    }
  }));
}

/*
Expected Check My Work request body:

{
  "task": "verify-lab",
  "moduleId": "admin-module-1",
  "skillId": "admin-hands-on-basics",
  "params": {
    "lab": {
      "labId": "admin-module-1-lab",
      "labTitle": "Admin Module 1 Hands-on Lab",
      "passingScore": 80,
      "criteria": []
    },
    "studentAnswers": {}
  }
}
*/
  });
}
