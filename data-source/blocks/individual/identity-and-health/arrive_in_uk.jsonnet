local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'arrive-in-uk-question',
  title: title,
  type: 'General',
  description: 'Do not count short visits away from the UK',
  answers: [
    {
      id: 'arrive-in-uk-answer',
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

{
  type: 'Question',
  id: 'arrive-in-uk',
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
            id: 'arrive-in-uk-answer',
            condition: 'greater than',
            date_comparison: {
              value: std.extVar('census_date'),
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
            id: 'arrive-in-uk-answer',
            condition: 'equals',
            date_comparison: {
              value: std.extVar('census_date'),
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
        block: 'understand-welsh',
        when: [rules.regionWales],
      },
    },
    {
      goto: {
        block: 'language',
      },
    },
  ],
}
