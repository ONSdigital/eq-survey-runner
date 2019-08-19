// Accommodation
local accommodation_introduction = import 'blocks/household/accommodation/accommodation_introduction.jsonnet';
local accommodation_summary = import 'blocks/household/accommodation/accommodation_summary.jsonnet';
local accommodation_type = import 'blocks/household/accommodation/accommodation_type.jsonnet';
local central_heating = import 'blocks/household/accommodation/central_heating.jsonnet';
local number_bedrooms = import 'blocks/household/accommodation/number_bedrooms.jsonnet';
local number_of_vehicles = import 'blocks/household/accommodation/number_of_vehicles.jsonnet';
local own_or_rent = import 'blocks/household/accommodation/own_or_rent.jsonnet';
local self_contained = import 'blocks/household/accommodation/self_contained.jsonnet';
local type_of_flat = import 'blocks/household/accommodation/type_of_flat.jsonnet';
local type_of_house = import 'blocks/household/accommodation/type_of_house.jsonnet';
local who_rent_from = import 'blocks/household/accommodation/who_rent_from.jsonnet';

// Who lives here
local any_visitors = import 'blocks/household/who-lives-here/any_visitors.jsonnet';
local anyone_else_list_collector = import 'blocks/household/who-lives-here/anyone_else_list_collector.jsonnet';
local anyone_else_temporarily_away_list_collector = import 'blocks/household/who-lives-here/anyone_else_temporarily_away_list_collector.jsonnet';
local anyone_usually_live_at = import 'blocks/household/who-lives-here/anyone_usually_live_at.jsonnet';
local primary_person_list_collector = import 'blocks/household/who-lives-here/primary_person_list_collector.jsonnet';
local visitor_list_collector = import 'blocks/household/who-lives-here/visitor_list_collector.jsonnet';
local who_lives_here_interstitial = import 'blocks/household/who-lives-here/who_lives_here_interstitial.jsonnet';
local who_lives_here_section_summary = import 'blocks/household/who-lives-here/who_lives_here_section_summary.jsonnet';

// Relationships
local relationships_collector = import 'blocks/household/who-lives-here/relationships_collector.jsonnet';
local relationships_interstitial = import 'blocks/household/who-lives-here/relationships_interstitial.jsonnet';


function(region_code, census_date, census_month_year_date) {
  mime_type: 'application/json/ons/eq',
  schema_version: '0.0.1',
  data_version: '0.0.3',
  survey_id: 'census',
  title: '2019 Census Test',
  description: 'Census England Household Schema',
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
    required_completed_sections: ['who-lives-here-section', 'accommodation-section'],
  },
  sections: [
    {
      id: 'who-lives-here-section',
      title: 'People who live here and overnight visitors',
      groups: [
        {
          id: 'who-lives-here--group',
          title: 'Who lives here',
          blocks: [
            who_lives_here_interstitial(census_date),
            primary_person_list_collector,
            anyone_usually_live_at(census_date),
            anyone_else_list_collector(census_date),
            anyone_else_temporarily_away_list_collector,
            any_visitors(census_date),
            visitor_list_collector(census_date),
            who_lives_here_section_summary,
            relationships_interstitial,
            relationships_collector,
          ],
        },
      ],
    },
    {
      id: 'accommodation-section',
      title: 'Household accommodation',
      groups: [
        {
          id: 'accommodation-group',
          title: 'Household accommodation',
          blocks: [
            accommodation_introduction,
            accommodation_type,
            type_of_house,
            type_of_flat,
            self_contained,
            number_bedrooms,
            central_heating,
            own_or_rent,
            who_rent_from,
            number_of_vehicles,
            accommodation_summary,
          ],
        },
      ],
    },
  ],
}
