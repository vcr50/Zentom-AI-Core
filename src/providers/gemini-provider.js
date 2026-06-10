export class GeminiProvider {
  constructor({ apiKey = process.env.GEMINI_API_KEY } = {}) {
    this.apiKey = apiKey;
  }

  async generate() {
    throw new Error("Gemini provider is not configured in this MVP.");
  }
}
