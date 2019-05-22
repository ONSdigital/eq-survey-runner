local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title) = {
  id: 'term-time-location-question',
  type: 'General',
  title: title,
  answers: [
    {
      id: 'term-time-location-answer',
      mandatory: true,
      type: 'Radio',
      options: [
        {
          label: {
            text: '{address}',
            placeholders: [
              placeholders.address,
            ],
          },
          value: 'household-address',
        },
        {
          label: 'Another address',
          value: 'Another address',
        },
      ],
    },
  ],
};

local nonProxyTitle = 'During term time, where do you usually live?';
local proxyTitle = {
  text: 'During term time, where does <em>{person_name}</em> usually live?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'term-time-location',
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
        group: 'comments-group',
        when: [
          {
            id: 'term-time-location-answer',
            condition: 'equals',
            value: 'Another address',
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
