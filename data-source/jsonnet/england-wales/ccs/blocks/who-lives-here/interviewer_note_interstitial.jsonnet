{
  type: 'Interstitial',
  id: 'interviewer-note-interstitial',
  content: {
    title: '<em>Interviewer Note</em>',
    contents: [
      {
        description: 'Only interview a person who was usually living at the property on census night.',
      },
      {
        description: 'If none of those household members are available, you must save and sign out of the survey and return to the address to interview one of them at a later date.',
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'primary-person-list-collector',
      },
    },
  ],
}
