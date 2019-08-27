local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local questionTitle = {
  text: 'Does anyone usually live at {address}?',
  placeholders: [
    placeholders.address,
  ],
};

local anyoneElseOptionDescription(census_date) = {
  text: 'Include partners, children, babies born on or before {census_date}, housemates, tenants and lodgers, students and schoolchildren who live away from home during term time, where this is their permanent or family home',
  placeholders: [
    placeholders.censusDate(census_date),
  ],
};

function(census_date) {
  type: 'Question',
  id: 'anyone-usually-live-at',
  skip_conditions: [
    {
      when: [rules.hasPrimary],
    },
  ],
  question: {
    type: 'General',
    id: 'anyone-usually-live-at-question',
    title: questionTitle,
    answers: [
      {
        id: 'anyone-usually-live-at-answer',
        mandatory: true,
        type: 'Radio',
        options: [
          {
            label: 'Yes, I need to add someone',
            value: 'Yes, I need to add someone',
            description: anyoneElseOptionDescription(census_date),
            action: {
              type: 'RedirectToListAddQuestion',
              params: {
                block_id: 'add-person',
                list_name: 'household',
              },
            },
          },
          {
            label: 'No, no one usually lives here',
            value: 'No, no one usually lives here',
            description: 'For example, this is a second address or holiday home',
          },
        ],
      },
    ],
  },
  routing_rules: [
    {
      goto: {
        block: 'anyone-else-temp-away-list-collector',
        when: [{
          id: 'anyone-usually-live-at-answer',
          condition: 'equals',
          value: 'No, no one usually lives here',
        }],
      },
    },
    {
      goto: {
        block: 'anyone-else-list-collector',
      },
    },
  ],
}
