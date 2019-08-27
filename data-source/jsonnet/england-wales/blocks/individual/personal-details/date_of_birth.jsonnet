local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, census_date) = {
  id: 'date-of-birth-question',
  title: title,
  guidance: {
    contents: [
      {
        description: 'For example 31 12 1970',
      },
    ],
  },
  type: 'General',
  answers: [
    {
      id: 'date-of-birth-answer',
      mandatory: true,
      type: 'Date',
      minimum: {
        value: census_date,
        offset_by: {
          years: -115,
        },
      },
      maximum: {
        value: 'now',
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

function(census_date) {
  type: 'Question',
  id: 'date-of-birth',
  question_variants: [
    {
      question: question(nonProxyTitle, census_date),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, census_date),
      when: [rules.isProxy],
    },
  ],
}
