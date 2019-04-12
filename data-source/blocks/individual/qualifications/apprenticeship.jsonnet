local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'apprenticeship-question',
  title: title,
  type: 'General',
  guidance: {
    content: [
      {
        title: 'Include equivalent apprenticeships completed anywhere outside England and Wales',
      },
    ],
  },
  answers: [
    {
      id: 'apprenticeship-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
          description: 'For example trade, advanced, foundation, modern',
        },
        {
          label: 'No',
          value: 'No',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Have you completed an apprenticeship?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> completed an apprenticeship?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'apprenticeship',
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
