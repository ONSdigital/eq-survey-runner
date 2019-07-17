{
  type: 'Question',
  id: 'proxy',
  question: {
    id: 'proxy-question',
    title: 'Are you answering the questions on behalf of someone else?',
    type: 'General',
    answers: [
      {
        id: 'proxy-answer',
        mandatory: false,
        default: 'Yes',
        options: [
          {
            label: 'No, I’m answering for myself',
            value: 'No',
          },
          {
            label: 'Yes',
            value: 'Yes',
          },
        ],
        type: 'Radio',
      },
    ],
  },
}
