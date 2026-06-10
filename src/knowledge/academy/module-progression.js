export const moduleProgression = [
  {
    moduleId: "admin-1",
    nextModuleId: "admin-2",
    requiredLabs: ["admin-1-lab-1"],
    minPassingScore: 80,
    requiredTier: "free"
  },
  {
    moduleId: "admin-2",
    nextModuleId: "admin-3",
    requiredLabs: ["admin-2-lab-1"],
    minPassingScore: 80,
    requiredTier: "founder"
  }
];
