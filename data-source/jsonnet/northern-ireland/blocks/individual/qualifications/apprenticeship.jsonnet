local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

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
      mandatory: true,
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
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle),
      when: [rules.proxyYes],
    },
  ],
}
