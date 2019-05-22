local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

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
  type: 'General',
  answers: [
    {
      id: 'religion-answer',
      mandatory: false,
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
        {
          label: 'None',
          value: 'None',
        },
      ],
      type: 'Radio',
    },
  ],
};

{
  type: 'Question',
  id: 'religion',
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
        block: 'no-religion',
        when: [
          {
            id: 'religion-answer',
            condition: 'equals',
            value: 'None',
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
