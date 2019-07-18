{
  type: 'Question',
  id: 'proxy',
  question: {
    id: 'proxy-question',
    title: 'Are you answering these questions for yourself or for someone else?',
    type: 'General',
    answers: [
      {
        id: 'proxy-answer',
        mandatory: false,
        default: 'For someone else',
        options: [
          {
            label: 'For myself',
            value: 'For myself',
          },
          {
            label: 'For someone else',
            value: 'For someone else',
          },
        ],
        type: 'Radio',
      },
    ],
  },
}
