local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, label) = {
  id: 'ever-worked-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'ever-worked-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes, in the last 12 months',
          value: 'Yes, in the last 12 months',
        },
        {
          label: 'Yes, but not in the last 12 months',
          value: 'Yes, but not in the last 12 months',
        },
        {
          label: label,
          value: label,
        },
      ],
      type: 'Radio',
    },
  ],
};

local studyRouting(label) = [
  {
    goto: {
      group: 'school-group',
      when: [
        {
          id: 'ever-worked-answer',
          condition: 'equals',
          value: label,
        },
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
      group: 'school-group',
      when: [
        {
          id: 'ever-worked-answer',
          condition: 'equals',
          value: label,
        },
        {
          id: 'employment-type-answer',
          condition: 'contains',
          value: 'Studying',
        },
      ],
    },
  },
];

local summaryRouting(label) = [
  {
    goto: {
      group: 'submit-group',
      when: [
        {
          id: 'ever-worked-answer',
          condition: 'equals',
          value: label,
        },
      ],
    },
  },
];

local nonProxyTitle = 'Have you ever done any paid work?';
local nonProxyLabel = 'No, have never worked';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> ever done any paid work?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyLabel = 'No, has never worked';

{
  type: 'Question',
  id: 'ever-worked',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyLabel),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyLabel),
      when: [rules.proxyYes],
    },
  ],
  routing_rules:
    studyRouting(nonProxyLabel) +
    studyRouting(proxyLabel) +
    summaryRouting(nonProxyLabel) +
    summaryRouting(proxyLabel) + [
      {
        goto: {
          block: 'main-employment-block',
        },
      },
    ],
}
