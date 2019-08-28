local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

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
          label: 'Single, never married and never in a same-sex civil partnership',
          value: 'Single, never married and never in a same-sex civil partnership',
        },
        {
          label: 'Married',
          value: 'Married',
        },
        {
          label: 'In a same-sex civil partnership',
          value: 'In a same-sex civil partnership',
        },
        {
          label: 'Separated, but still legally married',
          value: 'Separated, but still legally married',
        },
        {
          label: 'Separated, but still legally in a same-sex civil partnership',
          value: 'Separated, but still legally in a same-sex civil partnership',
        },
        {
          label: 'Divorced',
          value: 'Divorced',
        },
        {
          label: 'Formerly in a same-sex civil partnership which is now legally dissolved',
          value: 'Formerly in a same-sex civil partnership which is now legally dissolved',
        },
        {
          label: 'Widowed',
          value: 'Widowed',
        },
        {
          label: 'Surviving partner from a same-sex civil partnership',
          value: 'Surviving partner from a same-sex civil partnership',
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

local nonProxyTitle = 'What is your marital or same-sex civil partnership status?';

local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> marital or same-sex civil partnership status?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'marriage-type',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
  ],
}
