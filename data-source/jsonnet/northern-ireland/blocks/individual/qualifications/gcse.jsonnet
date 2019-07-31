local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local nonProxyTitle = 'Have you achieved a GCSE or equivalent qualification?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved a GCSE or equivalent qualification?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'gcse-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: false,
  guidance: {
    contents: [
      {
        description: 'Include equivalent qualifications achieved anywhere outside Northern Ireland',
      },
    ],
  },
  answers: [
    {
      id: 'gcse-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: '5 or more GCSEs grades A* to C or 9 to 4',
          value: '5 or more GCSEs',
          description: 'Include 5 or more O level passes or CSEs grades 1',
        },
        {
          label: 'Any other GCSEs',
          value: 'Any other GCSEs',
          description: 'Include any other O levels or CSEs at any grades',
        },
      ],
    },
    {
      id: 'gcse-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'None of these apply',
          value: 'None of these apply',
          description: 'Questions on A levels, NVQs and equivalents will follow',
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'gcse',
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
}
