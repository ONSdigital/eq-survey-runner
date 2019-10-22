local placeholders = import '../../../lib/placeholders.libsonnet';

{
  type: 'Question',
  id: 'internet',
  question: {
    id: 'internet-question',
    title: {
      text: 'How do you and the people in your household connect to the internet at {address}?',
      placeholders: [placeholders.address],
    },
    instruction: 'Tell respondent to turn to <strong>Showcard 6</strong>',
    type: 'MutuallyExclusive',
    mandatory: false,
    answers: [
      {
        id: 'internet-answer',
        mandatory: false,
        type: 'Checkbox',
        options: [
          {
            label: 'Broadband or WiFi',
            value: 'Broadband or WiFi',
          },
          {
            label: 'A mobile phone network such as 3G or 4G',
            value: 'A mobile phone network such as 3G or 4G',
          },
          {
            label: 'Public WiFi hotspot',
            value: 'Public WiFi hotspot',
          },
        ],
      },
      {
        id: 'internet-answer-exclusive',
        type: 'Checkbox',
        mandatory: false,
        options: [
          {
            label: 'Unable to access the internet at home',
            value: 'Unable to access the internet at home',
          },
        ],
      },
    ],
  },
}
