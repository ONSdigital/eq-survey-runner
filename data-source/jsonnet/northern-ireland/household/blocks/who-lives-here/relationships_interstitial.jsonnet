{
  type: 'Interstitial',
  id: 'relationships-interstitial',
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
  content: {
    title: 'Household relationships',
    contents: [
      {
        description: 'In this section, we’ll ask you how the people who usually live in this household are related to each other.',
      },
      {
        description: 'For the displayed household members, select the appropriate relationship from the options shown. The selected relationship will display at the bottom of the page for you to check.',
      },
    ],
  },
}
