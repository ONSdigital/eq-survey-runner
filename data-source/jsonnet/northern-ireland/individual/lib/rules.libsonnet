local common_rules = import '../../lib/common_rules.libsonnet';

{
  isNotProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'For myself',
  },
  isProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'For someone else',
  },
} + common_rules
