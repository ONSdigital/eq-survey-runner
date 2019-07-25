local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import '../../../lib/rules.libsonnet';

local question(title) = {
  id: 'work-location-question',
  type: 'General',
  title: title,
  answers: [
    {
      id: 'work-address-details-answer-building',
      label: 'Address line 1',
      mandatory: true,
      type: 'TextField',
    },
    {
      id: 'work-address-details-answer-street',
      label: 'Address line 2',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'work-address-details-answer-city',
      label: 'Town or city',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'work-address-details-answer-county',
      label: 'County (optional)',
      mandatory: false,
      type: 'TextField',
    },
    {
      id: 'work-address-details-answer-postcode',
      label: 'Postcode',
      mandatory: false,
      type: 'TextField',
    },
  ],
};

local nonProxyTitleWork = 'What address do you travel to for your main place of work?';
local proxyTitleWork = {
  text: 'What address does <em>{person_name}</em> travel to for your main place of work?',
  placeholders: [
    placeholders.personName,
  ],
};

local pastNonProxyTitleWork = 'What address did you travel to for your main place of work?';
local pastProxyTitleWork = {
  text: 'What address did <em>{person_name}</em> travel to for their main place of work?',
  placeholders: [
    placeholders.personName,
  ],
};


{
  type: 'Question',
  id: 'work-location',
  question_variants: [
    {
      question: question(nonProxyTitleWork),
      when: [rules.proxyNo, rules.mainJob],
    },
    {
      question: question(proxyTitleWork),
      when: [rules.proxyYes, rules.mainJob],
    },
    {
      question: question(pastNonProxyTitleWork),
      when: [rules.proxyNo],
    },
    {
      question: question(pastProxyTitleWork),
      when: [rules.proxyYes],
    },
  ],
}
