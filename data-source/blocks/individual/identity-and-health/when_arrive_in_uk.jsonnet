local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

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

local nonProxyTitle = {
  text: 'Did you arrive in the UK, on or after {census_date}',
  placeholders: [
    placeholders.censusDate,
  ],
};
local proxyTitle = {
  text: 'Did <em>{person_name}</em> arrive in the UK, on or after {census_date}',
  placeholders: [
    placeholders.personName,
    placeholders.censusDate,
  ],
};

{
  type: 'Question',
  id: 'when-arrive-in-uk',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle),
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
        block: 'understand-welsh',
        when: [
          {
            meta: 'region_code',
            condition: 'equals',
            value: 'GB-WLS',
          },
        ],
      },
    },
    {
      goto: {
        block: 'language',
      },
    },
  ],
}
