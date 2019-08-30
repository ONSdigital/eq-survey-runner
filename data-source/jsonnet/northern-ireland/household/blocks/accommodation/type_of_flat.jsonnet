{
  type: 'Question',
  id: 'type-of-flat',
  question: {
    id: 'type-of-flat-question',
    title: 'Where is your flat, maisonette or apartment?',
    type: 'General',
    answers: [{
      id: 'type-of-flat-answer',
      mandatory: false,
      options: [
        {
          label: 'In a purpose-built block of flats',
          value: 'In a purpose-built block of flats',
        },
        {
          label: 'Part of a converted or shared house',
          value: 'Part of a converted or shared house',
          description: 'Including bedsits',
        },
        {
          label: 'In a commercial building',
          value: 'In a commercial building',
          description: 'For example, in an office building, hotel, or over a shop',
        },
      ],
      type: 'Radio',
    }],
  },
}
