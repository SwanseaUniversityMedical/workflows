ARG NODE_VERSION=20.11.0
ARG ALPINE_VERSION=3.19.1

FROM node:${NODE_VERSION}-alpine AS node

FROM alpine:${ALPINE_VERSION}

COPY --from=node /usr/lib /usr/lib
COPY --from=node /usr/local/lib /usr/local/lib
COPY --from=node /usr/local/include /usr/local/include
COPY --from=node /usr/local/bin /usr/local/bin

# nice clean home for our action files
RUN mkdir /action
WORKDIR /action

# install deps
COPY ./package.json ./package-lock.json ./
RUN npm ci --only=prod

# copy in entrypoint after dependency installation
COPY entrypoint.js .

ENTRYPOINT ["node", "/action/entrypoint.js"]
