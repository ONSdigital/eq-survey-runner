local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'health-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'health-answer',
      mandatory: true,
      options: [
        {
          label: 'Very good',
          value: 'Very good',
        },
        {
          label: 'Good',
          value: 'Good',
        },
        {
          label: 'Fair',
          value: 'Fair',
        },
        {
          label: 'Bad',
          value: 'Bad',
        },
        {
          label: 'Very bad',
          value: 'Very bad',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'How is your health in general?';
local proxyTitle = {
  text: 'How is <em>{person_name_possessive}</em> health in general?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'health',
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
