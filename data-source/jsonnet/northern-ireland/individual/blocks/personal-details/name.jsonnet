local rules = import 'rules.libsonnet';

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
          MANDATORY_TEXTFIELD: 'Enter a first name to continue',
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
      mandatory: true,
      type: 'TextField',
      validation: {
        messages: {
          MANDATORY_TEXTFIELD: 'Enter a last name to continue',
        },
      },
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
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
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
