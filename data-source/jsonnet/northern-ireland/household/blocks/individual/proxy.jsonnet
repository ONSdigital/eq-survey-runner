local placeholders = import '../../../lib/placeholders.libsonnet';


{
  type: 'Question',
  id: 'proxy',
  question: {
    id: 'proxy-question',
    title: {
      text: 'Are you <em>{person_name}?</em>',
      placeholders: [
        placeholders.personName,
      ],
    },
    type: 'General',
    answers: [
      {
        id: 'proxy-answer',
        mandatory: false,
        default: 'No',
        options: [
          {
            label: 'Yes, I am',
            value: 'Yes',
          },
          {
            label: 'No, I am answering on their behalf',
            value: 'No',
          },
        ],
        type: 'Radio',
      },
    ],
  },
}
