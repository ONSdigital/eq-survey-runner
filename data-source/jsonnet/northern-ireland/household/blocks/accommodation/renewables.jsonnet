local placeholders = import '../../../lib/placeholders.libsonnet';

{
  type: 'Question',
  id: 'renewables',
  question: {
    id: 'renewables-question',
    mandatory: false,
    title: {
      text: 'What type of renewable energy systems does <em>{address}</em> have?',
      placeholders: [placeholders.address],
    },
    type: 'MutuallyExclusive',
    answers: [
      {
        id: 'renewables-answer',
        mandatory: false,
        type: 'Checkbox',
        options: [
          {
            label: 'Solar panels for electricity',
            value: 'Solar panels for electricity',
          },
          {
            label: 'Solar panels for heating water',
            value: 'Solar panels for heating water',
          },
          {
            label: 'Wind turbine',
            value: 'Wind turbine',
          },
          {
            label: 'Other',
            value: 'Other',
            detail_answer: {
              id: 'renewables-answer-other',
              type: 'TextField',
              mandatory: false,
              label: 'Enter renewable energy system',
            },
          },
        ],
      },
      {
        id: 'renewables-answer-exclusive',
        type: 'Checkbox',
        mandatory: false,
        options: [
          {
            label: 'No renewable energy systems',
            value: 'No renewable energy systems',
          },
        ],
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'accommodation-section-summary',
        when: [rules.listIsEmpty('household')],
      },
    },
    {
      goto: {
        block: 'own-or-rent',
      },
    },
  ],
}
