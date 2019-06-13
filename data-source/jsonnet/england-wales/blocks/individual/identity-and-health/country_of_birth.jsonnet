local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local nonProxyTitle = 'What is your country of birth?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> country of birth?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local englandOptions = {
  options: [
    {
      label: 'England',
      value: 'England',
    },
    {
      label: 'Wales',
      value: 'Wales',
    },
    {
      label: 'Scotland',
      value: 'Scotland',
    },
    {
      label: 'Northern Ireland',
      value: 'Northern Ireland',
    },
    {
      label: 'Republic of Ireland',
      value: 'Republic of Ireland',
    },
    {
      label: 'Elsewhere',
      value: 'Other',
      detail_answer: {
        id: 'country-of-birth-answer-other',
        type: 'TextField',
        mandatory: false,
        label: 'Please specify current name of country',
      },
    },
  ],
};

local walesOptions = {
  options: [
    {
      label: 'Wales',
      value: 'Wales',
    },
    {
      label: 'England',
      value: 'England',
    },
    {
      label: 'Scotland',
      value: 'Scotland',
    },
    {
      label: 'Northern Ireland',
      value: 'Northern Ireland',
    },
    {
      label: 'Republic of Ireland',
      value: 'Republic of Ireland',
    },
    {
      label: 'Elsewhere',
      value: 'Other',
      detail_answer: {
        id: 'country-of-birth-answer-other',
        type: 'TextField',
        mandatory: false,
        label: 'Please specify current name of country',
      },
    },
  ],
};

local question(title, region_code) = (
  local radioOptions = if region_code == 'GB-WLS' then walesOptions else englandOptions;
  {
    id: 'country-of-birth-question',
    title: title,
    type: 'General',
    answers: [
      {
        id: 'country-of-birth-answer',
        mandatory: true,
        type: 'Radio',
      } + radioOptions,
    ],
  }
);

function(region_code) {
  type: 'Question',
  id: 'country-of-birth',
  question_variants: [
    {
      question: question(nonProxyTitle, region_code),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, region_code),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'arrive-in-country',
        when: [
          {
            id: 'country-of-birth-answer',
            condition: 'equals',
            value: 'Other',
          },
        ],
      },
    },
    {
      goto: {
        block: 'arrive-in-country',
        when: [
          {
            id: 'country-of-birth-answer',
            condition: 'equals',
            value: 'Republic of Ireland',
          },
        ],
      },
    },
    {
      goto: {
        block: 'national-identity',
        when: [
          {
            id: 'country-of-birth-answer',
            condition: 'equals any',
            values: ['Wales', 'England', 'Scotland', 'Northern Ireland'],
          },
          rules.under3,
        ],
      },
    },
    {
      goto: {
        block: if region_code == 'GB-WLS' then 'understand-welsh' else 'language',
      },
    },
  ],
}
