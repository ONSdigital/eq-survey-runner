{
  type: 'Question',
  id: 'proxy',
  question: {
    id: 'proxy-question',
    title: '<em>Interviewer Note: Are they answering the questions for themselves or on someone else’s behalf?</em>',
    type: 'General',
    answers: [
      {
        id: 'proxy-answer',
        mandatory: false,
        default: 'Yes',
        options: [
          {
            label: 'Yes, they are answering for themselves',
            value: 'Yes',
          },
          {
            label: "No, they are answering on someone else's behalf",
            value: 'No',
          },
        ],
        type: 'Radio',
      },
    ],
  },
}
