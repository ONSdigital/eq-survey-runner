{
  type: 'Question',
  id: 'relationships',
  skip_conditions: [
    {
      when: [
        {
          list: 'household',
          condition: 'less than',
          value: 2,
        },
      ],
    },
  ],
  show_on_section_summary: false,
  question: {
    id: 'relationships-question',
    title: 'Are any of these people related to each other?',
    type: 'General',
    guidance: {
      contents: [
        {
          description: 'Remember to include partners and step-children as related',
        },
      ],
    },
    answers: [{
      id: 'relationships-answer',
      mandatory: false,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No, all household members are unrelated',
          value: 'No',
        },
      ],
      type: 'Radio',
    }],
  },
  list_summary: {
    for_list: 'household',
    summary: {
      item_title: {
        text: '{person_name}',
        placeholders: [
          {
            placeholder: 'person_name',
            transforms: [
              {
                arguments: {
                  delimiter: ' ',
                  list_to_concatenate: {
                    identifier: ['first-name', 'last-name'],
                    source: 'answers',
                  },
                },
                transform: 'concatenate_list',
              },
            ],
          },
        ],
      },
    },
  },
}
