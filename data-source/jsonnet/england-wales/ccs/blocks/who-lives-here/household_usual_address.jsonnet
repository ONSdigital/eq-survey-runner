{
  type: 'Question',
  id: 'household-usual-address',
  question: {
    id: 'household-usual-address-question',
    title: 'On Sunday 13 October 2019 what was your usual address?',
    type: 'General',
    answers: [
      {
        id: 'household-usual-address-answer-building',
        label: 'Address line 1',
        mandatory: false,
        type: 'TextField',
      },
      {
        id: 'household-usual-address-answer-street',
        label: 'Address line 2',
        mandatory: false,
        type: 'TextField',
      },
      {
        id: 'household-usual-address-answer-city',
        label: 'Town or city',
        mandatory: false,
        type: 'TextField',
      },
      {
        id: 'household-usual-address-answer-county',
        label: 'County (optional)',
        mandatory: false,
        type: 'TextField',
      },
      {
        id: 'household-usual-address-answer-postcode',
        label: 'Postcode',
        mandatory: false,
        type: 'TextField',
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'who-lives-here-section-summary',
      },
    },
  ],
}
