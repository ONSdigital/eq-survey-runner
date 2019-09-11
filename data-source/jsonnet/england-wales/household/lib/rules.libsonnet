local common_rules = import '../../lib/common_rules.libsonnet';

local listIsEmpty(listName) = {
    list: listName,
    condition: 'equals',
    value: 0
};

local listIsNotEmpty(listName) = {
    list: listName,
    condition: 'greater than',
    value: 0
};

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
  listIsEmpty: listIsEmpty,
  listIsNotEmpty: listIsNotEmpty
} + common_rules
