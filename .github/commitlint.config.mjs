// import { RuleConfigSeverity } from '@commitlint/types';
import 'conventional-changelog-conventionalcommits';

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
        'labeler'
    ]]
  }
};
