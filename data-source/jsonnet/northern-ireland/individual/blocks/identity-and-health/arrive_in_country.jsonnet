local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title) = {
  id: 'arrive-in-country-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'arrive-in-country-answer',
      mandatory: false,
      type: 'YearDate',
      minimum: {
        answer_id: 'date-of-birth-answer',
      },
      maximum: {
        value: 'now',
      },
    },
  ],
};

local nonProxyTitle = 'What year did you come to live in Northern Ireland?';
local proxyTitle = {
  text: 'What year did <em>{person_name}</em> come to live in Northern Ireland?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'arrive-in-country',
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
