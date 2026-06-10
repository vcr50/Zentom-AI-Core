import { aiEngine } from "zentom-ai-core";

export function registerAcademyAiRoute(app) {
  app.post("/api/ai/run", async (req, res) => {
    const result = await aiEngine.run(req.body.task, req.body.params, {
      userId: req.session?.user?.id,
      tier: req.session?.user?.tier || "free"
    });

    res.json(result);
  });
}
