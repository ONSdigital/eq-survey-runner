local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'name-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'first-name',
      label: 'First name',
      mandatory: true,
      type: 'TextField',
      validation: {
        messages: {
          MANDATORY_TEXTFIELD: 'Please enter a name or remove the person to continue',
        },
      },
    },
    {
      id: 'middle-names',
      label: 'Middle names',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'last-name',
      label: 'Last name',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitle = 'What is your name?';
local proxyTitle = 'What is their name?';

{
  type: 'Question',
  id: 'name',
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
        block: 'date-of-birth',
        when: [
          {
            meta: 'case_type',
            condition: 'equals',
            value: 'HI',
          },
        ],
      },
    },
    {
      goto: {
        block: 'date-of-birth',
        when: [
          {
            id: 'accommodation-type-answer',
            condition: 'equals',
            value: 'A private or family household',
          },
        ],
      },
    },
    {
      goto: {
        block: 'establishment-position',
      },
    },
  ],
}
