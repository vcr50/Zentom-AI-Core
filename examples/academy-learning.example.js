import { aiEngine } from "../src/index.js";

const result = await aiEngine.run(
  "chat",
  {
    message: "Give a short learning hint for a sanitized sample exercise."
  },
  {
    userId: "demo-learner",
    tier: "free"
  }
);

console.log(JSON.stringify(result, null, 2));
