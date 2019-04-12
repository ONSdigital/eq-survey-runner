local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, label) = {
  id: 'passports-question',
  title: title,
  description: '',
  type: 'MutuallyExclusive',
  mandatory: true,
  answers: [
    {
      id: 'passports-answer',
      mandatory: false,
      type: 'Checkbox',
      options: [
        {
          label: 'United Kingdom',
          value: 'United Kingdom',
        },
        {
          label: 'Ireland',
          value: 'Ireland',
        },
        {
          label: 'Other',
          value: 'Other',
          detail_answer: {
            id: 'passport-answer-other',
            type: 'TextField',
            mandatory: false,
            label: label,
          },
        },
      ],
    },
    {
      id: 'passports-answer-exclusive',
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

local nonProxyTitle = 'What passports do you hold?';
local nonProxyLabel = 'Please specify the passports you hold';
local proxyTitle = {
  text: 'What passports does <em>{person_name}</em> hold?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyLabel = 'Please specify the passports held';

{
  type: 'Question',
  id: 'passports',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyLabel),
      when: [rules.proxyNo],
    },
    {
      question: question(proxyTitle, proxyLabel),
      when: [rules.proxyYes],
    },
  ],
}
