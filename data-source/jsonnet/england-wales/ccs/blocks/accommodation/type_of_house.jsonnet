{
  type: 'Question',
  id: 'type-of-house',
  question: {
    id: 'type-of-house-question',
    title: 'Which of the following is your house or bungalow?',
    type: 'General',
    answers: [{
      id: 'type-of-house-answer',
      mandatory: false,
      options: [
        {
          label: 'Detached',
          value: 'Detached',
        },
        {
          label: 'Semi-detached',
          value: 'Semi-detached',
        },
        {
          label: 'Terraced',
          value: 'Terraced',
          description: 'Including end-terrace',
        },
      ],
      type: 'Radio',
    }],
  },
  routing_rules: [{
    goto: {
      block: 'self-contained',
    },
  }],
}
