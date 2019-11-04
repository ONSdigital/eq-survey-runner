local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

function(census_date) {
  type: 'Question',
  id: 'visitor-date-of-birth',
  question: {
    id: 'visitor-date-of-birth-question',
    description: '',
    type: 'MutuallyExclusive',
    title: {
      text: 'What is {person_name_possessive} date of birth?',
      placeholders: [placeholders.personNamePossessive],
    },
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
  },
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
