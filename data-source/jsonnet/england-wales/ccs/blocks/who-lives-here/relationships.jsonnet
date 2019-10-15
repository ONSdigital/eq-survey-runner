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
    title: 'Are any of these people related to each other? Remember to include partners and step-children as related.',
    type: 'General',
    answers: [{
      id: 'relationships-answer',
      mandatory: false,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No',
          value: 'No',
        },
      ],
      type: 'Radio',
    }],
  },
}
