import { aiEngine } from "../src/index.js";

const lab = {
  labId: "sample-lab-1",
  labTitle: "Create and Review Sample Records",
  passingScore: 80,
  criteria: [
    {
      id: "q1",
      question: "What is the exact account name you created?",
      type: "text",
      expectedKeywords: ["Sample Training Account"],
      hint: "Open the account record you created and confirm its name."
    },
    {
      id: "q2",
      question: "What is the exact contact last name you created?",
      type: "text",
      expectedKeywords: ["Sample Learner"],
      hint: "Open the contact record you created and confirm its name."
    },
    {
      id: "q3",
      question: "Which account is your contact linked to?",
      type: "text",
      expectedKeywords: ["Sample Training Account"],
      hint: "Open the contact record and check the linked account field."
    },
    {
      id: "q4",
      question: "What is the name of the list view you created?",
      type: "text",
      expectedKeywords: ["My Active Accounts"],
      hint: "Open the list view and confirm its name."
    },
    {
      id: "q5",
      question: "Name any two columns visible in your list view.",
      type: "text",
      expectedKeywords: ["Account Name", "Phone", "Industry", "Owner"],
      minimumMatches: 2,
      hint: "Open the list view and check the visible columns."
    }
  ]
};

const studentAnswers = {
  q1: "Sample Training Account",
  q2: "Sample Learner",
  q3: "Sample Training Account",
  q4: "My Active Accounts",
  q5: "Account Name, Phone"
};

const result = await aiEngine.run(
  "verify-lab",
  { lab, studentAnswers },
  {
    userId: "demo-student",
    tier: "free"
  }
);

console.log(JSON.stringify(result, null, 2));
