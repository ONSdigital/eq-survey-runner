local common_rules = import '../../lib/common_rules.libsonnet';

local listIsEmpty(listName) = {
  list: listName,
  condition: 'equals',
  value: 0,
};

local listIsNotEmpty(listName) = {
  list: listName,
  condition: 'greater than',
  value: 0,
};

local estimatedAgeOver16 = {
  id: 'age-last-birthday-answer',
  condition: 'greater than or equal to',
  value: 16,
};

local estimatedAgeOver15 = {
  id: 'age-last-birthday-answer',
  condition: 'greater than or equal to',
  value: 15,
};

local estimatedAgeUnder16 = {
  id: 'age-last-birthday-answer',
  condition: 'less than',
  value: 16,
};

local estimatedAgeUnder4 = {
  id: 'age-last-birthday-answer',
  condition: 'less than',
  value: 4,
};

local estimatedAgeUnder1 = {
  id: 'age-last-birthday-answer',
  condition: 'less than',
  value: 1,
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
  listIsNotEmpty: listIsNotEmpty,
  estimatedAgeOver16: estimatedAgeOver16,
  estimatedAgeUnder16: estimatedAgeUnder16,
  estimatedAgeOver15: estimatedAgeOver15,
  estimatedAgeUnder4: estimatedAgeUnder4,
  estimatedAgeUnder1: estimatedAgeUnder1,
} + common_rules
