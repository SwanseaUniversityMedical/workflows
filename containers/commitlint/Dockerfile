FROM node:20-alpine
WORKDIR /usr/app
RUN npm install commitlint@19.3.0 @commitlint/config-conventional @commitlint/cli
RUN yarn add -D conventional-changelog-conventionalcommits
WORKDIR /