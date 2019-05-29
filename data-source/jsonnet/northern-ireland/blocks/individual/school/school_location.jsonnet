local placeholders = import '../../../../common/lib/placeholders.libsonnet';
local rules = import '../../../../common/lib/rules.libsonnet';

local question(title) = {
  id: 'school-location-question',
  type: 'General',
  title: title,
  answers: [
    {
      id: 'school-address-details-answer-building',
      label: 'Building name or number',
      mandatory: true,
      type: 'TextField',
    },
    {
      id: 'school-address-details-answer-street',
      label: 'Street',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'school-address-details-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'school-address-details-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'school-address-details-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitle = 'What address do you travel to for your course of study, including school?';
local proxyTitle = {
  text: 'What address does <em>{person_name}</em> travel to for their course of study, including school?',
  placeholders: [
    placeholders.personName,
  ],
};

{
  type: 'Question',
  id: 'school-location',
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
