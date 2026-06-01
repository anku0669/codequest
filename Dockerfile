# Ironyx Code — production image (hardened)
FROM node:20-alpine

# Small init so Node receives signals correctly (clean shutdown).
RUN apk add --no-cache wget tini

WORKDIR /app

# Install dependencies first (better layer caching). Use the lockfile for
# reproducible installs; fall back to `npm install` if no lockfile is present.
COPY package.json package-lock.json* ./
RUN if [ -f package-lock.json ]; then npm ci --omit=dev; else npm install --omit=dev; fi \
    && npm cache clean --force

# Copy app source with ownership set to the built-in non-root `node` user.
COPY --chown=node:node server.js ./
COPY --chown=node:node public ./public
COPY --chown=node:node scripts ./scripts

ENV NODE_ENV=production
ENV PORT=3000
EXPOSE 3000

# Drop root.
USER node

# Basic healthcheck against the API.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/api/health || exit 1

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
