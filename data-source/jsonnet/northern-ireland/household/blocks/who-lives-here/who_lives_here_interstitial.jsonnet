local placeholders = import '../../../lib/placeholders.libsonnet';

local contentDescription = {
  text: 'In this section, we’re going to ask you about the people living or staying at {address}.',
  placeholders: [
    placeholders.address,
  ],
};


function(census_date) {
  type: 'Interstitial',
  id: 'who-lives-here-interstitial',
  content: {
    title: 'People who live here',
    contents: [
      {
        description: contentDescription,
      },
      {
        title: 'You will need to know',
        list: [
          'Names of the people living at this address including anyone temporarily away.',
          'Names of visitors staying overnight at this address on 13 October 2019',
          // This date is currently hard coded as validator currently does not allow placeholders within list object.
        ],
      },
    ],
  },
}
