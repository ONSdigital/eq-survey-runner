local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, definitionContent, regionOptions) = {
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
      options: regionOptions + [
        {
          label: 'Scottish',
          value: 'Scottish',
        },
        {
          label: 'Northern Irish',
          value: 'Northern Irish',
        },
        {
          label: 'British',
          value: 'British',
        },
        {
          label: 'Other',
          value: 'Other',
          detail_answer: {
            id: 'national-identity-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please describe your national identity',
          },
        },
      ],
    },
  ],
};

local nonProxyTitle = 'How would you describe your national identity?';
local nonProxyDefinitionContent = [
  {
    description: 'National identity is not dependent on your ethnic group or citizenship.',
  },
  {
    description: 'It is about the country or countries where you feel you belong or think of as home.',
  },
];
local proxyTitle = {
  text: 'How would <em>{person_name}</em> describe their national identity?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyDefinitionContent = [
  {
    description: 'National identity is not dependent on their ethnic group or citizenship.',
  },
  {
    description: 'It is about the country or countries where they feel they belong or think of as home.',
  },
];

local englandOptions = [
  {
    label: 'English',
    value: 'English',
  },
  {
    label: 'Welsh',
    value: 'Welsh',
  },
];

local walesOptions = [
  {
    label: 'Welsh',
    value: 'Welsh',
  },
  {
    label: 'English',
    value: 'English',
  },
];

{
  type: 'Question',
  id: 'national-identity',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDefinitionContent, englandOptions),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, proxyDefinitionContent, englandOptions),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, nonProxyDefinitionContent, walesOptions),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, proxyDefinitionContent, walesOptions),
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
}
