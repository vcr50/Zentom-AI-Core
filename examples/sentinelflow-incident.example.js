import { aiEngine } from "../src/index.js";

const result = await aiEngine.run("chat", {
  message: "Summarize this sanitized incident."
});

console.log(JSON.stringify(result, null, 2));
