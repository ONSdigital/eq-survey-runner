local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'Have you achieved an A level, AS level or equivalent qualifications?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved an A level, AS level or equivalent qualifications?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'a-level-question',
  title: title,
  guidance: {
    contents: [
      {
        description: 'Include equivalent qualifications achieved anywhere outside Northern Ireland',
      },
    ],
  },
  type: 'MutuallyExclusive',
  mandatory: false,
  answers: [
    {
      id: 'a-level-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: '2 or more A levels',
          value: '2 or more A levels',
          description: 'Include 4 or more AS levels',
        },
        {
          label: '1 A level',
          value: '1 A level',
          description: 'Include 2 or 3 AS levels',
        },
        {
          label: '1 AS level',
          value: '1 AS level',
        },
      ],
    },
    {
      id: 'a-level-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'None of these apply',
          value: 'None of these apply',
          description: 'Questions on NVQs and equivalents will follow',
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'a-level',
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
}
