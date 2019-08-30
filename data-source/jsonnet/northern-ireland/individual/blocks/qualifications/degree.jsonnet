local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local nonProxyTitle = 'Have you achieved a qualification at degree level or above?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved a qualification at degree level or above?',
  placeholders: [
    placeholders.personName,
  ],
};

local question(title) = {
  id: 'degree-question',
  title: title,
  type: 'General',
  guidance: {
    contents: [
      {
        description: 'Include equivalent qualifications achieved anywhere outside Northern Ireland',
      },
    ],
  },
  answers: [
    {
      id: 'degree-answer',
      mandatory: false,
      type: 'Radio',
      options: [
        {
          label: 'Yes',
          value: 'Yes',
          description: 'For example degree, foundation degree, HND or HNC, NVQ level 4 and above, teaching or nursing',
        },
        {
          label: 'No',
          value: 'No',
          description: 'Questions on GCSEs, A levels, other NVQs and equivalents will follow',
        },
      ],
    },
  ],
};

{
  type: 'Question',
  id: 'degree',
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
