local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

{
  type: 'Question',
  id: 'accommodation-type',
  question: {
    id: 'accommodation-type-question',
    title: {
      text: 'What type of accommodation is {address}?',
      placeholders: [placeholders.address],
    },
    description: '<em>Tell respondent to turn to <strong>Showcard 3</strong></em>',
    type: 'General',
    answers: [
      {
        id: 'accommodation-type-answer',
        mandatory: false,
        type: 'Radio',
        options: [
          {
            label: 'Whole house or bungalow',
            value: 'Whole house or bungalow',
          },
          {
            label: 'Flat, maisonette or apartment',
            value: 'Flat, maisonette or apartment',
          },
          {
            label: 'Caravan or other mobile or temporary structure',
            value: 'Caravan or other mobile or temporary structure',
          },
        ],
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'type-of-house',
        when: [rules.accommodationIsHouse],
      },
    },
    {
      goto: {
        block: 'type-of-flat',
        when: [rules.accommodationIsFlat],
      },
    },
    {
      goto: {
        block: 'self-contained',
      },
    },
  ],
}
