local placeholders = import '../../../lib/placeholders.libsonnet';

{
  type: 'Question',
  id: 'accommodation-type',
  question: {
    id: 'accommodation-type-question',
    title: {
      text: 'What type of accommodation is <em>{address}<em>?',
      placeholders: [
        placeholders.address,
      ],
    },
    type: 'General',
    answers: [
      {
        id: 'accommodation-type-answer',
        mandatory: true,
        options: [
          {
            label: 'A communal establishment',
            value: 'A communal establishment',
            description: 'For example, student hall of residence, boarding school, armed forces base, hospital, care home, prison',
          },
          {
            label: 'A private or family household',
            value: 'A private or family household',
          },
        ],
        type: 'Radio',
      },
    ],
  },
  skip_conditions: [
    {
      when: [
        {
          meta: 'case_type',
          condition: 'equals',
          value: 'HI',
        },
      ],
    },
    {
      when: [
        {
          meta: 'case_type',
          condition: 'equals',
          value: 'CI',
        },
      ],
    },
  ],
}
