{
  type: 'Question',
  id: 'government-services',
  question: {
    id: 'government-services-question',
    title: 'In the last year, how have you or your household used online government services?',
    guidance: {
      contents: [
        {
          description: 'This refers to any interaction you might have with public authorities online, such as DVLA, HMRC, local council or health related services.',
        },
      ],
    },
    instruction: 'Tell respondent to turn to <strong>Showcard 7</strong>',
    type: 'MutuallyExclusive',
    mandatory: false,
    answers: [
      {
        id: 'government-services-answer',
        mandatory: false,
        type: 'Checkbox',
        options: [
          {
            label: 'Completing forms online',
            value: 'Completing forms online',
            description: 'For example, taxing a car, registering to vote, applying for school places',
          },
          {
            label: 'Applying for official documents',
            value: 'Applying for official documents',
            description: 'For example, passports, visas',
          },
          {
            label: 'Used paper-based services',
            value: 'Used paper-based services',
          },
        ],
      },
      {
        id: 'government-services-answer-exclusive',
        type: 'Checkbox',
        mandatory: false,
        options: [
          {
            label: 'Did not use government services',
            value: 'Did not use government services',
          },
        ],
      },
    ],
  },
}
