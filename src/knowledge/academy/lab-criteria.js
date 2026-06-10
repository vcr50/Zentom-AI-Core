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
  },
  {
    moduleId: "admin-3",
    labId: "admin-3-lab-1",
    labTitle: "Configure Security for Student Success CRM",
    skillId: "salesforce-security-foundations",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What Permission Set did you create for Student Success CRM users?",
        type: "text",
        expectedKeywords: ["Student Success User", "Student Success CRM User"],
        minimumMatches: 1
      },
      {
        id: "q2",
        question: "Which object did you give access to in the Permission Set?",
        type: "text",
        expectedKeywords: ["Student__c", "Course__c", "Enrollment__c"],
        minimumMatches: 1
      },
      {
        id: "q3",
        question: "Which permission allows a user to create new records?",
        type: "text",
        expectedKeywords: ["Create"]
      },
      {
        id: "q4",
        question: "Why are Permission Sets better than editing Profiles for extra access?",
        type: "text",
        expectedKeywords: ["flexible", "additional access", "user specific", "without changing profile"],
        minimumMatches: 1
      },
      {
        id: "q5",
        question: "Name any two permissions you enabled for Student__c.",
        type: "text",
        expectedKeywords: ["Read", "Create", "Edit", "Delete", "View All", "Modify All"],
        minimumMatches: 2
      }
    ]
  },
  {
    moduleId: "admin-4",
    labId: "admin-4-lab-1",
    labTitle: "Configure Page Layouts and App Experience",
    skillId: "salesforce-app-user-experience",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What is the exact name of the Lightning App you created?",
        type: "text",
        expectedKeywords: ["Student Success CRM"]
      },
      {
        id: "q2",
        question: "What is the API name of the Student tab you created?",
        type: "text",
        expectedKeywords: ["Student__c"]
      },
      {
        id: "q3",
        question: "What is the API name of the Course tab you created?",
        type: "text",
        expectedKeywords: ["Course__c"]
      },
      {
        id: "q4",
        question: "What is the API name of the Enrollment tab you created?",
        type: "text",
        expectedKeywords: ["Enrollment__c"]
      },
      {
        id: "q5",
        question: "Name the customized Student Page Layout you configured.",
        type: "text",
        expectedKeywords: ["Student Layout", "Student Page Layout"],
        minimumMatches: 1
      },
      {
        id: "q6",
        question: "What is the name of the customized List View you created for Students?",
        type: "text",
        expectedKeywords: ["Active Students", "All Active Students"],
        minimumMatches: 1
      }
    ]
  },
  {
    moduleId: "admin-5",
    labId: "admin-5-lab-1",
    labTitle: "Create Validation Rules for Student Success CRM",
    skillId: "salesforce-data-quality-rules",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What validation rule did you create to require Student Email?",
        type: "text",
        expectedKeywords: ["Student_Email_Required", "Email Required"],
        minimumMatches: 1
      },
      {
        id: "q2",
        question: "Which object contains your Student Email validation rule?",
        type: "text",
        expectedKeywords: ["Student__c"]
      },
      {
        id: "q3",
        question: "What validation rule did you create for Enrollment Status?",
        type: "text",
        expectedKeywords: ["Enrollment_Status_Required", "Status Required"],
        minimumMatches: 1
      },
      {
        id: "q4",
        question: "Why are validation rules important in Salesforce?",
        type: "text",
        expectedKeywords: ["data quality", "prevent incorrect data", "required", "business rule"],
        minimumMatches: 1
      },
      {
        id: "q5",
        question: "Name any two fields you protected using validation rules.",
        type: "text",
        expectedKeywords: ["Email", "Phone", "Status", "Enrollment Status", "Course"],
        minimumMatches: 2
      }
    ]
  }
];
