local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, census_date) = {
    id: 'visitor-age-last-birthday-question',
    description: '',
    type: 'General',
    title: title,
    mandatory: false,
    answers: [
        {
            id: 'visitor-age-last-birthday-answer',
            label: 'Age',
            mandatory: true,
            type: 'TextField',
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
            id: 'visitor-age-estimate-answer',
            mandatory: false,
            label: '',
            type: 'Checkbox',
            options: [
                {
                    label: 'Estimate',
                    value: 'Estimate',
                },
            ],
        },
    ],
};

local nonProxyTitle = 'What was your age on your last birthday?';

local proxyTitle = {
  text: 'What was <em>{person_name_possessive}</em> on their last birthday?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

function(census_date) {
  type: 'Question',
  id: 'visitor-age-last-birthday',
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
      },
    },
  ],
}


