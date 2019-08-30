local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'Have you completed an apprenticeship?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> completed an apprenticeship?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'apprenticeship-question',
  title: title,
  type: 'General',
  guidance: {
    contents: [
      {
        description: 'Include equivalent apprenticeships completed anywhere outside Northern Ireland',
      },
    ],
  },
  answers: [
    {
      id: 'apprenticeship-answer',
      mandatory: false,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
          description: 'For example, trade, advanced, foundation or modern apprenticeships',
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

{
  type: 'Question',
  id: 'apprenticeship',
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
