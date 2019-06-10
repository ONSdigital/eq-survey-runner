local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title) = {
  id: 'when-arrive-in-uk-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'when-arrive-in-uk-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No',
          value: 'No',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle(census_date) = {
  text: 'Did you arrive in the UK, on or after {census_date}',
  placeholders: [
    placeholders.censusDate(census_date),
  ],
};

local proxyTitle(census_date) = {
  text: 'Did <em>{person_name}</em> arrive in the UK, on or after {census_date}',
  placeholders: [
    placeholders.personName,
    placeholders.censusDate(census_date),
  ],
};

function(region_code, census_date) {
  type: 'Question',
  id: 'when-arrive-in-uk',
  question_variants: [
    {
      question: question(nonProxyTitle(census_date)),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle(census_date)),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'length-of-stay',
        when: [
          {
            id: 'when-arrive-in-uk-answer',
            condition: 'equals',
            value: 'Yes',
          },
        ],
      },
    },
    {
      goto: {
        block: 'national-identity',
        when: [
          {
            id: 'when-arrive-in-uk-answer',
            condition: 'equals',
            value: 'No',
          },
          rules.under3,
        ],
      },
    },
    {
      goto: {
        block: if region_code == 'GB-WLS' then 'understand-welsh' else 'language',
      },
    },
  ],
}
