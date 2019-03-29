local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'degree-question',
  title: title,
  type: 'General',
  guidance: {
    content: [
      {
        title: 'Include equivalent qualifications achieved anywhere outside England and Wales',
      },
    ],
  },
  answers: [
    {
      id: 'degree-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
          description: 'For example degree, foundation degree, HND or HNC, NVQ level 4 and above, teaching or nursing',
        },
        {
          label: 'No',
          value: 'No',
          description: 'Questions on other NVQs, A levels, GCSEs and equivalents will follow',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Have you achieved a qualification at degree level or above?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved a qualification at degree level or above?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'degree',
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
