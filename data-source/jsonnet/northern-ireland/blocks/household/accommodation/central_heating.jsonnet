local placeholders = import '../../../lib/placeholders.libsonnet';

{
  type: 'Question',
  id: 'central-heating',
  question: {
    id: 'central-heating-question',
    type: 'MutuallyExclusive',
    mandatory: false,
    title: {
      text: 'What type of central heating does <em>{address}</em> have?',
      placeholders: [placeholders.address],
    },
    guidance: {
      contents: [
        {
          title: 'Include central heating systems that generate heat for multiple rooms whether or not you use them',
        },
      ],
    },
    answers: [
      {
        id: 'central-heating-answer',
        mandatory: false,
        type: 'Checkbox',
        options: [
          {
            label: 'Oil',
            value: 'Oil',
          },
          {
            label: 'Mains gas',
            value: 'Mains gas',
          },
          {
            label: 'Tank or bottled gas',
            value: 'Tank or bottled gas',
          },
          {
            label: 'Electric',
            value: 'Electric',
            description: 'Including storage heaters',
          },
          {
            label: 'Wood',
            value: 'Wood',
          },
          {
            label: 'Solid fuel',
            value: 'Solid fuel',
            description: 'Including coal',
          },
          {
            label: 'Renewable energy',
            value: 'Renewable energy',
            description: 'For example wood pellets, Biomass, air or ground heat source systems',
          },
          {
            label: 'Other central heating',
            value: 'Other central heating',
          },
        ],
      },
      {
        id: 'central-heating-answer-exclusive',
        type: 'Checkbox',
        mandatory: false,
        options: [
          {
            label: 'No central heating',
            value: 'No central heating',
          },
        ],
      },
    ],
  },
}
