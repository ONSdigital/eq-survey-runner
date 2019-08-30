local placeholders = import '../../../lib/placeholders.libsonnet';


function(census_date) {
  type: 'Interstitial',
  id: 'visitor-interstitial',
  content: {
    title: 'Visitors',
    contents: [
      {
        description: {
          text: 'In this section, we’re going to ask you about any visitors that were staying overnight at <strong>{address}</strong> on {census_date}.',
          placeholders: [
            placeholders.address,
            placeholders.censusDate(census_date),
          ],
        },
      },
      {
        title: 'You will need to know',
        list: [
          'Date of birth.',
          'Usual address',
          'Sex',
        ],
      },
      {
        description: 'We ask for visitor information to check that everyone is counted. This helps to produce accurate population estimates. Add any visitors, even if you think they may have been counted elsewhere.',
      },
    ],
  },
}
