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

// Accommodation
local accommodation_introduction = import 'ccs/blocks/accommodation/accommodation_introduction.jsonnet';
local accommodation_type = import 'ccs/blocks/accommodation/accommodation_type.jsonnet';
local type_of_house = import 'ccs/blocks/accommodation/type_of_house.jsonnet';
local type_of_flat = import 'ccs/blocks/accommodation/type_of_flat.jsonnet';
local self_contained = import 'ccs/blocks/accommodation/self_contained.jsonnet';
local own_or_rent = import 'ccs/blocks/accommodation/own_or_rent.jsonnet';
local who_rent_from = import 'ccs/blocks/accommodation/who_rent_from.jsonnet';
local internet = import 'ccs/blocks/accommodation/internet.jsonnet';
local government_services = import 'ccs/blocks/accommodation/government_services.jsonnet';
local other_living_accommodation = import 'ccs/blocks/accommodation/other_living_accommodation.jsonnet';

// Individual
local individual_interstitial = import 'ccs/blocks/individual/individual_interstitial.jsonnet';
local proxy = import 'ccs/blocks/individual/proxy.jsonnet';
local date_of_birth = import 'ccs/blocks/individual/date_of_birth.jsonnet';
local confirm_dob = import 'ccs/blocks/individual/confirm_dob.jsonnet';
local sex = import 'ccs/blocks/individual/sex.jsonnet';
local country_of_birth = import 'ccs/blocks/individual/country_of_birth.jsonnet';
local marriage_type = import 'ccs/blocks/individual/marriage_type.jsonnet';

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
            accommodation_introduction,
            accommodation_type,
            type_of_house,
            type_of_flat,
            self_contained,
            own_or_rent,
            who_rent_from,
            internet,
            government_services,
            other_living_accommodation,
            who_lives_here_section_summary,
          ],
        },
      ],
    },
    {
      id: 'individual-section',
      title: 'Individual Section',
      repeat: {
        for_list: 'household',
        title: {
          text: '{person_name}',
          placeholders: [
            {
              placeholder: 'person_name',
              transforms: [
                {
                  transform: 'concatenate_list',
                  arguments: {
                    list_to_concatenate: {
                      source: 'answers',
                      identifier: ['first-name', 'last-name'],
                    },
                    delimiter: ' ',
                  },
                },
              ],
            },
          ],
        },
      },
      groups: [
        {
          id: 'personal-details-group',
          title: 'Personal Details',
          blocks: [
            individual_interstitial,
            proxy,
            date_of_birth(census_date),
            confirm_dob,
            sex,
            country_of_birth,
            marriage_type(census_date),
          ],
        },
      ],
    },
  ],
}

