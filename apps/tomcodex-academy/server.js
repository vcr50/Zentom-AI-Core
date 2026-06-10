import express from "express";
import { aiEngine, buildSkillPassportUpdate } from "zentom-ai-core";
import { updateSkillPassport, getSkillPassport, getUnlockDecision } from "./services/passport-db.js";

const app = express();
app.use(express.json({ limit: "1mb" }));

// Mock session middleware for parsing userId and tier
app.use((req, res, next) => {
  if (req.body) {
    req.session = {
      user: {
        id: req.body.userId,
        tier: req.body.tier || "free"
      }
    };
  }
  next();
});

const PORT = process.env.PORT || 3001;

app.post("/api/academy/verify-lab", async (req, res) => {
  const user = req.session?.user || {};
  const task = req.body?.task || "verify-lab";
  const params = req.body?.params || {};

  const result = await aiEngine.run(task, params, {
    userId: user.id,
    tier: user.tier || "free"
  });

  let skillPassportUpdate = null;
  let passport = null;

  if (result.ok) {
    const lab = params.lab || {};
    const moduleId = lab.moduleId || params.moduleId;
    const skillId = lab.skillId || params.skillId;

    skillPassportUpdate = buildSkillPassportUpdate({
      labResult: result.data,
      moduleId,
      skillId
    });

    passport = updateSkillPassport({
      userId: user.id,
      skillPassportUpdate,
      result
    });
  }

  // Generate Unlock Decision
  const lab = params.lab || {};
  const labId = lab.labId;
  const moduleId = lab.moduleId || "admin-1";
  const nextModuleId = moduleId === "admin-1" ? "admin-2" : "unknown";
  const passingScore = lab.passingScore || 80;

  const unlockDecision = getUnlockDecision({
    userId: user.id,
    moduleId,
    nextModuleId,
    tier: user.tier,
    labId,
    passingScore
  });

  const currentPassport = passport || getSkillPassport(user.id);

  res.json({
    ...result,
    skillPassportUpdate,
    unlockDecision,
    passportSummary: {
      completedLabsCount: currentPassport.completedLabs.length,
      skillsCount: Object.keys(currentPassport.skills).length,
      attemptsCount: currentPassport.attempts?.length || 0,
      verifiedAt: currentPassport.verifiedAt?.[labId] || null,
      failedAttemptsCount: currentPassport.failedAttemptsCount?.[labId] || 0
    }
  });
});

app.get("/api/academy/passport/:userId", (req, res) => {
  res.json({
    ok: true,
    passport: getSkillPassport(req.params.userId)
  });
});

app.listen(PORT, () => {
  console.log(`TomCodeX Academy backend running on http://localhost:${PORT}`);
});
