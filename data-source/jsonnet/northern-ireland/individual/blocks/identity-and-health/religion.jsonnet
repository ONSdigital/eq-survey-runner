local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'What religion, religious denomination or body do you belong to?';
local proxyTitle = {
  text: 'What religion, religious denomination or body does <em>{person_name}</em> belong to?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'religion-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: false,
  answers: [
    {
      id: 'religion-answer',
      mandatory: false,
      type: 'Checkbox',
      label: '',
      options: [
        {
          label: 'Roman Catholic',
          value: 'Roman Catholic',
        },
        {
          label: 'Presbyterian Church in Ireland',
          value: 'Presbyterian Church in Ireland',
        },
        {
          label: 'Church of Ireland',
          value: 'Church of Ireland',
        },
        {
          label: 'Methodist Church in Ireland',
          value: 'Methodist Church in Ireland',
        },
        {
          label: 'Other',
          value: 'Other',
          detail_answer: {
            id: 'religion-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify religion, religious denomination or body',
          },
        },
      ],
    },
    {
      id: 'religion-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'None',
          value: 'None',
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'religion',
  question_variants: [
    {
      question: question(nonProxyTitle),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle),
      when: [rules.isProxy],
    },
  ],
  routing_rules: [
    {
      goto: {
        block: 'no-religion',
        when: [
          {
            id: 'religion-answer',
            condition: 'not set',
          },
        ],
      },
    },
    {
      goto: {
        block: 'health',
        when: [rules.under3],
      },
    },
    {
      goto: {
        block: 'language',
      },
    },
  ],
}
