local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, regionOptions) = {
  id: 'other-qualifications-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: true,
  answers: [
    {
      id: 'other-qualifications-answer',
      mandatory: false,
      type: 'Checkbox',
      options: regionOptions,
    },
    {
      id: 'other-qualifications-answer-exclusive',
      type: 'Checkbox',
      mandatory: false,
      options: [
        {
          label: 'No qualifications',
          value: 'No qualifications',
        },
      ],
    },
  ],
};

local nonProxyTitle = 'Have you achieved any other qualifications?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> achieved any other qualifications?',
  placeholders: [
    placeholders.personName,
  ],
};

local englandOptions = [
  {
    label: 'Yes, in England or Wales',
    value: 'Yes, in England or Wales',
  },
  {
    label: 'Yes, anywhere outside of England and Wales',
    value: 'Yes, anywhere outside of England and Wales',
  },
];

local walesOptions = [
  {
    label: 'Yes, in Wales or England',
    value: 'Yes, in Wales or England',
  },
  {
    label: 'Yes, anywhere outside of Wales and England',
    value: 'Yes, anywhere outside of Wales and England',
  },
];

{
  type: 'Question',
  id: 'other-qualifications',
  question_variants: [
    {
      question: question(nonProxyTitle, englandOptions),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, englandOptions),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, walesOptions),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, walesOptions),
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
  routing_rules: [
    {
      goto: {
        group: 'employment-group',
      },
    },
  ],
}
