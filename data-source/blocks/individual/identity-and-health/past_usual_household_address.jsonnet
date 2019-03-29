local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description) = {
  id: 'past-usual-address-household-question',
  title: title,
  type: 'General',
  description: description,
  answers: [
    {
      id: 'past-usual-address-household-answer',
      mandatory: true,
      options: [
        {
          label: {
            text: '{address}',
            placeholders: [
              placeholders.address,
            ],
          },
          value: 'household-address',
        },
        {
          label: 'Student term-time or boarding school address in the UK',
          value: 'Student term-time or boarding school address in the UK',
        },
        {
          label: 'Another address in the UK',
          value: 'Another address in the UK',
        },
        {
          label: 'An address outside the UK',
          value: 'Other',
          detail_answer: {
            id: 'past-usual-address-household-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please enter the country',
          },
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'One year ago, what was your usual address?';
local nonProxyDescription = 'If you had no usual address one year ago, state the address where you were staying';
local proxyTitle = {
  text: 'One year ago, what was <em>{person_name_possessive}</em> usual address?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};
local proxyDescription = 'If they had no usual address one year ago, state the address where they were staying';

{
  type: 'Question',
  id: 'past-usual-household-address',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDescription),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyDescription),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'last-year-address',
        when: [
          {
            id: 'past-usual-address-household-answer',
            condition: 'equals',
            value: 'Student term-time or boarding school address in the UK',
          },
        ],
      },
    },
    {
      goto: {
        block: 'last-year-address',
        when: [
          {
            id: 'past-usual-address-household-answer',
            condition: 'equals',
            value: 'Another address in the UK',
          },
        ],
      },
    },
    {
      goto: {
        block: 'passports',
      },
    },
  ],
}
