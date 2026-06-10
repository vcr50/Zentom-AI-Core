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
  },
  {
    moduleId: "admin-2",
    labId: "admin-2-lab-1",
    labTitle: "Create Student Success CRM Core Objects",
    skillId: "salesforce-object-modeling",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What is the API name of the Student object you created?",
        type: "text",
        expectedKeywords: ["Student__c"]
      },
      {
        id: "q2",
        question: "What is the API name of the Course object you created?",
        type: "text",
        expectedKeywords: ["Course__c"]
      },
      {
        id: "q3",
        question: "What is the API name of the Enrollment object you created?",
        type: "text",
        expectedKeywords: ["Enrollment__c"]
      },
      {
        id: "q4",
        question: "Which object connects Student and Course?",
        type: "text",
        expectedKeywords: ["Enrollment__c", "Enrollment"],
        minimumMatches: 1
      },
      {
        id: "q5",
        question: "Name any two fields you created on Student__c.",
        type: "text",
        expectedKeywords: ["Email", "Phone", "Status", "Student ID", "Date of Birth"],
        minimumMatches: 2
      }
    ]
  }
];
