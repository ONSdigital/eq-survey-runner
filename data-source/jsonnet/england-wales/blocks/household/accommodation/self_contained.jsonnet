{
  type: 'Question',
  id: 'self-contained',
  question: {
    id: 'self-contained-question',
    title: 'Are all the rooms in this accommodation, including the kitchen, bathroom and toilet, behind a door that only this household can use?',
    type: 'General',
    definitions: [{
      title: 'What is a “household”?',
      contents: [{
        description: 'One person living alone; or a group of people, who are not necessarily related, living at the same address who share cooking facilities and share a living room or sitting room or dining area.',
      }]
    }],
    answers: [{
      id: 'self-contained-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No, one or more rooms are shared with another household',
          value: 'No',
        },
      ],
      type: 'Radio',
    }],
  },
}
