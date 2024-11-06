// import { RuleConfigSeverity } from '@commitlint/types';

export default {
  extends: ['@commitlint/config-conventional'],
  parserPreset: 'conventional-changelog-conventionalcommits',
  rules: {
    'scope-enum': [2, 'always', [
        '',
        'deps',
        'containers',
        'charts',
        'commitlint',
        'labeler',
        'renovate',
        'sonar-dotnet'
    ]]
  }
};
