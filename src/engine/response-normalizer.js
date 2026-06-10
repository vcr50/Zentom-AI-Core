export function successResponse({ task, mode, model, data, usage = null }) {
  return {
    ok: true,
    task,
    mode,
    model,
    data,
    usage,
    error: null,
    timestamp: new Date().toISOString()
  };
}

export function errorResponse({ task, code, message, status = 500, usage = null }) {
  return {
    ok: false,
    task,
    mode: "none",
    model: null,
    data: null,
    usage,
    error: {
      code,
      message,
      status
    },
    timestamp: new Date().toISOString()
  };
}
