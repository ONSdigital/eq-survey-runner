// Who lives here
local who_lives_here_interstitial = import 'ccs/blocks/who-lives-here/who_lives_here_interstitial.jsonnet';
local who_lives_here_section_summary = import 'ccs/blocks/who-lives-here/who_lives_here_section_summary.jsonnet';
local primary_person_list_collector = import 'ccs/blocks/who-lives-here/primary_person_list_collector.jsonnet';
local anyone_else_usually_living = import 'ccs/blocks/who-lives-here/anyone_else_usually_living.jsonnet';
local household_usual_address = import 'ccs/blocks/who-lives-here/household_usual_address.jsonnet';
local anyone_else_list_collector = import 'ccs/blocks/who-lives-here/anyone_else_list_collector.jsonnet';
local interviewer_note_interstitial = import 'ccs/blocks/who-lives-here/interviewer_note_interstitial.jsonnet';
local anyone_else_temp_away_list_collector = import 'ccs/blocks/who-lives-here/anyone_else_temp_away_list_collector.jsonnet';
local relationships = import 'ccs/blocks/who-lives-here/relationships.jsonnet';
local any_visitors = import 'ccs/blocks/who-lives-here/any_visitors.jsonnet';
local visitor_list_collector = import 'ccs/blocks/who-lives-here/visitor_list_collector.jsonnet';


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
            primary_person_list_collector,
            anyone_else_usually_living,
            interviewer_note_interstitial,
            household_usual_address,
            anyone_else_list_collector(census_date),
            anyone_else_temp_away_list_collector,
            relationships,
            any_visitors(census_date),
            visitor_list_collector(census_date),
            who_lives_here_section_summary,
          ],
        },
      ],
    },
  ],
}

