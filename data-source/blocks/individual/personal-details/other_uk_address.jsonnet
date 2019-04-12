local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'other-address-question',
  title: title,
  type: 'General',
  answers: [
    {
      id: 'other-address-answer-building',
      label: 'House name or number',
      mandatory: true,
      type: 'TextField',
    },
    {
      id: 'other-address-answer-street',
      label: 'Street',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'other-address-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'other-address-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'other-address-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitle = 'Enter details of the other UK address where you stay for more than 30 days a year';
local proxyTitle = {
  text: 'Enter details of the other UK address where <em>{person_name_possessive}</em> stays for more than 30 days a year?',
  placeholders: [
    placeholders.personNamePossessive,
  ],
};

{
  type: 'Question',
  id: 'other-address',
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
