import { aiEngine, buildSkillPassportUpdate } from "../src/index.js";

const req = {
  session: {
    user: {
      id: "demo-learner",
      tier: "free"
    }
  },
  body: {
    task: "verify-lab",
    params: {
      lab: {
        labId: "admin-module-1-lab",
        labTitle: "Admin Module 1 Hands-on Lab",
        passingScore: 80,
        criteria: [
          {
            id: "q1",
            question: "What account name did you create?",
            type: "text",
            expectedKeywords: ["Sample Training Account"]
          },
          {
            id: "q2",
            question: "How many sample records did you create?",
            type: "number",
            expectedValue: 2
          }
        ]
      },
      studentAnswers: {
        q1: "Sample Training Account",
        q2: 2
      }
    }
  }
};

const aiResult = await aiEngine.run(req.body.task, req.body.params, {
  userId: req.session?.user?.id,
  tier: req.session?.user?.tier || "free"
});

const skillPassportUpdate = aiResult.ok
  ? buildSkillPassportUpdate({
      labResult: aiResult.data,
      moduleId: "admin-module-1",
      skillId: "admin-hands-on-basics"
    })
  : null;

console.log(
  JSON.stringify(
    {
      flow: [
        "Admin Module 1",
        "Hands-on Lab",
        "Check My Work",
        "Zentom AI Learning Intelligence",
        "Score + feedback",
        "Skill Passport update"
      ],
      aiResult,
      skillPassportUpdate
    },
    null,
    2
  )
);
