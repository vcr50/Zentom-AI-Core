import { GeminiProvider } from "../providers/gemini-provider.js";
import { OllamaProvider } from "../providers/ollama-provider.js";
import { OpenSourceProvider } from "../providers/open-source-provider.js";

export function createModelProvider(provider = process.env.AI_PROVIDER || "mock") {
  switch (provider) {
    case "gemini":
      return new GeminiProvider();
    case "ollama":
      return new OllamaProvider();
    case "open-source":
      return new OpenSourceProvider();
    case "mock":
      return {
        async generate() {
          return {
            model: "zentom-mock-v1",
            text: "Mock provider response."
          };
        }
      };
    default:
      throw new Error(`Unsupported AI provider: ${provider}`);
  }
}
