local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'What is your main language?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> main language?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local englandOption = {
  label: 'English',
  value: 'English',
};

local walesOption = {
  label: 'English or Welsh',
  value: 'English or Welsh',
};

local nonProxyDefinitionDescription = 'Your main language is the language you use most naturally. It could be the language you use at home.';
local proxyDefinitionDescription = 'Their main language is the language they use most naturally. It could be the language they use at home.';

local question(title, definitionDescription, region_code) = (
  local regionOption = if region_code == 'GB-WLS' then walesOption else englandOption;
  {
    id: 'language-question',
    title: title,
    type: 'General',
    definitions: [{
      title: 'What do we mean by “main language”?',
      contents: [
        {
          description: definitionDescription,
        },
      ],
    }],
    answers: [
      {
        id: 'language-answer',
        mandatory: false,
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
  }
);

function(region_code) {
  type: 'Question',
  id: 'language',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyDefinitionDescription, region_code),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyDefinitionDescription, region_code),
      when: [rules.proxyYes],
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
