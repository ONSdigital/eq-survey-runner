local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'date-of-birth-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'date-of-birth-answer',
      mandatory: true,
      type: 'Date',
      maximum: {
        value: 'now',
      },
      minimum: {
        value: '1900-01-01',
      },
    },
  ],
};

local nonProxyTitle = 'What is your date of birth?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> date of birth?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'date-of-birth',
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
