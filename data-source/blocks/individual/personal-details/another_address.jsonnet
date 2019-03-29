local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'another-address-question',
  title: title,
  type: 'General',
  definitions: [
    {
      title: "What do we mean by 'another address'?",
      content: [
        {
          description: "Another address refers to a different address to the one at the start of this survey. This might be another parent or guardian’s address, a term-time address, a partner's address, or a holiday home.",
        },
      ],
    },
  ],
  description: 'This could be more than 30 days in a row or divided across the year',
  answers: [
    {
      id: 'another-address-answer',
      mandatory: true,
      options: [
        {
          label: 'No',
          value: 'No',
        },
        {
          label: 'Yes, an address within the UK',
          value: 'Yes, an address within the UK',
        },
        {
          label: 'Yes, an address outside the UK',
          value: 'Other',
          detail_answer: {
            id: 'another-address-answer-other-country',
            type: 'TextField',
            mandatory: true,
            label: 'Please specify a country',
          },
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Do you stay at another address for more than 30 days a year?';
local proxyTitle = {
  text: 'Does <em>{person_name_possessive}</em> stay at another address for more than 30 days a year?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'another-address',
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
    {
      goto: {
        block: 'in-education',
        when: [
          {
            id: 'another-address-answer',
            condition: 'equals',
            value: 'No',
          },
        ],
      },
    },
    {
      goto: {
        block: 'other-address',
        when: [
          {
            id: 'another-address-answer',
            condition: 'equals',
            value: 'Yes, an address within the UK',
          },
        ],
      },
    },
    {
      goto: {
        block: 'address-type',
      },
    },
  ],
}
