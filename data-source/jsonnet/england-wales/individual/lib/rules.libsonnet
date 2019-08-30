local common_rules = import '../../lib/common_rules.libsonnet';

{
  isNotProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'No',
  },
  isProxy: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'Yes',
  },
} + common_rules
