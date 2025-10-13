FROM git.docker-sandbox.place-start.ru/placestart/node:22.19-alpine3.21

RUN mkdir -p /app && \
  chown -R node:node /app

WORKDIR /app

USER node

ENV npm_config_cache=/app/.npm

CMD ["/bin/sh", "-c", "npm install && npm cache clean --force && rm -rf /tmp/nitro/ && npm run dev"]