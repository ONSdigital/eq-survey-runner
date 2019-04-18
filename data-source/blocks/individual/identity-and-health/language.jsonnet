local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, definitionDescription, regionOption) = {
  id: 'language-question',
  title: title,
  type: 'General',
  definitions: [{
    title: 'What do we mean by “main language”?',
    content: [
      {
        description: definitionDescription,
      },
    ],
  }],
  answers: [
    {
      id: 'language-answer',
      mandatory: true,
      type: 'Radio',
      options: [
        regionOption,
        {
          label: 'Other',
          value: 'Other',
          description: 'Including British Sign Language',
          detail_answer: {
            id: 'language-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify main language',
          },
        },
      ],
    },
  ],
};

local nonProxyTitle = 'What is your main language?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> main language?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};
local nonProxyDefinitionDescription = 'Your main language is the language you use most naturally. It could be the language you use at home.';
local proxyDefinitionDescription = 'Their main language is the language they use most naturally. It could be the language they use at home.';

local englandOption = {
  label: 'English',
  value: 'English',
};

local walesOption = {
  label: 'English or Welsh',
  value: 'English or Welsh',
};

{
  type: 'Question',
  id: 'language',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDefinitionDescription, englandOption),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, proxyDefinitionDescription, englandOption),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, nonProxyDefinitionDescription, walesOption),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, proxyDefinitionDescription, walesOption),
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'national-identity',
        when: [
          {
            id: 'language-answer',
            condition: 'equals',
            value: 'English',
          },
        ],
      },
    },
    {
      goto: {
        block: 'national-identity',
        when: [
          {
            id: 'language-answer',
            condition: 'equals',
            value: 'English or Welsh',
          },
        ],
      },
    },
    {
      goto: {
        block: 'english',
      },
    },
  ],
}
