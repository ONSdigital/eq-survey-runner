local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'marriage-type-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'marriage-type-answer',
      mandatory: true,
      options: [
        {
          label: 'Never married and never registered a civil partnership',
          value: 'Never',
        },
        {
          label: 'Married',
          value: 'Married',
        },
        {
          label: 'In a registered civil partnership',
          value: 'In a registered civil partnership',
        },
        {
          label: 'Separated, but still legally married',
          value: 'Separated, but still legally married',
        },
        {
          label: 'Separated, but still legally in a civil partnership',
          value: 'Separated, but still legally in a civil partnership',
        },
        {
          label: 'Divorced',
          value: 'Divorced',
        },
        {
          label: 'Formerly in a civil partnership which is now legally dissolved',
          value: 'Formerly in a civil partnership which is now legally dissolved',
        },
        {
          label: 'Widowed',
          value: 'Widowed',
        },
        {
          label: 'Surviving partner from a registered civil partnership',
          value: 'Surviving partner from a registered civil partnership',
        },
      ],
      type: 'Radio',
    },
  ],
};

local gotoRule(blockId, whenValue) = {
  goto: {
    block: blockId,
    when: [
      {
        id: 'marriage-type-answer',
        condition: 'equals',
        value: whenValue,
      },
    ],
  },
};

local nonProxyTitle = {
  text: 'On {census_date}, what is your legal marital or registered civil partnership status?',
  placeholders: [
    placeholders.censusDate,
  ],
};
local proxyTitle = {
  text: 'On {census_date}, what is <em>{person_name_possessive}</em> legal marital or registered civil partnership status?',
  placeholders: [
    placeholders.censusDate,
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'marriage-type',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    gotoRule('another-address', 'Never'),
    gotoRule('current-marriage-status', 'Married'),
    gotoRule('current-partnership-status', 'In a registered civil partnership'),
    gotoRule('current-marriage-status', 'Separated, but still legally married'),
    gotoRule('current-partnership-status', 'Separated, but still legally in a civil partnership'),
    gotoRule('previous-marriage-status', 'Divorced'),
    gotoRule('previous-partnership-status', 'Formerly in a civil partnership which is now legally dissolved'),
    gotoRule('previous-marriage-status', 'Widowed'),
    gotoRule('previous-partnership-status', 'Surviving partner from a registered civil partnership'),
    {
      goto: {
        block: 'another-address',
      },
    },
  ],
}
