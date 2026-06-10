export class OllamaProvider {
  constructor({ baseUrl = process.env.OLLAMA_BASE_URL, model = process.env.OLLAMA_MODEL } = {}) {
    this.baseUrl = baseUrl;
    this.model = model;
  }

  async generate() {
    throw new Error("Ollama provider is not configured in this MVP.");
  }
}
