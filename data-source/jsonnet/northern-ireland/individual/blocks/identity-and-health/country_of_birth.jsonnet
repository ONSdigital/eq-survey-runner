local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'What is your country of birth?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> country of birth?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

local question(title) = {
  id: 'country-of-birth-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'country-of-birth-answer',
      mandatory: true,
      type: 'Radio',
      options: [
        {
          label: 'Northern Ireland',
          value: 'Northern Ireland',
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
          label: 'Wales',
          value: 'Wales',
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
    },
  ],
};

{
  type: 'Question',
  id: 'country-of-birth',
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
  routing_rules: [
    {
      goto: {
        block: 'arrive-in-country',
        when: [
          {
            id: 'country-of-birth-answer',
            condition: 'not equals',
            value: 'Northern Ireland',
          },
        ],
      },
    },
    {
      goto: {
        block: 'passports',
        when: [rules.under1],
      },
    },
    {
      goto: {
        block: 'past-usual-household-address',
      },
    },
  ],
}
