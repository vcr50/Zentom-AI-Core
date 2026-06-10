import dotenv from "dotenv";
import { routeTask } from "./task-router.js";
import { checkQuota, consumeQuota } from "./quota-manager.js";
import { errorResponse, successResponse } from "./response-normalizer.js";
import { logUsage } from "./usage-logger.js";

dotenv.config();

export class AIEngine {
  async run(task, params = {}, request = {}) {
    const userId = request.userId || "anonymous";
    const tier = request.tier || "free";
    const hasPersonalKey = Boolean(request.personalApiKey);

    try {
      const quota = checkQuota({ userId, tier, hasPersonalKey });

      if (!quota.allowed) {
        return errorResponse({
          task,
          code: "AI_QUOTA_EXCEEDED",
          message: "You reached today's AI usage limit.",
          status: 429,
          usage: {
            tier,
            remainingToday: quota.remaining
          }
        });
      }

      const result = await routeTask(task, params);

      consumeQuota({ userId, tier, hasPersonalKey });

      logUsage({
        userId,
        tier,
        task,
        mode: result.mode,
        model: result.model,
        success: true
      });

      return successResponse({
        task,
        mode: result.mode,
        model: result.model,
        data: result.data,
        usage: {
          tier,
          remainingToday: hasPersonalKey ? Infinity : Math.max(quota.remaining - 1, 0)
        }
      });
    } catch (error) {
      logUsage({
        userId,
        tier,
        task,
        success: false,
        error: error.message
      });

      return errorResponse({
        task,
        code: "AI_ENGINE_ERROR",
        message: error.message,
        status: 500
      });
    }
  }
}

export const aiEngine = new AIEngine();
