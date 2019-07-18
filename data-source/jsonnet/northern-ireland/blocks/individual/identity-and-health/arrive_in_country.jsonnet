local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'arrive-in-country-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'arrive-in-country-answer',
      mandatory: true,
      type: 'YearDate',
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
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle),
      when: [rules.proxyYes],
    },
  ],
}
