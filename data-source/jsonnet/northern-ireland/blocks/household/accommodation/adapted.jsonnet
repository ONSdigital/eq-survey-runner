local placeholders = import '../../../lib/placeholders.libsonnet';

{
  type: 'Question',
  id: 'adapted',
  question: {
    id: 'adapted-question',
    mandatory: false,
    type: 'MutuallyExclusive',
    title: {
      text: 'Has <em>{address}</em> been designed or adapted for any of the following?',
      placeholders: [placeholders.address],
    },
    answers: [
      {
        id: 'adapted-answer',
        mandatory: false,
        type: 'Checkbox',
        options: [
          {
            label: 'Internal wheelchair usage',
            value: 'Internal wheelchair usage',
            description: 'For example downstairs bathroom',
          },
          {
            label: 'External wheelchair access',
            value: 'External wheelchair access',
            description: 'For example a ramp',
          },
          {
            label: 'Other physical or mobility difficulties',
            value: 'Other physical or mobility difficulties',
          },
          {
            label: 'Visual difficulties',
            value: 'Visual difficulties',
          },
          {
            label: 'Hearing difficulties',
            value: 'Hearing difficulties',
          },
          {
            label: 'Other',
            value: 'Other',
          },
        ],
      },
      {
        id: 'adapted-answer-exclusive',
        type: 'Checkbox',
        mandatory: false,
        options: [
          {
            label: 'None of these',
            value: 'None of these',
          },
        ],
      },
    ],
  },
}
