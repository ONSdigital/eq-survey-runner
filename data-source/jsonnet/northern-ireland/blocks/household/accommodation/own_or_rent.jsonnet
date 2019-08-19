local placeholders = import '../../../lib/placeholders.libsonnet';

{
  type: 'Question',
  id: 'own-or-rent',
  question: {
    id: 'own-or-rent-question',
    title: {
      text: 'Does your household own or rent <em>{address}</em>?',
      placeholders: [placeholders.address],
    },
    type: 'General',
    answers: [{
      id: 'own-or-rent-answer',
      mandatory: true,
      options: [
        {
          label: 'Owns outright',
          value: 'Owns outright',
        },
        {
          label: 'Owns with a mortgage or loan',
          value: 'Owns with a mortgage or loan',
        },
        {
          label: 'Part owns and part rents',
          value: 'Part owns and part rents',
          description: 'Shared ownership',
        },
        {
          label: 'Rents',
          value: 'Rents',
          description: 'With or without housing benefit',
        },
        {
          label: 'Lives here rent free',
          value: 'Lives here rent free',
        },
      ],
      type: 'Radio',
    }],
  },
  routing_rules: [
    {
      goto: {
        block: 'number-of-vehicles',
        when: [{
          id: 'own-or-rent-answer',
          condition: 'equals',
          value: 'Owns outright',
        }],
      },
    },
    {
      goto: {
        block: 'number-of-vehicles',
        when: [{
          id: 'own-or-rent-answer',
          condition: 'equals',
          value: 'Owns with a mortgage or loan',
        }],
      },
    },
    {
      goto: {
        block: 'who-rent-from',
      },
    },
  ],
}
