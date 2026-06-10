export class ZentomAIError extends Error {
  constructor(message, { code = "AI_ERROR", status = 500 } = {}) {
    super(message);
    this.name = "ZentomAIError";
    this.code = code;
    this.status = status;
  }
}
