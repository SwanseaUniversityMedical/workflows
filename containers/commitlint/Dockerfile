FROM node:20-alpine
WORKDIR /usr/app
RUN npm install @commitlint/config-conventional @commitlint/cli conventional-changelog-conventionalcommits
ENTRYPOINT ["commitlint"]