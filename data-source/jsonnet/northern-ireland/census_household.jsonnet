// Accommodation
local accommodation_introduction = import 'blocks/household/accommodation/accommodation_introduction.jsonnet';
local accommodation_summary = import 'blocks/household/accommodation/accommodation_summary.jsonnet';
local accommodation_type = import 'blocks/household/accommodation/accommodation_type.jsonnet';
local adapted = import 'blocks/household/accommodation/adapted.jsonnet';
local central_heating = import 'blocks/household/accommodation/central_heating.jsonnet';
local number_bedrooms = import 'blocks/household/accommodation/number_bedrooms.jsonnet';
local number_of_vehicles = import 'blocks/household/accommodation/number_of_vehicles.jsonnet';
local own_or_rent = import 'blocks/household/accommodation/own_or_rent.jsonnet';
local renewables = import 'blocks/household/accommodation/renewables.jsonnet';
local self_contained = import 'blocks/household/accommodation/self_contained.jsonnet';
local type_of_flat = import 'blocks/household/accommodation/type_of_flat.jsonnet';
local type_of_house = import 'blocks/household/accommodation/type_of_house.jsonnet';
local who_rent_from = import 'blocks/household/accommodation/who_rent_from.jsonnet';


function(region_code, census_date) {
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
  },
  sections: [
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
            adapted,
            central_heating,
            renewables,
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
