FROM node:20-alpine
WORKDIR /usr/app
RUN npm install conventional-changelog-conventionalcommits
WORKDIR /
ENTRYPOINT ["commitlint"]