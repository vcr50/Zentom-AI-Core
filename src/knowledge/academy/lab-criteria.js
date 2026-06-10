export const labCriteria = [
  {
    moduleId: "admin-1",
    labId: "admin-1-lab-1",
    labTitle: "Explore Salesforce and Create Basic Records",
    skillId: "salesforce-platform-foundations",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What is the exact Account Name you created?",
        type: "text",
        expectedKeywords: ["TomCodeX Training Institute"]
      },
      {
        id: "q2",
        question: "What is the exact Contact Last Name you created?",
        type: "text",
        expectedKeywords: ["Demo Student"]
      },
      {
        id: "q3",
        question: "Which Account is your Contact linked to?",
        type: "text",
        expectedKeywords: ["TomCodeX Training Institute"]
      },
      {
        id: "q4",
        question: "What is the name of the Account list view you created?",
        type: "text",
        expectedKeywords: ["My Active Accounts"]
      },
      {
        id: "q5",
        question: "Name any two columns visible in your Account list view.",
        type: "text",
        expectedKeywords: ["Account Name", "Phone", "Industry", "Owner"],
        minimumMatches: 2
      }
    ]
  }
];
