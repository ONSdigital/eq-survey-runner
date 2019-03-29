local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, options) = {
  id: 'country-of-birth-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'country-of-birth-answer',
      mandatory: true,
      type: 'Radio',
    } + options,
  ],
};

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

{
  type: 'Question',
  id: 'country-of-birth',
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
        block: 'arrive-in-uk',
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
        block: 'arrive-in-uk',
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
        block: 'understand-welsh',
        when: [
          {
            meta: 'region_code',
            condition: 'equals',
            value: 'GB-WLS',
          },
        ],
      },
    },
    {
      goto: {
        block: 'language',
      },
    },
  ],
}
