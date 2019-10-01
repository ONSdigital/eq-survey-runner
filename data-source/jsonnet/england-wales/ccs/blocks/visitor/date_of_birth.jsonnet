local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, census_date) = {
  id: 'visitor-date-of-birth-question',
  description: '',
  type: 'MutuallyExclusive',
  title: title,
  mandatory: false,
  answers: [
    {
      id: 'visitor-date-of-birth-answer',
      mandatory: false,
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
    {
      id: 'visitor-date-of-birth-exclusive-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'Date of birth is not known',
          value: 'Date of birth is not known',
        },
      ],
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
  id: 'visitor-date-of-birth',
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
  routing_rules: [
    {
      goto: {
        block: 'visitor-sex',
        when: [{
          id: 'visitor-date-of-birth-answer',
          condition: 'set',
        }],
      },
    },
    {
      goto: {
        block: 'visitor-age-last-birthday',
      },
    },
  ],
}
