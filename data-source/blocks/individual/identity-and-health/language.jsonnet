local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, options) = {
  id: 'language-question',
  title: title,
  type: 'General',
  definitions: [
    {
      title: "What do we mean by 'main language'?",
      content: [
        {
          description: 'Main language is your first or preferred language.',
        },
      ],
    },
  ],
  answers: [
    {
      id: 'language-answer',
      mandatory: true,
      type: 'Radio',
    } + options,
  ],
};

local nonProxyTitle = 'What is your main language?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> main language?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local englandOptions = {
  options: [
    {
      label: 'English',
      value: 'English',
    },
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
};

local walesOptions = {
  options: [
    {
      label: 'English or Welsh',
      value: 'English or Welsh',
    },
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
};

{
  type: 'Question',
  id: 'language',
  question_variants: [
    {
      question: question(nonProxyTitle, englandOptions),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, englandOptions),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, walesOptions),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, walesOptions),
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
