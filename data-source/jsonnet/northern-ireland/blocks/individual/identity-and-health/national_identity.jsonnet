local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'How would you describe your national identity?';
local proxyTitle = {
  text: 'How would <em>{person_name}</em> describe their national identity?',
  placeholders: [
    placeholders.personName,
  ],
};

local nonProxyDefinitionContent = [
  {
    description: 'National identity is not dependent on your ethnic group or citizenship.',
  },
  {
    description: 'It is about the country or countries where you feel you belong or think of as home.',
  },
];

local proxyDefinitionContent = [
  {
    description: 'National identity is not dependent on their ethnic group or citizenship.',
  },
  {
    description: 'It is about the country or countries where they feel they belong or think of as home.',
  },
];

local nonProxyDetailAnswerLabel = 'Please describe your national identity';
local proxyDetailAnswerLabel = 'Please describe their national identity';

local question(title, definitionContent, detailAnswerLabel) = {
  id: 'national-identity-question',
  title: title,
  type: 'General',
  definitions: [
    {
      title: 'What do we mean by “national identity”?',
      content: definitionContent,
    },
  ],
  answers: [
    {
      id: 'national-identity-answer',
      mandatory: true,
      type: 'Checkbox',
      options: [
        {
          label: 'British',
          value: 'British',
        },
        {
          label: 'Irish',
          value: 'Irish',
        },
        {
          label: 'Northern Irish',
          value: 'Northern Irish',
        },
        {
          label: 'English',
          value: 'English',
        },
        {
          label: 'Scottish',
          value: 'Scottish',
        },
        {
          label: 'Welsh',
          value: 'Welsh',
        },
        {
          label: 'Other',
          value: 'Other',
          detail_answer: {
            id: 'national-identity-answer-other',
            type: 'TextField',
            mandatory: false,
            label: detailAnswerLabel,
          },
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'national-identity',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDefinitionContent, nonProxyDetailAnswerLabel),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyDefinitionContent, proxyDetailAnswerLabel),
      when: [rules.proxyYes],
    },
  ],
}
