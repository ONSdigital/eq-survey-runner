local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title, description) = {
  id: 'religion-question',
  title: title,
  description: 'This question is voluntary',
  type: 'General',
  answers: [
    {
      id: 'religion-answer',
      mandatory: false,
      label: 'Select one option only',
      options: [
        {
          label: 'No religion',
          value: 'No religion',
        },
        {
          label: 'Christian',
          value: 'Christian',
          description: description,
        },
        {
          label: 'Buddhist',
          value: 'Buddhist',
        },
        {
          label: 'Hindu',
          value: 'Hindu',
        },
        {
          label: 'Jewish',
          value: 'Jewish',
        },
        {
          label: 'Muslim',
          value: 'Muslim',
        },
        {
          label: 'Sikh',
          value: 'Sikh',
        },
        {
          label: 'Any other religion',
          value: 'Other',
          detail_answer: {
            id: 'religion-answer-other',
            type: 'TextField',
            mandatory: false,
            label: 'Please specify other religion',
          },
        },
      ],
      type: 'Checkbox',
    },
  ],
};

local nonProxyTitle = 'What is your religion?';
local proxyTitle = {
  text: 'What is <em>{person_name_possessive}</em> religion?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};
local englandDescription = 'Including Church of England, Catholic, Protestant and all other Christian denominations';
local walesDescription = 'All denominations';

{
  type: 'Question',
  id: 'religion',
  question_variants: [
    {
      question: question(nonProxyTitle, englandDescription),
      when: [rules.proxyNo, rules.regionNotWales],
    },
    {
      question: question(proxyTitle, englandDescription),
      when: [rules.proxyYes, rules.regionNotWales],
    },
    {
      question: question(nonProxyTitle, walesDescription),
      when: [rules.proxyNo, rules.regionWales],
    },
    {
      question: question(proxyTitle, walesDescription),
      when: [rules.proxyYes, rules.regionWales],
    },
  ],
}
