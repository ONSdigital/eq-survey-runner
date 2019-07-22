local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'in-education-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'in-education-answer',
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


local nonProxyUnder16Title = 'Are you a schoolchild or student in full-time education?';
local proxyUnder16Title = {
  text: 'Is <em>{person_name}</em> a schoolchild or student in full-time education?',
  placeholders: [
    placeholders.personName,
  ],
};
local nonProxyOver16Title = 'Are you a student in full-time education?';
local proxyOver16Title = {
  text: 'Is <em>{person_name}</em> a student in full-time education?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'in-education',
  question_variants: [
    {
      question: question(nonProxyOver16Title),
      when: [rules.proxyNo, rules.over16],
    },
    {
      question: question(proxyOver16Title),
      when: [rules.proxyYes, rules.over16],
    },
    {
      question: question(nonProxyUnder16Title),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyUnder16Title),
      when: [rules.proxyYes],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'term-time-location',
        when: [
          {
            id: 'in-education-answer',
            condition: 'equals',
            value: 'Yes',
          },
        ],
      },
    },
    {
      goto: {
        group: 'identity-and-health-group',
      },
    },
  ],
}
