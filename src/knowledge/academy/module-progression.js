export const moduleProgression = [
  {
    moduleId: "admin-1",
    moduleName: "Salesforce Platform Foundations",
    requiredTier: "free",
    prerequisites: [
      {
        labId: "admin-1-lab-1",
        minPassingScore: 80
      }
    ],
    nextModuleId: "admin-2"
  },
  {
    moduleId: "admin-2",
    moduleName: "Student Success CRM Object Model",
    requiredTier: "founder",
    prerequisites: [
      {
        labId: "admin-2-lab-1",
        minPassingScore: 80
      }
    ],
    nextModuleId: "admin-3"
  },
  {
    moduleId: "admin-3",
    moduleName: "Security and Access Control",
    requiredTier: "founder",
    prerequisites: [
      {
        labId: "admin-3-lab-1",
        minPassingScore: 80
      }
    ],
    nextModuleId: "admin-4"
  },
  {
    moduleId: "admin-4",
    moduleName: "Page Layouts, Lightning App, and User Experience",
    requiredTier: "founder",
    prerequisites: [],
    nextModuleId: null
  }
];
