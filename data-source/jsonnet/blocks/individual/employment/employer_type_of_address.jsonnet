local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'employer-type-of-address-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'employer-type-of-address-answer',
      mandatory: true,
      options: [
        {
          label: 'At a workplace',
          value: 'At a workplace',
        },
        {
          label: 'Report to a depot',
          value: 'Report to a depot',
        },
        {
          label: 'At or from home',
          value: 'At or from home',
        },
        {
          label: 'An offshore installation',
          value: 'An offshore installation',
        },
        {
          label: 'No fixed place',
          value: 'No fixed place',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Where do you mainly work?';
local proxyTitle = {
  text: 'Where does <em>{person_name}</em> mainly work?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'employer-type-of-address',
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
        block: 'employer-address-workplace',
        when: [
          {
            id: 'employer-type-of-address-answer',
            condition: 'equals',
            value: 'At a workplace',
          },
        ],
      },
    },
    {
      goto: {
        block: 'employer-address-depot',
        when: [
          {
            id: 'employer-type-of-address-answer',
            condition: 'equals',
            value: 'Report to a depot',
          },
        ],
      },
    },
    {
      goto: {
        group: 'comments-group',
      },
    },
  ],
}
