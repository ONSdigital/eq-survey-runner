local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title) = {
  id: 'disability-limitation-question',
  title: title,
  guidance: {
    contents: [
      {
        title: 'Include problems relating to old age',
      },
    ],
  },
  type: 'General',
  answers: [
    {
      id: 'disability-limitation-answer',
      mandatory: true,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
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

local nonProxyTitle = 'Are your day-to-day activities limited because of a health problem, or disability which has lasted, or is expected to last, at least 12 months?';

local proxyTitle = {
  text: 'Are <em>{person_name_possessive}</em> day-to-day activities limited because of a health problem, or disability which has lasted, or is expected to last, at least 12 months?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'disability-limitation',
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
