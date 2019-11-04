local placeholders = import '../../../lib/placeholders.libsonnet';

function(census_date) {
  type: 'Interstitial',
  id: 'who-lives-here-interstitial',
  content: {
    title: 'Household definition',
    contents: [
      {
        description: 'All the questions are about the people in your household on Sunday 13 October 2019.',
      },
      {
        description: 'A <em>household</em> is one person living alone or a group of people (not necessarily related) who share cooking facilities and share a\n        living room <em>OR</em> sitting room <em>OR</em> dining area.',
      },
      {
        description: 'Here are some cards to help with answering the questions.',
      },
    ],
  },
}
