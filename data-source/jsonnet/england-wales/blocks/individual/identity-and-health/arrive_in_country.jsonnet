local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title) = {
  id: 'arrive-in-country-question',
  title: title,
  type: 'General',
  description: 'Do not count short visits away from the UK',
  answers: [
    {
      id: 'arrive-in-country-answer',
      mandatory: true,
      type: 'MonthYearDate',
    },
  ],
};

local nonProxyTitle = 'When did you most recently arrive to live in the United Kingdom?';
local proxyTitle = {
  text: 'When did <em>{person_name}</em> most recently arrive to live in the United Kingdom?',
  placeholders: [
    placeholders.personName,
  ],
};

function(region_code, census_date) {
  type: 'Question',
  id: 'arrive-in-country',
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
            id: 'arrive-in-country-answer',
            condition: 'greater than',
            date_comparison: {
              value: census_date,
              offset_by: {
                years: -1,
              },
            },
          },
        ],
      },
    },
    {
      goto: {
        block: 'when-arrive-in-uk',
        when: [
          {
            id: 'arrive-in-country-answer',
            condition: 'equals',
            date_comparison: {
              value: census_date,
              offset_by: {
                years: -1,
              },
            },
          },
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
