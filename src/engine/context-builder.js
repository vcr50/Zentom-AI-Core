export function buildContext({ product = "core", user = null, metadata = {} } = {}) {
  return {
    product,
    user,
    metadata,
    createdAt: new Date().toISOString()
  };
}
