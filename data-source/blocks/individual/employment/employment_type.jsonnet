local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'employment-type-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'employment-type-answer',
      mandatory: true,
      options: [
        {
          label: 'Retired',
          value: 'Retired',
          description: 'Whether receiving a pension or not',
        },
        {
          label: 'Studying',
          value: 'Studying',
        },
        {
          label: 'Looking after home or family',
          value: 'Looking after home or family',
        },
        {
          label: 'Long-term sick or disabled',
          value: 'Long-term sick or disabled',
        },
        {
          label: 'Other',
          value: 'Other',
        },
      ],
      type: 'Checkbox',
    },
  ],
};

local nonProxyTitle = 'Which of the following describes what you were doing in the last seven days?';
local proxyTitle = {
  text: 'Which of the following describes what <em>{person_name}</em> was doing in the last seven days?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'employment-type',
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
}
