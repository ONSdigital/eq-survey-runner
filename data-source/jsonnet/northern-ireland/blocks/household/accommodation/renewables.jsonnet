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
}
