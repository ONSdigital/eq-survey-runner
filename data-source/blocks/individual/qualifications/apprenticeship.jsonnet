local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, regionGuidanceTitle) = {
  id: 'apprenticeship-question',
  title: title,
  type: 'General',
  guidance: {
    content: [
      {
        title: regionGuidanceTitle,
      },
    ],
  },
  answers: [
    {
      id: 'apprenticeship-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
          description: 'For example trade, advanced, foundation, modern',
        },
        {
          label: 'No',
          value: 'No',
        },
      ],
      type: 'Radio',
    },
  ],
};

local nonProxyTitle = 'Have you completed an apprenticeship?';
local proxyTitle = {
  text: 'Has <em>{person_name}</em> completed an apprenticeship?',
  placeholders: [
    placeholders.personName,
  ],
};

local notWalesGuidanceTitle = 'Include equivalent apprenticeships completed anywhere outside England and Wales';

local walesGuidanceTitle = 'Include equivalent apprenticeships completed anywhere outside Wales and England';

{
  type: 'Question',
  id: 'apprenticeship',
  question_variants: [
    {
      question: question(nonProxyTitle, notWalesGuidanceTitle),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, notWalesGuidanceTitle),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, walesGuidanceTitle),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, walesGuidanceTitle),
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
}
