{
  type: 'Question',
  id: 'term-time-address-country',
  question: {
    id: 'term-time-address-country-question',
    title: 'Is this address in the UK?',
    type: 'General',
    answers: [
      {
        id: 'term-time-address-country-answer',
        mandatory: true,
        options: [
          {
            label: 'Yes',
            value: 'Yes',
          },
          {
            label: 'No',
            value: 'No',
            detail_answer: {
              id: 'term-time-address-country-answer-other',
              type: 'TextField',
              mandatory: false,
              label: 'Please specify a country',
            },
          },
        ],
        type: 'Radio',
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'term-time-address-details',
        when: [
          {
            id: 'term-time-address-country-answer',
            condition: 'equals',
            value: 'Yes',
          },
        ],
      },
    },
    {
      goto: {
        group: 'comments-group',
      },
    },
  ],
}
