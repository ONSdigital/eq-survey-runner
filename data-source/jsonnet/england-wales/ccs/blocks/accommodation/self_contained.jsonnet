{
  type: 'Question',
  id: 'self-contained',
  question: {
    id: 'self-contained-question',
    title: 'Are all the rooms in this accommodation, including the kitchen, bathroom and toilet, behind a door that only this household can use?',
    description: 'If "No" confirm one or more rooms are shared with another household',
    type: 'General',
    answers: [{
      id: 'self-contained-answer',
      mandatory: false,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No',
          value: 'No',
        },
      ],
      type: 'Radio',
    }],
  },
}
