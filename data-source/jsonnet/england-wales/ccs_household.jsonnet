// Who lives here
local who_lives_here_interstitial = import 'ccs/blocks/who-lives-here/who_lives_here_interstitial.jsonnet';
local who_lives_here_section_summary = import 'ccs/blocks/who-lives-here/who_lives_here_section_summary.jsonnet';


function(region_code, census_date, census_month_year_date) {
  mime_type: 'application/json/ons/eq',
  schema_version: '0.0.1',
  data_version: '0.0.3',
  survey_id: 'census',
  title: '2019 Census Coverage Survey Test',
  description: 'Census England Coverage Survey Schema',
  theme: 'census',
  legal_basis: 'Voluntary',
  navigation: {
    visible: false,
  },
  metadata: [
    {
      name: 'user_id',
      type: 'string',
    },
    {
      name: 'period_id',
      type: 'string',
    },
    {
      name: 'display_address',
      type: 'string',
    },
  ],
  hub: {
    enabled: true,
    required_completed_sections: ['who-lives-here-section'],
  },
  sections: [
    {
      id: 'who-lives-here-section',
      title: 'People who live here',
      groups: [
        {
          id: 'who-lives-here-group',
          title: 'Who lives here',
          blocks: [
            who_lives_here_interstitial(census_date),
            who_lives_here_section_summary,
          ],
        },
      ],
    },
  ],
}

