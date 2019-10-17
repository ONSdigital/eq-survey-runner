{
  type: 'ListCollectorDrivingQuestion',
  for_list: 'visitor',
  id: 'any-visitors',
  show_on_section_summary: false,
  question: {
    type: 'General',
    id: 'any-visitors-question',
    title: 'How many visitors were staying in your household overnight on Sunday 13 October 2019?',
    description: '<em>Tell respondent to turn to <strong>Showcard 13</strong></em>',
    guidance: {
      contents: [
        {
          description: 'A visitor is a person staying overnight in your household who usually lives at another address.',
        },
      ],
    },
    answers: [
      {
        id: 'any-visitors-answer',
        mandatory: false,
        options: [
          {
            label: '1 or more',
            value: '1 or more',
            action: {
              type: 'RedirectToListAddQuestion',
              params: {
                block_id: 'add-visitor',
                list_name: 'visitor',
              },
            },
          },
          {
            label: 'None',
            value: 'None',
          },
        ],
        type: 'Radio',
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'who-lives-here-section-summary',
        when: [{
          id: 'any-visitors-answer',
          condition: 'equals',
          value: 'None',
        }],
      },
    },
    {
      goto: {
        block: 'visitor-list-collector',
      },
    },
  ],
}
