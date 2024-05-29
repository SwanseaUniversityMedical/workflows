FROM node:20-alpine
WORKDIR /tmp
RUN npm install -g @commitlint/config-conventional @commitlint/cli conventional-changelog-conventionalcommits
RUN alias commitlint='commitlint --extends "@commitlint/config-conventional"'
WORKDIR /