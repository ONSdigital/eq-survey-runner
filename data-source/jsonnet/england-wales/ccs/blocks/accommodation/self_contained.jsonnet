local placeholders = import '../../../lib/placeholders.libsonnet';

{
  type: 'Question',
  id: 'self-contained',
  question: {
    id: 'self-contained-question',
    title: {
      text: 'Are all the rooms at {address}, including the kitchen, bathroom and toilet, behind a door that only this household can use?',
      placeholders: [placeholders.address],
    },
    description: '<em>If "No" confirm one or more rooms are shared with another household</em>',
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