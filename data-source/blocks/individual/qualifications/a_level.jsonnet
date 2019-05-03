local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, guidanceTitle, regionOptions) = {
  id: 'a-level-question',
  title: title,
  guidance: {
    content: [
      {
        title: guidanceTitle,
      },
    ],
  },
  type: 'MutuallyExclusive',
  mandatory: true,
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
          description: 'Include 2 to 3 AS levels',
        },
        {
          label: '1 AS level',
          value: '1 AS level',
        },
      ] + regionOptions,
    },
    {
      id: 'a-level-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'None of these apply',
          value: 'None of these apply',
          description: 'Questions on GCSEs and equivalents will follow',
        },
      ],
    },
  ],
};

local nonProxyTitle = 'Have you achieved an AS, A level or equivalent qualification?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved an AS, A level or equivalent qualification?',
  placeholders: [
    placeholders.personName,
  ],
};

local englandGuidanceTitle = 'Include equivalent qualifications achieved anywhere outside England and Wales';
local walesGuidanceTitle = 'Include equivalent qualifications achieved anywhere outside Wales and England';
local walesOptions = [{
  label: 'Advanced Welsh Baccalaureate',
  value: 'Advanced Welsh Baccalaureate',
}];

{
  type: 'Question',
  id: 'a-level',
  question_variants: [
    {
      question: question(nonProxyTitle, englandGuidanceTitle, []),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, englandGuidanceTitle, []),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, walesGuidanceTitle, walesOptions),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, walesGuidanceTitle, walesOptions),
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
}
