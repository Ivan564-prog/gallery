FROM git.docker-sandbox.place-start.ru/placestart/node:22.19-alpine3.21 as builder 

COPY ./frontend/package.json ./frontend/package-lock.json /app/

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm npm clean-install

COPY ./frontend /app 


ARG HOST='django-core.docker-sandbox.place-start.ru'
ENV HOST=$HOST

#ENV HOST='https://django-core.docker-sandbox.place-start.ru'
ENV BACKEND_HOST='http://backend:8000'

RUN npm run build


FROM git.docker-sandbox.place-start.ru/placestart/node:22.9-alpine3.19

EXPOSE 3000

ENV NITRO_PORT=3000

ENV NITRO_HOST="0.0.0.0"

COPY --chown=node:node --from=builder /app/.output /app/
COPY --chown=node:node --from=builder /app/package-lock.json /app/

USER node

CMD ["/usr/local/bin/node", "/app/server/index.mjs"]
