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
  },
  {
    moduleId: "admin-6",
    labId: "admin-6-lab-1",
    labTitle: "Create Reports and Dashboards for Student Success CRM",
    skillId: "salesforce-reporting-dashboards",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What report did you create to group Students by Status?",
        type: "text",
        expectedKeywords: ["Students by Status", "Student Status"],
        minimumMatches: 1
      },
      {
        id: "q2",
        question: "What report did you create to track Enrollments by Course?",
        type: "text",
        expectedKeywords: ["Enrollments by Course", "Enrollment by Course"],
        minimumMatches: 1
      },
      {
        id: "q3",
        question: "What report did you create to track Pending Fee Payments?",
        type: "text",
        expectedKeywords: ["Pending Fee Payments", "Pending Fees", "Fee Payments"],
        minimumMatches: 1
      },
      {
        id: "q4",
        question: "What dashboard did you create for Student Success CRM?",
        type: "text",
        expectedKeywords: ["Student Success CRM Dashboard", "Student Success Dashboard"],
        minimumMatches: 1
      },
      {
        id: "q5",
        question: "Name any three dashboard components you added.",
        type: "text",
        expectedKeywords: ["chart", "bar chart", "pie chart", "table", "metric", "gauge", "report chart"],
        minimumMatches: 3
      }
    ]
  },
  {
    moduleId: "admin-7",
    labId: "admin-7-lab-1",
    labTitle: "Build Flow Automations for Student Success CRM",
    skillId: "salesforce-flow-automation",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What type of Flow did you create to automate Student registration?",
        type: "text",
        expectedKeywords: ["Record-Triggered", "Record Triggered"],
        minimumMatches: 1
      },
      {
        id: "q2",
        question: "Which object triggers your record-triggered flow?",
        type: "text",
        expectedKeywords: ["Student__c", "Student"],
        minimumMatches: 1
      },
      {
        id: "q3",
        question: "What is the API name of the Flow you created?",
        type: "text",
        expectedKeywords: ["Student_Registration_Automation", "Student_Welcome_Flow", "Student_Welcome"],
        minimumMatches: 1
      },
      {
        id: "q4",
        question: "What element in your flow evaluates conditions to branch logic?",
        type: "text",
        expectedKeywords: ["Decision"],
        minimumMatches: 1
      },
      {
        id: "q5",
        question: "What global variable refers to the record that triggered the flow?",
        type: "text",
        expectedKeywords: ["$Record", "Record"],
        minimumMatches: 1
      }
    ]
  },
  {
    moduleId: "admin-8",
    labId: "admin-8-lab-1",
    labTitle: "Build Intermediate Flow Automation for Student Success CRM",
    skillId: "salesforce-flow-automation-intermediate",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What is the API name of your intermediate flow?",
        type: "text",
        expectedKeywords: ["Student_Status_Update_Automation", "Enrollment_Follow_Up_Flow", "Student_Follow_Up_Flow"],
        minimumMatches: 1
      },
      {
        id: "q2",
        question: "Which object triggers your flow?",
        type: "text",
        expectedKeywords: ["Student__c", "Enrollment__c"],
        minimumMatches: 1
      },
      {
        id: "q3",
        question: "Which Flow element did you use to branch logic?",
        type: "text",
        expectedKeywords: ["Decision"]
      },
      {
        id: "q4",
        question: "Which Flow element did you use to create a follow-up task or record?",
        type: "text",
        expectedKeywords: ["Create Records", "Create Record"]
      },
      {
        id: "q5",
        question: "Why is a fault path important in Salesforce Flow?",
        type: "text",
        expectedKeywords: ["error handling", "failure", "debug", "prevent automation failure", "handle errors"],
        minimumMatches: 1
      }
    ]
  },
  {
    moduleId: "admin-9",
    labId: "admin-9-lab-1",
    labTitle: "Build a Student Graduation Approval Process",
    skillId: "salesforce-approval-processes",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "What is the API name of the Approval Process you created?",
        type: "text",
        expectedKeywords: ["Student_Graduation_Approval", "Graduation_Approval"],
        minimumMatches: 1
      },
      {
        id: "q2",
        question: "What object is the Approval Process built on?",
        type: "text",
        expectedKeywords: ["Student__c"]
      },
      {
        id: "q3",
        question: "What field and value did you set as Entry Criteria?",
        type: "text",
        expectedKeywords: ["Status__c", "Pending Graduation", "Pending"],
        minimumMatches: 1
      },
      {
        id: "q4",
        question: "What Final Approval Action did you configure?",
        type: "text",
        expectedKeywords: ["Field Update", "Status__c", "Graduated", "field update"],
        minimumMatches: 1
      },
      {
        id: "q5",
        question: "What is the key difference between an Approval Process and a Record-Triggered Flow?",
        type: "text",
        expectedKeywords: ["human", "manual", "approve", "decision", "automatic", "automated"],
        minimumMatches: 1
      }
    ]
  },
  {
    moduleId: "admin-10",
    labId: "admin-10-lab-1",
    labTitle: "Bulk Import and Duplicate Management for Student Success CRM",
    skillId: "salesforce-data-management",
    passingScore: 80,
    criteria: [
      {
        id: "q1",
        question: "How many Student records did you import using Data Import Wizard?",
        type: "text",
        expectedKeywords: ["10", "ten", "5", "five", "20", "twenty"],
        minimumMatches: 1
      },
      {
        id: "q2",
        question: "What tool did you use to import the Student records?",
        type: "text",
        expectedKeywords: ["Data Import Wizard", "Import Wizard", "wizard"],
        minimumMatches: 1
      },
      {
        id: "q3",
        question: "What field did you use in your Matching Rule to detect duplicate students?",
        type: "text",
        expectedKeywords: ["Email__c", "Email", "email"],
        minimumMatches: 1
      },
      {
        id: "q4",
        question: "What action did you set in your Duplicate Rule when a match is found?",
        type: "text",
        expectedKeywords: ["Block", "block", "Alert", "Report"],
        minimumMatches: 1
      },
      {
        id: "q5",
        question: "What is the key difference between Data Import Wizard and Data Loader?",
        type: "text",
        expectedKeywords: ["50,000", "50000", "record limit", "millions", "desktop", "browser", "install", "Data Loader"],
        minimumMatches: 1
      }
    ]
  }
];
