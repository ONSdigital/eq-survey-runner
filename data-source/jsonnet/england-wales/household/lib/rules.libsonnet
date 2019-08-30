local common_rules = import '../../lib/common_rules.libsonnet';

{
  isNotProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'Yes',
  },
  isProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'No',
  },
} + common_rules
