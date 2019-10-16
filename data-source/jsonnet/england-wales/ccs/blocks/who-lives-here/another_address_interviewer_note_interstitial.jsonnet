{
  type: 'Interstitial',
  id: 'another-address-interviewer-note-interstitial',
  content: {
    title: '<em>Interviewer Note</em>',
    contents: [
      {
        description: 'If none of the household members were usually living at the property on census night, you must save and sign out of the survey and complete a paper questionnaire.',
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'who-lives-here-section-summary',
      },
    },
  ],
}
