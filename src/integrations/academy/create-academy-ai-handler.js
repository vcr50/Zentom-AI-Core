import { aiEngine } from "../../core/ai-engine.js";
import { buildSkillPassportUpdate } from "../../intelligence-layers/learning/skill-passport.js";

function getSessionUser(req) {
  return req.session?.user || {};
}

function getPassportContext(body = {}) {
  return {
    moduleId: body.moduleId || body.params?.moduleId,
    skillId: body.skillId || body.params?.skillId
  };
}

export function createAcademyAiHandler({
  engine = aiEngine,
  updateSkillPassport = async () => null
} = {}) {
  return async function academyAiHandler(req, res) {
    const user = getSessionUser(req);
    const task = req.body?.task;
    const params = req.body?.params || {};

    const result = await engine.run(task, params, {
      userId: user.id,
      tier: user.tier || "free"
    });

    let skillPassportUpdate = null;

    if (task === "verify-lab" && result.ok) {
      const { moduleId, skillId } = getPassportContext(req.body);

      skillPassportUpdate = buildSkillPassportUpdate({
        labResult: result.data,
        moduleId,
        skillId
      });

      await updateSkillPassport({
        userId: user.id,
        update: skillPassportUpdate,
        aiResult: result
      });
    }

    return res.json({
      ...result,
      skillPassportUpdate
    });
  };
}
