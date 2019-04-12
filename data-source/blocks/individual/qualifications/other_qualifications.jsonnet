local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'other-qualifications-question',
  title: title,
  type: 'MutuallyExclusive',
  mandatory: true,
  answers: [
    {
      id: 'other-qualifications-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'Yes, in England or Wales',
          value: 'Yes, in England or Wales',
        },
        {
          label: 'Yes, anywhere outside of England and Wales',
          value: 'Yes, anywhere outside of England and Wales',
        },
      ],
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

{
  type: 'Question',
  id: 'other-qualifications',
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
        group: 'employment-group',
      },
    },
  ],
}
