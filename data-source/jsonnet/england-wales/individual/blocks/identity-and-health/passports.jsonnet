local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';

local question(title, label, definitionContent) = {
  id: 'passports-question',
  title: title,
  description: '',
  type: 'MutuallyExclusive',
  mandatory: false,
  definitions: [
    {
      title: 'What official documents can be included?',
      contents: [
        {
          description: definitionContent,
        },
      ],
    },
  ],
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
          description: 'Select to enter answer',
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

local nonProxyDefinitionContent = 'You may have other travel documents that show you are a citizen of a particular country. Please complete this question as if your travel documents are passports.';
local nonProxyTitle = 'What passports do you hold?';
local nonProxyLabel = 'Enter the passports you hold';
local proxyDefinitionContent = 'They may have other travel documents that show they are a citizen of a particular country. Please complete this question as if their travel documents are passports.';
local proxyTitle = {
  text: 'What passports does <em>{person_name}</em> hold?',
  placeholders: [
    placeholders.personName,
  ],
};
local proxyLabel = 'Enter passports held';

{
  type: 'Question',
  id: 'passports',
  question_variants: [
    {
      question: question(nonProxyTitle, nonProxyLabel, nonProxyDefinitionContent),
      when: [rules.isNotProxy],
    },
    {
      question: question(proxyTitle, proxyLabel, proxyDefinitionContent),
      when: [rules.isProxy],
    },
  ],
}
