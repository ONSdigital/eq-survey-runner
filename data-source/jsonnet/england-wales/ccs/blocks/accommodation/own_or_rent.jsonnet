local placeholders = import '../../../lib/placeholders.libsonnet';

{
  type: 'Question',
  id: 'own-or-rent',
  question: {
    id: 'own-or-rent-question',
    title: {
      text: 'Did your household own or rent <em>{address}</em>?',
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
          description: 'Including shared ownership',
        },
        {
          label: 'Rents with or without housing benefit',
          value: 'Rents with or without housing benefit',
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
        block: 'who-rent-from',
        when: [{
          id: 'own-or-rent-answer',
          condition: 'equals',
          value: 'Rents with or without housing benefit',
        }],
      },
    },
    {
      goto: {
        block: 'internet',
      },
    },
  ],
}
