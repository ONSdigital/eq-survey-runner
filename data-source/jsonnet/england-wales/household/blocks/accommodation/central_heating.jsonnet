local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

{
  type: 'Question',
  id: 'central-heating',
  question: {
    id: 'central-heating-question',
    title: {
      text: 'What type of central heating does <em>{address}</em> have?',
      placeholders: [placeholders.address],
    },
    type: 'General',
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
            label: 'No central heating',
            value: 'No central heating',
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
            label: 'Oil',
            value: 'Oil',
          },
          {
            label: 'Wood',
            value: 'Wood',
            description: 'For example, logs, waste wood or pellets',
          },
          {
            label: 'Solid fuel',
            value: 'Solid fuel',
            description: 'For example, coal',
          },
          {
            label: 'Renewable energy',
            value: 'Renewable energy',
            description: 'For example, solar thermal or heat pumps',
          },
          {
            label: 'District or communal heat networks',
            value: 'District or communal heat networks',
          },
          {
            label: 'Other',
            value: 'Other',
          },
        ],
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'accommodation-section-summary',
        when: [rules.listIsEmpty('household')],
      },
    },
    {
      goto: {
        block: 'own-or-rent',
      },
    },
  ],
}
