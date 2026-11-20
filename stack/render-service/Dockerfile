# Playwright's own image already has Chromium and its system libraries.
FROM mcr.microsoft.com/playwright:v1.49.0-noble
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY server.mjs ./
COPY templates ./templates
ENV OUT_DIR=/data PORT=4000
EXPOSE 4000
CMD ["node", "server.mjs"]
