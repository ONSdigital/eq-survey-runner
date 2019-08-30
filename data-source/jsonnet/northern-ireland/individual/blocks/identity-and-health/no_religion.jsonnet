local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'What religion, religious denomination or body were you <em>brought up</em> in?';
local proxyTitle = {
  text: 'What religion, religious denomination or body was {person_name} <em>brought up</em> in?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'no-religion-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: false,
  answers: [
    {
      id: 'no-religion-answer',
      mandatory: false,
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
            id: 'no-religion-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify religion, religious denomination or body',
          },
        },
      ],
      type: 'Checkbox',
    },
    {
      id: 'no-religion-answer-exclusive',
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
  id: 'no-religion',
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
